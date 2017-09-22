#!/usr/bin/env bash

PROJECT_NAME="webinvoices"
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
PROJECT_DIR=/home/vagrant/$PROJECT_NAME

# pdf server
(cd $PROJECT_DIR && git submodule init)
(cd $PROJECT_DIR && git submodule update)
(cd $PROJECT_DIR/external/html2pdf/ && npm install)

source $VIRTUALENV_DIR/bin/activate
pip install -r $PROJECT_DIR/requirements.txt
honcho run python $PROJECT_DIR/manage.py migrate
honcho run python $PROJECT_DIR/manage.py collectstatic --no-input
