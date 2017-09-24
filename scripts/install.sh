#!/usr/bin/env bash

# base system
add-apt-repository ppa:fkrull/deadsnakes
add-apt-repository ppa:chris-lea/redis-server

apt-get install -y python-software-properties
apt-get update

apt-get install -y build-essential python3.6 python3.6-dev python3.6-examples htop links \
    python3-cffi python3-cryptography python3-simplejson python3-anyjson python3-psycopg2 python3-mysqldb python3-crypto \
    libffi-dev libssl-dev libfontconfig1 redis-server gettext

# python
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py && rm get-pip.py

pip3.6 install --upgrade pip
pip3.6 install virtualenv virtualenvwrapper stevedore virtualenv-clone


# setup
PROJECT_NAME="webinvoices"
DB_NAME="fakturi"
PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

# virtualenv for project
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR --python=/usr/bin/python3.6 && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"

echo "alias honcho='honcho -e $PROJECT_DIR/.myenv -f $PROJECT_DIR/Procfile.dev'" >> /home/vagrant/.bashrc
echo ". $VIRTUALENV_DIR/bin/activate" >> /home/vagrant/.bashrc

## set execute permissions on manage.py, as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py

# postgresql
PG_VERSION=9.5
APP_DB_USER=vagrant
APP_DB_PASS=vagrant
APP_DB_NAME=fakturi

apt-get install -y "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# restart so that all new config is loaded:
service postgresql restart

cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $APP_DB_USER WITH SUPERUSER PASSWORD '$APP_DB_PASS';

-- Create the database:
CREATE DATABASE $APP_DB_NAME WITH OWNER=$APP_DB_USER
                                  LC_COLLATE='en_US.utf8'
                                  LC_CTYPE='en_US.utf8'
                                  ENCODING='UTF8'
                                  TEMPLATE=template0;
EOF

# NodeJS
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt-get install nodejs
npm install -g yarn webpack
