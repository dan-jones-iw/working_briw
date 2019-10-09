#!/usr/bin/env bash

echo 'copy to home in server'
sudo scp -r ~/PycharmProjects/BrIW/dynamic_website ubuntu@35.178.132.71:/home/ubuntu/

echo 'installing nginx'
sudo apt-get install nginx

echo 'connect to db and copy'
ssh ubuntu@35.178.132.71 'sudo cp -r /home/ubuntu/dynamic_website /var/www/html/dynamic_website; sudo apt-get update'
