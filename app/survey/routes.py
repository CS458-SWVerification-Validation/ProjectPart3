from flask import request, jsonify
from flask_login import logout_user, current_user
import json

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