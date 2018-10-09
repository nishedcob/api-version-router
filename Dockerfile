
FROM python:3

WORKDIR /usr/src/app

RUN mkdir /data

COPY app.py migrate.py requirements.txt ./

RUN pip install -r requirements.txt

RUN python migrate.py

VOLUME /data

COPY . .

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi" ]
