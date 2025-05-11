from app.extensions import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(10), nullable=True)
    education_level = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(20), nullable=True)

    models_and_defects = db.Column(db.String, nullable=True)       # Dict of model -> defect text
    use_case = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('surveys'))