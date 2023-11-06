FROM python:3.10-alpine

ARG AUTHORISATION_API_PORT

WORKDIR /app

RUN apk add --update gcc g++ build-base

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE $AUTHORISATION_API_PORT

CMD ["sh", "/app/run.sh"]