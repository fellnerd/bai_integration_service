# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN net user appuser && mkdir C:\app && chown -R appuser:C:\app

# Switch to the newly created user
USER appuser

# Expose port 80
EXPOSE 80

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
