#!/usr/bin/env bash
PROJECT_PATH="/home/ubuntu"
${PROJECT_PATH}/virtualenvs/prjenv/bin/pip3.6 install -r ${PROJECT_PATH}/invoiceapp/requirements.txt
${PROJECT_PATH}/invoiceapp/manage.py migrate
${PROJECT_PATH}/invoiceapp/manage.py collectstatic --noinput --verbosity=3
