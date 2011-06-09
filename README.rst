Django BlockedEmails
====================

django-blockedemails is a reusable app that provides a form field,
validators, and models that check if an email is being blocked, or
is disposable/throwaway.

Installation
------------

You can install django-blockedemails with pip by typing::

    pip install django-blockedemails
    
Or with easy_install by typing::

    easy_install django-blockedemails
    
Or manually by downloading a tarball and typing::

    python setup.py install
    
Settings
--------

django-blockedemails adds 3 settings

    Specifies an API_KEY to use with http://www.block-disposable-email.com/::

        BLOCK_DISPOSABLE_EMAIL_API_KEY = "" # Defaults to None which disables this validator

    Specifies a different url to use for the block-disposable-email.com api::

        BLOCK_DISPOSABLE_EMAIL_URL = "" # Will be string formated with a dictionary with api_key and domain

    Specifies if we should block an email if an exception occurs trying to check block-disposable-email.com::

        BLOCK_EMAIL_ON_URLERROR = False # Defaults to False

Usage
-----

    To use the formfield simply import it and use it::

        from django import forms
        from blockedemails.fields import EmailField

        class ExampleForm(forms.Form):
            email = EmailField()
