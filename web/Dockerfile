FROM debian:stable-slim as bootstrap
RUN apt-get update && apt-get install wget -y
RUN wget https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css

FROM python:3-slim

WORKDIR /usr/src/web

COPY --from=bootstrap bootstrap.min.css templates/
COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
