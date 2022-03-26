#!/bin/bash
cd /app
flask db migrate
flask db upgrade
flaskk run -h 0.0.0.0
