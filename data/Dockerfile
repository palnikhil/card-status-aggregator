# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY data/requirements.txt /data-service/requirements.txt
COPY data/csv_files /data-service/csv_files
COPY data/etl_pipeline.py /data-service/etl_pipeline.py
COPY data/config.py /data-service/config.py

WORKDIR /data-service

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps


ENTRYPOINT ["python3","etl_pipeline.py"]