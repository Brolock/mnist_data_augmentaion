#TODO real passwords with docker secret
mysql:
docker run --name database -e MYSQL_USER=bob -e MYSQL_PASSWORD=popo -e MYSQL_DATABASE=porygon -d mysql

image_gen:
docker run -d --network image -e "RABBITMQ_HOST=rabbit-server" --name image_gen  image_generator python rabbit_handler.py

web backend:
 docker run -d -e RABBITMQ_HOST=rabbit-server -e MYSQL_USER=bob -e MYSQL_PASSWORD=popo -e MYSQL_DATABASE=porygon -e MYSQL_HOST=database --name backend --network image web-backend flask run --host=0.0.0.0

database-handler:
docker run -d -e RABBITMQ_HOST=rabbit-server -e MYSQL_USER=bob -e MYSQL_PASSWORD=popo -e MYSQL_DATABASE=porygon -e MYSQL_HOST=database --network image --volumes-from image_gen --name db-handler database_handler

rabbitmq:
docker run -d --network image --name rabbit-server rabbitmq


images names:
image_generator

web backend:
web-backend

database-handler:
database_handler

rabbitmq:
rabbit-server
