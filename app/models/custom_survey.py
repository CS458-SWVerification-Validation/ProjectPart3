from app.extensions import db

class CustomSurvey(db.Model):
    __tablename__ = 'custom_survey'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questions = db.relationship('Question', backref='survey', cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('custom_survey.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.String(50))
    required = db.Column(db.Boolean, default=False)

    options = db.relationship('Option', backref='question', cascade='all, delete-orphan')

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(100), nullable=False)

class ConditionalLogic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False, unique=True)
    show_if_question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    expected_value = db.Column(db.String(100))

    question = db.relationship(
        'Question',
        foreign_keys=[question_id],
        backref=db.backref('conditional_logic', uselist=False, cascade='all, delete-orphan')
    )

    trigger_question = db.relationship('Question', foreign_keys=[show_if_question_id])