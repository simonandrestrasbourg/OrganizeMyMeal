**************
OrganizeMyMeal
**************

The easy way to organize your meal #remoteworking

Installation guide
##################

Install virtualenv and dependency
*********************************

Prerequisites
=============

* Have Postgresql installed locally with peer authentification on 127.0.0.1:5432
* Have linux distribution with libpq-dev python3 python3-dev postgresql

Installation guide
==================

.. code-block:: sh

    python -m venv django-env
    cd django-env
    source bin/activate
    git clone https://github.com/simonandrestrasbourg/OrganizeMyMeal.git
    cd OrganizeMyMeal
    pip3 install -r OrganizeMyMeal/requirements.txt
    createdb organizemymeal 
    python manage.py migrate 
    python manage.py createsuperuser
    python manage.py loaddata ingredients/fixtures/ingredients_fixture.json
    python manage.py runserver
