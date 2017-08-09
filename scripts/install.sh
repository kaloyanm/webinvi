#!/usr/bin/env bash
add-apt-repository ppa:fkrull/deadsnakes
add-apt-repository ppa:chris-lea/redis-server

# Base system
apt-get install -y python-software-properties
apt-get update
apt-get upgrade -y

apt-get install -y build-essential python3.6 python3.6-dev python3.6-examples htop links \
    python3-cffi python3-cryptography python3-simplejson python3-anyjson python3-psycopg2 python3-mysqldb python3-crypto \
    libffi-dev libssl-dev

# Basic Python
wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py && rm get-pip.py

pip3.6 install --upgrade pip
pip3.6 install virtualenv virtualenvwrapper

ln -s /usr/bin/python3.6 /usr/bin/python

# Database
PG_VERSION=9.5
APP_DB_USER=ubuntu
APP_DB_PASS=ubuntu
APP_DB_NAME=fakturi

PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"


apt-get install -y "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION" "postgresql-$PG_VERSION-postgis-2.1" "postgresql-server-dev-$PG_VERSION"
# Edit postgresql.conf to change listen address to '*':
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth:
echo "host    all             all             all                     md5" >> "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Restart so that all new config is loaded:
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

# NoceJS
curl -sL https://deb.nodesource.com/setup_8.x | bash -
apt-get install nodejs
npm install -g yarn webpack