from flask import request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_user, login_required, logout_user, current_user
import json

from app.custom_survey import bp
from app.extensions import db
from app.models.user import User
from app.models.custom_survey import CustomSurvey, Question, Option, ConditionalLogic

@bp.route('/designer', methods=['GET', 'POST'])
@login_required
def survey_designer():

    if request.method == "POST":
        data = json.loads(request.form['survey_json'])
        title = request.form.get('title', 'Untitled Survey')
        
        if not title.strip() or title.strip() == "":
            flash("Survey title cannot be empty.", "error")
            return render_template('custom_survey/survey_designer.html')


        survey = CustomSurvey(title=title, user_id=current_user.id)
        db.session.add(survey)

        if len(data) == 0:
            flash("Any survey should have at least ONE question.", "error")
            return render_template('custom_survey/survey_designer.html')

        for q in data:
            if (not q['question'] or q['question'] == "") or (not q['type'] or q['type'] == ""):
                    flash("Each question must have text and type.", "error")
                    return render_template('custom_survey/survey_designer.html')

            question = Question(
                text=q['question'],
                question_type=q['type'],
                required=q.get('required', False),
                survey=survey
            )
            db.session.add(question)

            # Add options if applicable
            if q['type'] in ['multiple_choice', 'dropdown', 'checkbox']:
                if len(q['options']) == 0:
                    flash("Each question must have options.", "error")
                    return render_template('custom_survey/survey_designer.html')

                for opt in q['options']:
                    db.session.add(Option(text=opt, question=question))

            # Add conditional logic if applicable
            if 'conditional' in q:
                cond = ConditionalLogic(
                    question=question,
                    show_if_question_id=q['conditional']['show_if']['question_id'],
                    expected_value=q['conditional']['show_if']['value']
                )
                db.session.add(cond)

        db.session.commit()
        return redirect(url_for('user.dashboard'))
    
    return render_template('custom_survey/survey_designer.html')