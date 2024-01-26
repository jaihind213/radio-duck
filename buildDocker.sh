#!/bin/bash

PROJECT_VERSION=$1
DUCKDB_VERSION=$2
if [ "$PROJECT_VERSION" == "" ];then
  echo "PROJECT_VERSION not set as 1st argument. bash buildDocker.sh <version>  <duckdb_version>"
  exit 2
fi
if [ "$DUCKDB_VERSION" == "" ];then
  echo "DUCKDB_VERSION not set as 2nd argument. bash buildDocker.sh <project_version> <duckdb_version>"
  exit 2
fi
#####################
export IMAGE_NAME=jaihind213/radio-duck
export DOCKER_DUCKX_IMAGE_VERSION=$DUCKDB_VERSION-0.2
IMAGE_VERSION=${PROJECT_VERSION}-${DOCKER_DUCKX_IMAGE_VERSION}
PLATFORM=linux/x86_64,linux/amd64

PUSH_REPO=remote
if [ "$PUSH_REPO" == "local" ];then
  DOCKER_ARGS="--load" #or --output=type=docker both are same
else
  #push to remote
  DOCKER_ARGS="--output=type=registry"
fi

PUSH_LATEST_TAG="no"
if [ "$PUSH_LATEST_TAG" == "yes" ];then
  echo "setting latest tag..."
  LATEST_TAG = "-t $IMAGE_NAME:latest"
fi

cd "$(dirname "$0")"
echo "exporting poetry deps to requirements.txt..."
#easy to build docker image with python and install with pip. hence converting to requirements.txt :)
poetry export --without-hashes --format=requirements.txt > requirements.txt
echo "building docker image... with version $IMAGE_NAME:$IMAGE_VERSION"
echo "base duckdbX version: $DOCKER_DUCKX_IMAGE_VERSION ..."
echo "PUSH_REPO FLAG: $PUSH_REPO"
echo "PUSH_LATEST_TAG FLAG: $PUSH_LATEST_TAG"
sleep 10
export DOCKER_BUILDKIT=1
docker buildx build $DOCKER_ARGS --platform $PLATFORM --build-arg DOCKER_DUCKX_IMAGE_VERSION=${DOCKER_DUCKX_IMAGE_VERSION} -t  $IMAGE_NAME:$IMAGE_VERSION ${LATEST_TAG} .

#for Macs-m1
#docker buildx build --platform linux/x86_64 -t  $IMAGE_NAME:$PROJECT_VERSION -t $IMAGE_NAME:latest .
touch /tmp/version
cat /dev/null > /tmp/version
echo $IMAGE_VERSION > /tmp/version