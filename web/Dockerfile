FROM python:3-slim

WORKDIR /usr/src/web

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host=0.0.0.0"]
