# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY card-status-service/requirements.txt /card-status-service/requirements.txt
COPY card-status-service/app /card-status-service/app
COPY card-status-service/zywadb /card-status-service/zywadb


WORKDIR /card-status-service

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps


EXPOSE 8080

CMD gunicorn "app.api:app" -k uvicorn.workers.UvicornWorker --workers 3 --bind 0.0.0.0:8080