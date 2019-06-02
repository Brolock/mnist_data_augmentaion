#TODO real passwords with docker secret
mysql:
docker run --name database -e MYSQL_USER=bob -e MYSQL_PASSWORD=popo -e MYSQL_DATABASE=porygon -d mysql
