FROM python:3.10-slim-bullseye

RUN apt-get update && \
  apt-get install -y \
  zip \
  curl \
  wget \
  # python3 \
  # python3-pip \
  # python3-setuptools \
  && pip3 install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*

# RUN pip3 --no-cache-dir install --upgrade awscli

WORKDIR /app

COPY src /app/src
# COPY entrypoint.py /app
# COPY requirements.txt /app
WORKDIR /app/src
RUN pip3 install -r requirements.txt

# ENV AWS_PAGER=""

ENTRYPOINT [ "python3", "-u", "main.py"]
