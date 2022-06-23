#!/bin/bash


cp ../mundi/dist/code-de.bundle.js edc_ogc/static/
cp ../mundi/dist/d0866eb6b70f54ef7169.worker.js edc_ogc/static/

heroku container:login

PIP_EXTRA_INDEX_URL=$(grep 'index-url' ~/.config/pip/pip.conf | sed 's/^.*=//' | tr -d ' ')
heroku container:push web -a vast-cliffs-90167 --arg PIP_EXTRA_INDEX_URL="$PIP_EXTRA_INDEX_URL"
heroku container:release web -a vast-cliffs-90167
heroku open -a vast-cliffs-90167


#heroku logs -a vast-cliffs-90167 --tail