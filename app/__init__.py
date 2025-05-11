from flask import Flask, redirect, url_for, render_template, request, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient

import os
import json
import requests
from dotenv import load_dotenv
from config import config
from app.extensions import db
from app.models.user import User
from datetime import datetime

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_mode='development'):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins="*")
    app.config.from_object(config[config_mode])

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    def get_google_provider_cfg():
        return requests.get(os.getenv("GOOGLE_DISCOVERY_URL")).json()
    
    client = WebApplicationClient(os.getenv("GOOGLE_CLIENT_ID"))
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.getUserById(int(user_id))

    # Register blueprints here
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.survey import bp as survey_bp
    app.register_blueprint(survey_bp, url_prefix='/survey')

    from app.custom_survey import bp as custom_survey_bp
    app.register_blueprint(custom_survey_bp, url_prefix='/custom-survey')
    
    @app.route('/')
    def splash():
        return redirect(url_for("auth.login"))

    @app.route("/oauth", methods=["GET"])
    def login_google():
        print("oauth starts")
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        print(request.base_url)

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri= "https://127.0.0.1:5000/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

    @app.route("/callback", methods=["GET"])
    def login_callback():
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]  

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(os.getenv("GOOGLE_CLIENT_ID"), os.getenv("GOOGLE_CLIENT_SECRET")),
        )

        # Parse the tokens!
        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            users_firstname = userinfo_response.json()["given_name"]
            users_lastname = userinfo_response.json()["family_name"]
            print(userinfo_response.json())
            user = User.query.filter_by(email=users_email).first()
            if user:
                if user.check_password(unique_id):
                    flash('Logged in Successfully!', "success")
                    login_user(user)
                    return redirect(url_for("user.dashboard"))
                else:
                    flash('Invalid Credentials!', "error")
            else:
                db.session.add(User(birthdate=datetime.now(), phone_number="", firstname=users_firstname, lastname=users_lastname,
                                    email=users_email, password=unique_id))
                db.session.commit()

                user = User.query.filter_by(email=users_email).first()
                if user:
                    flash('Registered and Logged In Successfully!', "success")
                    login_user(user)
                    return redirect(url_for("user.dashboard"))
                else:
                    flash('Already Logged In!', "error")
                    return redirect(url_for("auth.login"))

        else:
            flash('Google Authentication Failed', "error")
            return redirect("/auth/login")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 200

    return app