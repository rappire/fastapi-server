#!/bin/sh
cd fastapi-server
git pull origin master
cd ..
docker stop fastapi
docker rm fastapi
docker rmi webserver
docker build -t webserver .
docker run -it -p 9999:8000 --name  fastapi webserver