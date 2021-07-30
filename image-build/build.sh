#!/usr/bin/bash
echo "BASE IMAGE:  $1"
echo "BUILD CONTEXT: $2"
echo "TAGGED: $3"
docker build --tag "$3" -f ./Dockerfile --build-arg BASE_IMAGE="$1" "$2"