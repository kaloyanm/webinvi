#!/usr/bin/env bash
cat >> ~/.bashrc <<EOL
export LC_CTYPE=en_US.UTF-8
export WORKON_HOME=$HOME/virtualenvs
export VIRTUALENVWRAPPER_PYTHON=`which python`
export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`
source `which virtualenvwrapper.sh`
workon prjenv
EOL

export WORKON_HOME=$HOME/virtualenvs
export VIRTUALENVWRAPPER_PYTHON=`which python`
export VIRTUALENVWRAPPER_VIRTUALENV=`which virtualenv`
source `which virtualenvwrapper.sh`
mkvirtualenv prjenv
