#!/usr/bin/env bash

PIP_EXTRA_INDEX_URL=$(grep 'index-url' ~/.config/pip/pip.conf | sed 's/^.*=//' | tr -d ' ')

PORT=8585

docker build -t eo4alps-browser --build-arg PIP_EXTRA_INDEX_URL="$PIP_EXTRA_INDEX_URL" --build-arg PORT="$PORT" .

docker run eo4alps-browser
