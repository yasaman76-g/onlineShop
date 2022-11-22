#!/bin/bash

echo "waiting for migrate"
python3 manage.py migrate

echo "run project"
python3 manage.py runserver 0.0.0.0:8000
