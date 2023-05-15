#!/usr/bin/env bash

PIP_EXTRA_INDEX_URL=$(grep 'index-url' ~/.config/pip/pip.conf | sed 's/^.*=//' | tr -d ' ')

docker build -t eo4alps-browser --build-arg PIP_EXTRA_INDEX_URL="$PIP_EXTRA_INDEX_URL" .

# docker run --env PORT=$PORT eo4alps-browser

tag=$(docker images | awk '{print $3}' | awk 'NR==2')

docker tag $tag ghcr.io/mobygis-srl/docker-registry/eo4alps-browser:0.1.4

# docker push ghcr.io/mobygis-srl/docker-registry/eo4alps-browser:0.1.4 &

docker-compose up -d

docker-compose logs
