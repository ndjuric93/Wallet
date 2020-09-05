FROM python:3.7-alpine

RUN adduser -D wallet

WORKDIR /home/wallet

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY wallet wallet
COPY migrations migrations
COPY config config
#COPY microblog.py config.py boot.sh ./
COPY boot.sh ./
RUN chmod +x boot.sh

RUN chown -R wallet:wallet ./
USER wallet

ENV FLASK_APP wallet.main:create_app(\"config.ProductionConfig\")

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
