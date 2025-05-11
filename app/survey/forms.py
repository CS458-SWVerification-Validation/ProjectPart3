from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, PasswordField, SubmitField
from wtforms import validators

class SurveyForm(FlaskForm):
    firstname = StringField(u'Firstname', [validators.DataRequired(), validators.Length(max=128)], render_kw={"placeholder": "Firstname"})
    lastname = StringField(u'Lastname', [validators.DataRequired(), validators.Length(max=128)], render_kw={"placeholder": "Lastname"})
    email = EmailField(u'Email', [validators.DataRequired(), validators.Length(max=128), validators.Email()], render_kw={"placeholder": "Email"})
    birthdate = DateField(u'Birthdate', [validators.DataRequired()])
    phone_number = StringField('Phone Number', [
        validators.DataRequired(),
        validators.Length(min=10, max=10, message="Phone number must be between 10 and 15 characters")
    ], render_kw={"placeholder": "Phone Number"})
    password = PasswordField(u'Password', [
        validators.DataRequired(), 
        validators.Length(min=8, max=20), 
        validators.EqualTo('confirm_password', message='Passwords must match')], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(u'Password', render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')