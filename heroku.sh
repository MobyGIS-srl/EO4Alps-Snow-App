#!/bin/bash


heroku container:login

PIP_EXTRA_INDEX_URL=$(grep 'index-url' ~/.config/pip/pip.conf | sed 's/^.*=//' | tr -d ' ')
heroku container:push web -a vast-cliffs-90167 --arg PIP_EXTRA_INDEX_URL="$PIP_EXTRA_INDEX_URL"
heroku container:release web -a vast-cliffs-90167
heroku open -a vast-cliffs-90167


#heroku logs -a vast-cliffs-90167 --tail
