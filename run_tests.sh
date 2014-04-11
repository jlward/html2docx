#! /bin/sh

RUN_TESTS='nosetests -v -v --with-coverage --cover-erase --cover-package=. html2docx'
echo $RUN_TESTS
$RUN_TESTS
