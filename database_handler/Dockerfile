FROM python:3-slim

WORKDIR /usr/src/database_handler

COPY . .

RUN pip install -r requirements.txt

CMD ["./save_image.py"]
