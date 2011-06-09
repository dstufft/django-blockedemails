from setuptools import setup

setup(
    name = "django-blockedemails",
    version = __import__("blockedemails").__version__,
    author = "Donald Stufft",
    author_email = "donald@e.vilgeni.us",
    description = "A Django reusable app that provides a form field, models and validators for blocking email addresses",
    long_description = open("README.rst").read(),
    url = "http://github.com/dstufft/django-blockedemails/",
    license = "BSD",
    packages = [
        "blockedemails",
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Framework :: Django",
    ]
)
