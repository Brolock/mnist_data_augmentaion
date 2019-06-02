import pika
import json
import os
import utility
import logging

from single_image_generator import generate_numbers_sequence

def callback(ch, method, properties, body):
    logging.info("received body: {}".format(body))
    spacing_range = [5, 6]
    # number log 10?
    image_width = 500

    # TODO: proper spacing and width
    number = json.loads(body)["number"]
    img = generate_numbers_sequence(number, spacing_range, image_width)

    utility.save_to_dir(img, number)

    # TODO: FORWARD USERID WHEN WORK IS DONE

if "RABBITMQ_HOST" in os.environ:
    host_dest = os.environ["RABBITMQ_HOST"]
else:
    host_dest = "localhost"

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(pika.ConnectionParameters(host_dest))
channel = connection.channel()

channel.basic_consume(queue="web-queries",
                      auto_ack=True,
                      on_message_callback=callback)

channel.start_consuming()
