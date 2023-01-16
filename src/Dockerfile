FROM python:3.10-alpine

# set working directory and cd into it automatically
WORKDIR /app
COPY . .

# copy to and install requirements
RUN pip install -r requirements.txt

WORKDIR /src

CMD [ "uvicorn", "main:app" ]