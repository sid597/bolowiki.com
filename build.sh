#!/bin/bash

# Inside server
git pull
source venv/bin/activate
sudo pip3 install -r requirements.txt
sudo systemctl restart flaskapp
sudo systemctl restart nginx

