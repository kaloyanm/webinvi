Contents
========

* [Setup](#setup)
    * [Starting the server](#starting-the-server)
    * [Settings and manage\.py](#settings-and-managepy)
    * [Upgrading after a pull](#upgrading-after-a-pull)
* [Miscellaneous](#miscellaneous)
    * [Coding Conventions](#coding-conventions)
    * [Dummy data](#dummy-data)
* [Tests](#tests)
    * [Coverage](#coverage)
    * [Profiling](#profiling)

Setup
=====
To run the platform on your machine, you should use docker. Follow these
steps to set that up:

1. Download and install Docker (https://docs.docker.com/engine/installation/)
2. Open a terminal (or command prompt) in the repository folder. If you
are on windows, you need to run this cmd with admin privileges.
4. Run `docker-compose up`.
5. Wait :). This might take up to 20 minutes. Meanwhile don't do anything
and let it finish
6. Enter into the web container with `docker exec -it invoice bash` and
apply the migrations via `python src/manage.py migrate`
7. Create a default user to work with by calling `python src/manage.py createsuperuser`


Once the setup is done, you will have a docker containers running. To
start or stop the project run `docker-compose start` or `docker-compose stop`.

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

Dummy data
----------
The platform can generate dummy data for local testing. To seed the db with
dummy data, run `fm createdummydata`. The newly generated data will be
associated with the first admin account found in the database.


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
