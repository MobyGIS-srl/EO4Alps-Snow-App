#!/usr/bin/env bash

source keys # get SH_CLIENT_ID and SH_CLIENT_SECRET from file

if [ ! -d "venv" ] 
then
    echo "create venv" 
    
    pip install virtualenv

    python -m venv venv/
    
    source venv/bin/activate

    pip install -r requirements.txt 
fi
    
source venv/bin/activate

export FLASK_DEBUG=1
export FLASK_ENV=development 

(cd edc_ogc/ && flask run )
