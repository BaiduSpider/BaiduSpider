FROM python:3.8.1

RUN mkdir /api
WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install -r requirements.txt

COPY . /api

CMD uvicorn baiduspider.api.app:app --host=0.0.0.0
