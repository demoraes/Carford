# Dockerfile, Image, Container
FROM python:3.8

WORKDIR /carford-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./flaskr ./flaskr

RUN flask --app flaskr init-db

ENTRYPOINT ["flask"]

CMD ["--app", "flaskr", "--debug", "run", "--host=0.0.0.0"]