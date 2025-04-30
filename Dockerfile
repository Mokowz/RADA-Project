FROM python:3.12-slim-bookworm

WORKDIR /app/final/rada/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN python3 -m pip install https://storage.googleapis.com/tensorflow/versions/2.19.0/tensorflow_cpu-2.19.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
RUN apt-get update && apt-get install -y \
    netcat-traditional

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./wait-for-migrations.sh
# COPY wait-for-migrations.sh /usr/bin/wait-for-migrations.sh


# ENTRYPOINT [ "/bin/bash", "run_django.sh" ]