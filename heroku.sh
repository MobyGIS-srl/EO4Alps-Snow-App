#!/bin/bash


cp ../mundi/dist/code-de.bundle.js edc_ogc/static/
cp ../mundi/dist/d0866eb6b70f54ef7169.worker.js edc_ogc/static/

heroku container:login
heroku container:push web -a vast-cliffs-90167
heroku container:release web -a vast-cliffs-90167
heroku open -a vast-cliffs-90167


#heroku logs -a vast-cliffs-90167 --tail