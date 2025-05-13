from flask import Blueprint
ready_survey_bp = Blueprint(
    "ready_survey", __name__, template_folder="../../templates"
)

# routes live in views.py so the blueprint is clean
from . import views          # noqa: E402,F401
