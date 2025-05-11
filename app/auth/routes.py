from flask import request, jsonify, flash, redirect, url_for, render_template, render_template_string
from flask_login import login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
from hashlib import sha256
from datetime import datetime, timedelta
from user_agents import parse
import re
import jwt

from config import Config
from app.auth import bp
from app.extensions import db
from app.models.user import User
from app.auth.forms import LoginForm, RegisterForm

redirect_path = "/auth/callback"
final_uri = "myapp://auth"

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit(): #validation check
        password = form.password.data
        if is_email(form.email_or_phone.data):
            user = User.query.filter_by(email=form.email_or_phone.data).first()
        elif is_phone_number(form.email_or_phone.data):
            user = User.query.filter_by(phone_number=form.email_or_phone.data).first()
        else:
            flash('Please Enter a Valid Email or Phone Number!', "error")  
            return render_template('auth/login.html', form=form), 200
        
        if user and user.check_password(password):
            flash('Logged in Successfully!', "success")
            login_user(user)
            # Check if mobile or pc
            ua_string = request.headers.get("User-Agent")
            user_agent = parse(ua_string)
            if user_agent.is_mobile:
                print("Mobile Device")
                token = jwt.encode({"user_id": user.id}, "secret_key", algorithm="HS256")
                return redirect(f"/auth/callback?token={token}&final_uri={final_uri}")
            elif user_agent.is_pc:
                print("PC User")
                return redirect(url_for("user.dashboard"))
        else:
            flash('Invalid Credentials!', "error")

    return render_template('auth/login.html', form=form), 200

@bp.route("/callback")
def callback():
    token = request.args.get("token")
    final_uri = request.args.get("final_uri")
    print(token, final_uri)
    return render_template_string(f"""
        <html>
        <head><title>Redirecting...</title></head>
        <body>
            <p>Login successful. Redirecting to app...</p>
            <script>
                setTimeout(function() {{
                    console.log("It is redirecting!!!")
                    window.location.href = "{final_uri}?token={token}";
                }}, 100);
            </script>
        </body>
        </html>
    """)

@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash('Email already registered!', "error")
            else:
                db.session.add(User(birthdate=form.birthdate.data, phone_number=form.phone_number.data, 
                                    firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data,
                                    password=form.password.data))
                db.session.commit()

                flash('Registered Successfully!', "success")
                return redirect(url_for("auth.login"))
        elif form.errors:
            flash(form.errors["password"][0], "error")

    return render_template("auth/register.html", form=form), 200

@bp.route("/logout", methods=["GET"])
@login_required
def logout():

    if current_user.is_authenticated:
        flash('Successfully Logged Out!', "success")
        logout_user()
        return redirect("/auth/login")

    return jsonify(status="not logged in yet")

def is_email(identifier):
    try:
        validate_email(identifier)  # Tries to validate email
        return True
    except EmailNotValidError:
        return False
    
def is_phone_number(identifier):
    return re.fullmatch(r'^\+?\d{10}$', identifier) is not None