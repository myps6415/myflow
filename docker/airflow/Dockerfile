FROM apache/airflow:latest-python3.10
USER root

RUN apt-get update && \
    apt-get install -y gcc python3-dev ffmpeg

COPY requirements.txt .
RUN python -m pip install --upgrade pip

USER airflow
RUN pip install -r requirements.txt