FROM python:3.8
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

RUN adduser -D sid597

WORKDIR /var/www/bolowiki

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip3 install wheel
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn




COPY bolowikiApp bolowikiApp
COPY migrations migrations
COPY run.py boot.sh ./

RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R sid597:sid597 ./
USER sid597

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
