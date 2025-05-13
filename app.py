from app import create_app
from app.ready_survey import ready_survey_bp


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")