Contents
========

* [Setup](#setup)
    * [Starting the server](#starting-the-server)
    * [Settings and manage\.py](#settings-and-managepy)
    * [Upgrading after a pull](#upgrading-after-a-pull)
* [Miscellaneous](#miscellaneous)
    * [Coding Conventions](#coding-conventions)

Setup
=====
To run the platform on your machine, you should use vagrant. Follow these
steps to set that up:

1. Download and install Docker (https://docs.docker.com/engine/installation/)
2. Open a terminal (or command prompt) in the repository folder. If you are on
   windows, you need to run this cmd with admin privileges.
4. Run `docker-compose up`.
5. Wait :). This might take up to 20 minutes. Meanwhile don't do anything
and let it finish


Once the setup is done, you will have a docker containers running. To start or stop the project run
`docker-compose start` or `docker-compose stop`.

Miscellaneous
=============

Coding Conventions
------------------
We use EditorConfig to maintain basic code styles (like intendation size).
Check the [official page](http://editorconfig.org/#download) for a plugin for
your editor.

### Python
We follow the [pep8 standart](https://www.python.org/dev/peps/pep-0008/).
Our docstrings follow the [Google styleguide]
(https://google.github.io/styleguide/pyguide.html#Comments).

You are required to run `flake8` over your code before you commit. See [here]
(https://flake8.readthedocs.org/en/latest/vcs.html) on how to install the git
hook and look for a plugin for your editor.

We organize our imports with [isort](https://github.com/timothycrosley/isort).

### Javascript
We use [eslint](http://eslint.org/) for style checks.