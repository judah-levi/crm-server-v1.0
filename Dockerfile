FROM python:3.8-slim-buster

COPY . /api
WORKDIR /api

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


ENTRYPOINT [ "sh", "run_config.sh" ]
