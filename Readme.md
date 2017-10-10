Contents
========

* [Setup](#setup)
    * [Starting the server](#starting-the-server)
* [Miscellaneous](#miscellaneous)
    * [Coding Conventions](#coding-conventions)
* [Development](#daytoday)
    * [Dummy data](#dummy-data)
    * [Translations](#translations)
    * [Emails](#emails)
* [Tests](#tests)
    * [Coverage](#coverage)
    * [Profiling](#profiling)

Setup
=====

Starting the server
-------------------

To run the platform on your machine, you should use Vagrant. Follow these
steps to set that up:

1. Download and install Vagrant (https://www.vagrantup.com/downloads.html).
2. Open a terminal (or command prompt) in the repository folder. If you
are on windows, you need to run this cmd with admin privileges.
4. Run `vagrant up`.
5. Wait :). This might take up to 20 minutes. Meanwhile don't do anything
and let it finish
6. Enter into the container with `vagrant ssh`. You will find a folder named `webinvoices`. This is your project root's
directory. To run the application go inside `webinvoices` and run `honcho start`.
7. Create a default user to work with by calling `./manage.py createsuperuser`

Once the setup is done, you will have a vagrant container running. To
start or stop the project run `vagrant up` or `vagrant halt`.

Miscellaneous
=============

Coding Conventions
------------------
We use EditorConfig to maintain basic code styles (like intendation size).
Check the [official page](http://editorconfig.org/#download) for a plugin for
your editor.

### Python
We follow the [pep8 standart](https://www.python.org/dev/peps/pep-0008/).
Our docstrings follow the [Google styleguide](https://google.github.io/styleguide/pyguide.html#Comments).

You are required to run `flake8` over your code before you commit. See [here](https://flake8.readthedocs.org/en/latest/vcs.html) on how to install the git
hook and look for a plugin for your editor.

We organize our imports with [isort](https://github.com/timothycrosley/isort).

### Javascript
We use [eslint](http://eslint.org/) for style checks.



Development
===========

Dummy data
----------
The platform can generate dummy data for local testing. To seed the db with
dummy data, run `./manage.py createdummydata`. This will produce 10 companies each one associated with 50 invoices. Each company is associated with one account. All users accounts have the following form:

    username: user[n]@demo.com
    password: test1234

Where *n* any number from 1 to 10.

Translations
------------

Once the string literals of an application have been tagged for later translation, the translation themselves need to be written (or obtained). Here’s how that works.

1. The first step is to create a message file for a new language.

    `django-admin makemessages -l en`

2. We use *django-rosetta* to edit the translations. In order to see them go to ``http://yourdomain.com/rosetta/``. Don't forget to log in into the admin beforehand.

3. After you create and edit your message file – and each time you make changes to it – you’ll need to compile it into a more efficient form, for use by gettext. Do this with the django-admin compilemessages utility.

    `django-admin compilemessages`

That’s it. Your translations are ready for use.

Emails
-----
The project uses **mailhog** to capture all outbound emails. Just open `http://182.16.0.5:8025/` to see them.


Google Drive integration for development
----------------------------------------

1. Make sure you have the following line in /etc/hosts

    182.16.0.5 webinvoices-local.dev

2. Make sure you have webinvoices-local.dev present in the allowed URLS when creating client_secrets.json in google console.


Deployment
==========

## Configuration
Configuration is stored in ansible inventory under ansible/inventory dir and the template for production config is in ansible/inventory/productionenv. Edit ansible/inventory/productionenv and ansible/inventory/group_vars/default.yml with the correct setting.

NOTE: Do not change the value of **deploy_in_vagrant**, it must be false.

## First time install:

```shell
cd ansible
ansible-playbook -i inventory/hosts install_web_app.yml
ansible-playbook -i inventory/hosts create_database.yml
ansible-playbook -i inventory/hosts html2pdf.yml
ansible-playbook -i inventory/hosts web_app.yml
```

## Deploy changes

```shell
cd ansible
ansible-playbook -i inventory/hosts web_app.yml
```


Tests
=====
Use this command to run the tests:
```
py.test -l
```
As long as the database did not change, you can leave out the --create-db on
following runs.


Coverage
--------
You can generate an HTML test coverage report like this:
```
py.test --cov=. --cov-report html
```
The coverage wil be in the `build/htmlcov` folder.

Profiling
---------
Simple profile middleware to profile django views. To run it, add ?prof to
the URL like this: http://localhost:8000/view/?prof.

Optionally pass the following to modify the output:

    ?sort => Sort the output by a given metric. Default is time.
        See http://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
        for all sort options.
    ?count => The number of rows to display. Default is 100.
    ?download => Download profile file suitable for visualization. For example in
        snakeviz or RunSnakeRun

    This is adapted from an example found here:
    http://www.slideshare.net/zeeg/django-con-high-performance-django-presentation.
