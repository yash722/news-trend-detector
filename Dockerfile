FROM apache/airflow:2.8.1-python3.10

USER root

RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    curl \
    telnet \
    && apt-get clean

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
