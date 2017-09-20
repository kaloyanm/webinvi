#!/usr/bin/env bash

PROJECT_NAME="webinvoices"
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
PROJECT_DIR=/home/vagrant/$PROJECT_NAME

source $VIRTUALENV_DIR/bin/activate
pip install -r $PROJECT_DIR/requirements.txt
python $PROJECT_DIR/manage.py migrate
python $PROJECT_DIR/manage.py collectstatic --no-input
