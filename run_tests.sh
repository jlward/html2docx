#! /bin/sh

nosetests -v -v --with-coverage --cover-erase --cover-package=html2docx html2docx && find -name '*.py' | xargs flake8
