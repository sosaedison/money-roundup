# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install curl
RUN apt-get update && apt-get install -y curl

RUN useradd -ms /bin/bash appuser

WORKDIR /home/app

COPY . .

RUN chown -R appuser:appuser /home/app

USER appuser

# Add app source code to pythonpath
ENV PYTHONPATH /home/app

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

RUN mkdir -p ~/.aws && \
    echo "[default]" > ~/.aws/config && \
    echo "region = ${AWS_REGION}" >> ~/.aws/config
# echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >> ~/.aws/config && \
# echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" >> ~/.aws/config && \

CMD [ "python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "moneyroundup.main:app", "--reload", "--host=0.0.0.0", "--port=8080" ]
