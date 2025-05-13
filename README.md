# ProjectPart3

This is the Flask App for CS458 Project.

# Getting Started

> [!WARNING]
> (For Windows) If Visual Studio Code is the used\
> IDE, it is advised to use CMD instead of PowerShell\
> since if the required permissions are not given\
> to PowerShell it will not run the scripts that are \
> needed for the next steps.

## Cloning Repository

This step clones the project repository onto your\
local machine.

```bash
git clone https://github.com/CS458-SWVerification-Validation/ProjectPart1.git
```

## Python Virtual Environment Setup

Python virtual environment used to both install\
dependencies and run the Flask application on, which\
provides a clean and isolated development environment for Python\
projects easing the management process.

For Windows:
```bash
cd ProjectPart1
python -m venv env
.\env\Scripts\activate
```

For Linux/MacOS:
```bash
cd ProjectPart1
python -m venv env
source env/bin/activate
```

If '(env)' is seen at the start of the command line\
the first part of the setup is complete.

## Dependency Installation

This command installs all the necessary dependencies\
for the project to run. After the installation only\
database setup remains.

```bash
pip install -r requirements.txt
```

## Database Setup

This command block will initialize the migration repository,\
detect the changes made on the SQLAlchemy models and run the\
latest migration scripts onto the database.

```bash
flask db init
flask db migrate
flask db upgrade
```

## Running the Flask App

This command is used to run the code on the development environment.

```bash
python app.py
```

Now the Flask application would run on [http://127.0.0.1:5000](http://127.0.0.1:5000)


