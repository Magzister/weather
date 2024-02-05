FROM python:3.12-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./weather_app /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN adduser -D app
USER app

CMD ["entrypoint.sh"]
