# Match

A web application that allows users to rank options, then assigns options to the users
based on those rankings (i.e., a house allocation problem).

# Usage

## Requirements

* flask==1.0.3
* flask-login==0.4.1
* flask-sqlalchemy==2.4.0
* flask-wtf==0.14.2
* itsdangerous==1.1.0
* jinja2==2.10.1
* ldap3==2.9.1
* markupsafe==1.1.1
* requests==2.28.1
* sqlalchemy==1.3.4
* werkzeug-0.16.1
* wtforms==3.0.1
* [Sortable](https://github.com/RubaXa/Sortable/)

# Configuration

## Installing Sortable

[Sortable](https://github.com/RubaXa/Sortable/) is used as a Git submodule. To initialize
the submodule after cloning the Match repository run:

```sh
git submodule init
git submodule update
```

## config.py

You'll also need to create a `config.py` file, which specifies details such as which
method to use to make allocations, how to post notifications of the winners, etc.
A sample configuration file can be found at `sample_config.py`.

## Starting the Server

Start the server with `run.py`. By default it will be accessible at `localhost:9999`. To
make the server world-accessible or for other options, see `run.py -h`.

If you're having trouble configuring your sever, I wrote a
[blog post](http://blog.spurll.com/2015/02/configuring-flask-uwsgi-and-nginx.html)
explaining how you can get Flask, uWSGI, and Nginx working together.

# Bugs and Feature Requests

## Feature Requests

None

## Known Bugs

None

# License Information

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

This work makes use of [Sortable](http://rubaxa.github.io/Sortable) by [Lebedev Konstantin](mailto:ibnRubaXa@gmail.com) for ranking, licensed under the MIT License.

Remember: [GitHub is not my CV.](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/)
