#!/bin/sh
sleep 5
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - "wallet.main:create_app('config.ProductionConfig')"
