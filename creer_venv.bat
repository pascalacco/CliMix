@echo off
set VENV_DIR=venv
set REQUIREMENTS_FILE=requirements.txt

:: Create Python virtual environment
python -m venv %VENV_DIR%

:: Activate the virtual environment
call %VENV_DIR%\Scripts\activate

:: Install packages from requirements file into the virtual environment
pip install -r %REQUIREMENTS_FILE%

:: Upgrade pip to the latest version
pip install -r requirements.txt
pip install -r notebooks_requirements.txt
pip install -e .

pause

