from datetime import date
import jwt               # pip install PyJWT
import requests          # already in most stacks
from flask import (
    render_template, request, redirect, url_for, flash, session
)
from . import ready_survey_bp

AI_MODELS = ["ChatGPT", "Bard", "Claude", "Copilot"]

@ready_survey_bp.route("/form", methods=["GET", "POST"])
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
        # ---- decode auth token (from session cookie) ----
        token = session.get("auth_token", "")
        try:
            user_id = jwt.decode(token, "secret_key", ["HS256"])["user_id"]
        except Exception:
            flash("Authentication failed – please log in again.", "danger")
            return redirect(url_for("auth.login"))

        # ---- submit to back-end API ----
        resp = requests.post(
            f"https://validsoftware458.com.tr:8443/survey/submit/{user_id}",
            json=values, timeout=10
        )
        if resp.ok:
            flash("Survey submitted – thank you!", "success")
            return redirect(url_for("user.dashboard"))
        flash("Server error: " + resp.text, "danger")
        return render_template(
            "ready_survey.html",
            ai_models=AI_MODELS,
            selected=form.getlist("ai_models"),
            values=form
        )
    # GET or failed POST
    return render_template("ready_survey.html", ai_models=AI_MODELS,
                           selected=[], values={})
