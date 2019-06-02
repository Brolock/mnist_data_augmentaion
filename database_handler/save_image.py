#! /usr/bin/env python3

import pika
import json
import mysql.connector

import glob
import os
import binascii

import logging

images_dir = os.path.join("/data", "generated_numbers")

def callback(ch, method, properties, body):
    logging.info("received body: {}".format(body))
    json_content = json.loads(body)
    user_id, query_id = json_content["user_id"], json_content["query_id"]
    images = [f for f in glob.glob(images_dir + "/{}/**/*.png".format(query_id))]
    #TODO PREFIX FOR images
    logging.info("images to copy: {}".format(images))
    for img_path in images:
        # The first part of the image name is the number it represents
        image_description = os.path.basename(img_path).split("_")[0]
        number_of_digits = len(image_description)

        add_image = ("INSERT INTO images (user_id, number_of_digits, image_description, image) "
                "VALUES (%s, %s, %s, UNHEX(\"%s\"))")
        logging.info("Copying image {} to database".format(img_path))
        with open(img_path, 'rb') as img_file:
            img_content = img_file.read()
            cmd = add_image % (user_id, number_of_digits, image_description, binascii.hexlify(img_content).decode())
            logging.info("Running command: {}".format(cmd))
            cursor.execute(cmd)
            cnx.commit()

#TODO: MOVE ELSEWHERE
def get_env(env_var):
    if env_var in os.environ:
        return os.environ[env_var]
    else:
        raise Exception("No {} argument provided, can't connect".format(env_var))

## Connect to MySQL
sql_params = {env_var: get_env(env_var) for env_var in
        ["MYSQL_DATABASE", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST"]}

# TODO Handle connexion error
cnx = mysql.connector.connect(user=sql_params["MYSQL_USER"],
                              host=sql_params["MYSQL_HOST"],
                              password=sql_params["MYSQL_PASSWORD"],
                              database=sql_params["MYSQL_DATABASE"])

cursor = cnx.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS images("
        "image_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
        "user_id INTEGER NOT NULL,"
        "number_of_digits INTEGER UNSIGNED NOT NULL,"
        "image_description TEXT,"
        "image BLOB NOT NULL,"
        "FOREIGN KEY(user_id) REFERENCES users(user_id))"
    "DEFAULT CHARACTER SET = utf8 COLLATE = utf8_bin")

## Connect to rabbit
if "RABBITMQ_HOST" in os.environ:
    host_dest = os.environ["RABBITMQ_HOST"]
else:
    host_dest = "localhost"

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(pika.ConnectionParameters(host_dest))
channel = connection.channel()

logging.info("Rabbit Channel: {}".format(channel))

channel.basic_consume(queue="db-save",
                      auto_ack=True,
                      on_message_callback=callback)

channel.start_consuming()
