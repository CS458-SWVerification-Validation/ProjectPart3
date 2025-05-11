from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.user import bp
from app.models.custom_survey import CustomSurvey

@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if current_user:
        surveys = CustomSurvey.query.filter_by(user_id=current_user.id).order_by(CustomSurvey.id.desc()).all()
        return render_template('user/dashboard.html', surveys=surveys), 200
    else:
        return redirect(url_for("auth.login"))