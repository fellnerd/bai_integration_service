@echo off
SET "repoPath=C:\bai_integration_service"
SET "repoURL=https://github.com/fellnerd/bai_integration_service.git"
SET "branchName=ssk-win"

IF EXIST "%repoPath%" (
    echo Removing existing directory at %repoPath%...
    rd /s /q "%repoPath%"
)

echo Cloning the repository from the %branchName% branch to %repoPath%...
git clone -b %branchName% %repoURL% "%repoPath%"
IF ERRORLEVEL 1 (
    echo Failed to clone the repository.
    pause > nul
    exit /b 1
)

cd /d %repoPath%

IF NOT EXIST ".venv" (
    echo Setting up the virtual environment...
    python -m venv .venv
)

echo Installing dependencies from requirements.txt...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt


call .venv\Scripts\python -m flask run

echo Flask application has stopped. Press any key to close this window.
pause > nul
