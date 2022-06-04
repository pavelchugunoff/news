#!/bin/bash

sleep 60

python3 news/manage.py migrate
python3 news/manage.py runserver 0.0.0.0:8000