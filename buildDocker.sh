#!/bin/bash

VERSION=$1
export IMAGE_NAME=jaihind213/radio-duck

if [ "$VERSION" == "" ];then
  echo "VERSION not set as 1st argument. bash buildDocker.sh <version>"
  exit 2
fi
export VERSION

cd "$(dirname "$0")"
echo "exporting poetry deps to requirements.txt..."
#easy to build docker image with python and install with pip. hence converting to requirements.txt :)
poetry export --without-hashes --format=requirements.txt > requirements.txt
echo "building docker image..."
docker build -t  $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .

#for Macs-m1
#docker buildx build --platform linux/x86_64 -t  $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .
