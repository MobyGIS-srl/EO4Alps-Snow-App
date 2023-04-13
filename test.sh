#!/usr/bin/env bash

deactivate
rm -rf venv/

pip install virtualenv

python -m venv venv/
source venv/bin/activate

pip install -r requirements_new.txt 

(cd edc_ogc/ && python -m flask run)
