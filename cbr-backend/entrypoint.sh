#!/bin/bash
cd /app
flaskk db migrate
flaskk db upgrade
flaskk run -h 0.0.0.0
