from flask import Blueprint

bp = Blueprint('custom-survey', __name__)

from app.custom_survey import routes