#!/usr/bin/env bash

deactivate
rm -rf venv/

pip install virtualenv

python -m venv venv/
source venv/bin/activate

pip install -r requirements_dev.txt 

export FLASK_DEBUG=1
export FLASK_ENV=development 

(cd edc_ogc/ && python -m flask run )
