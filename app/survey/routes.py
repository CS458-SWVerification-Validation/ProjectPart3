from flask import request, jsonify, flash, render_template, redirect, url_for
from flask_login import logout_user, current_user
import json
from datetime import date

from app.survey import bp
from app.extensions import db
from app.models.user import User
from app.models.survey import Survey
from app.mail import send_email

final_uri = "myapp://home"

@bp.route("/submit/<user_id>", methods=["POST"])
def submit_survey(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if user:
        data = request.get_json()
        survey = Survey(
            user_id=user_id,
            name=data.get('name'),
            surname=data.get('surname'),
            birth_date=data.get('birthDate'),
            education_level=data.get('educationLevel'),
            city=data.get('city'),
            gender=data.get('gender'),
            models_and_defects=json.dumps(data.get('defects')),
            use_case=data.get('useCase')
        )
        db.session.add(survey)
        if user.email:
            send_email("About Survey", 
                    f"Your survey submitted successfully!\n\nName: {survey.name}\nSurname: {survey.surname}\nBirthdate: {survey.birth_date}\nCity: {survey.city}\nEducation Level: {survey.education_level}\nGender: {survey.gender}\nModels&Defects: {survey.models_and_defects}\n Use Cases: {survey.use_case}", 
                    user.email)

        if current_user.is_authenticated:
            logout_user()
            print("Logout successfull")
        db.session.commit()
        db.session.close()
        return jsonify({'message': 'Survey submitted successfully'}), 200
    else:
        return jsonify({'message': 'User does not exist'}), 200
    

AI_MODELS = ["ChatGPT", "Bard", "Claude", "Copilot"]

@bp.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        form = request.form
        # pull everything with .get so we never KeyError
        name            = form.get("name",         "").strip()
        surname         = form.get("surname",      "").strip()
        birthDate       = form.get("birthDate",    "").strip()
        educationLevel  = form.get("educationLevel","")
        city            = form.get("city",         "")
        gender          = form.get("gender",       "")
        useCase         = form.get("useCase",      "")

        errors = []
        if not name:
            errors.append("Name is required.")
        if not surname:
            errors.append("Surname is required.")
        if not birthDate:
            errors.append("Birthdate is required.")
        else:
            try:
                if date.fromisoformat(birthDate) > date.today():
                    errors.append("Birth date cannot be in the future.")
            except ValueError:
                errors.append("Birth date must be YYYY-MM-DD.")
        # --- NEW: require these fields, too ---
        if not educationLevel:
            errors.append("Education level is required.")
        if not city:
            errors.append("City is required.")
        if not gender:
            errors.append("Gender is required.")

        # EARLY RETURN ON ANY VALIDATION ERROR
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "ready_survey.html",
                ai_models=AI_MODELS,
                selected=form.getlist("ai_models"),
                values=form
            )
        # ---- build JSON identical to original mobile payload ----
       
        user_id = current_user.id
        user = User.query.filter_by(id=user_id).first_or_404()
        if user:
            values = {
                "name": name,
                "surname": surname,
                "birthDate": birthDate,
                "educationLevel": educationLevel,
                "city": city,
                "gender": gender,
                "defects": {
                    k.split("_", 1)[1]: v
                    for k, v in form.items() if k.startswith("defect_")
                },
                "useCase": useCase,
            }
            if user.email:
                send_email("About Survey", 
                        f"Your survey submitted successfully!\n\nName: {values['name']}\nSurname: {values['surname']}\nBirthdate: {values['birthDate']}\nCity: {values['city']}\nEducation Level: {values['educationLevel']}\nGender: {values['gender']}\nModels&Defects: {values['defects']}\n Use Cases: {values['useCase']}", 
                        user.email)
            flash("Survey submitted – thank you!", "success")
            return redirect(url_for("user.dashboard"))
        else:
            flash("Server error!", "danger")
            return render_template(
                "ready_survey.html",
                ai_models=AI_MODELS,
                selected=form.getlist("ai_models"),
                values=form
            )
        
    return render_template("ready_survey/ready_survey.html", ai_models=AI_MODELS,
                           selected=[], values={})