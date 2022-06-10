#!/bin/bash


cp ../mundi/dist/code-de.bundle.js edc_ogc/static/
cp ../mundi/dist/d0866eb6b70f54ef7169.worker.js edc_ogc/static/

heroku container:login
heroku container:push web -a vast-cliffs-90167 --arg PIP_EXTRA_INDEX_URL='https://__token__:glpat-MqFzPDkhcxsuiZKiGCi9@gitlab.com/api/v4/projects/34222301/packages/pypi/simple'
heroku container:release web -a vast-cliffs-90167
heroku open -a vast-cliffs-90167


#heroku logs -a vast-cliffs-90167 --tail