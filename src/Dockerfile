# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

RUN mkdir -p ~/.aws && \
    echo "[default]" > ~/.aws/config && \
    echo "region = ${AWS_REGION}" >> ~/.aws/config
# echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >> ~/.aws/config && \
# echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/config && \

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "moneyroundup.main:app"]
CMD ["uvicorn", "moneyroundup.main:app", "--host=0.0.0.0", "--port=8000"]
