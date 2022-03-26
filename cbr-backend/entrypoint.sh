#!/bin/bash
cd /app
flaskk db migrate
flask db upgrade
flask run -h 0.0.0.0
