
FROM python:3

RUN pip install pipenv

WORKDIR /usr/src/app

RUN mkdir /data

VOLUME /data

COPY Pipfile ./

RUN pipenv --three

COPY . .

RUN pipenv install

RUN pipenv run python migrate.py

CMD [ "pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "wsgi" ]
