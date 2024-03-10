#!/bin/bash

PROJECT_VERSION=$1
DUCKDB_VERSION=$2
PUSH_REPO=$3
PUSH_LATEST_TAG=$4

if [ "$PROJECT_VERSION" == "" ];then
  echo "PROJECT_VERSION not set as 1st argument. bash buildDocker.sh <version>  <duckdb_version>"
  exit 2
fi
if [ "$DUCKDB_VERSION" == "" ];then
  echo "DUCKDB_VERSION not set as 2nd argument. bash buildDocker.sh <project_version> <duckdb_version>"
  exit 2
fi
if [ "$PYTHON_VERSION" == "" ];then
  PYTHON_VERSION=3.10
fi
if [ "$DOCKERFILE_VERSION" == "" ];then
  DOCKERFILE_VERSION=0.1
fi
#####################
export IMAGE_NAME=jaihind213/radio-duck
export IMAGE_VERSION="d${DUCKDB_VERSION}-v${PROJECT_VERSION}-$DOCKERFILE_VERSION"
PLATFORM=linux/amd64

if [ "$PUSH_REPO" == "remote" ];then
  DOCKER_ARGS="--output=type=registry"
else
  DOCKER_ARGS="--load" #or --output=type=docker both are same
fi

TAGS="-t $IMAGE_NAME:$IMAGE_VERSION"
if [ "$PUSH_LATEST_TAG" == "yes" ];then
  echo "setting latest tag..."
  TAGS = "$TAGS -t $IMAGE_NAME:latest"
fi

cd "$(dirname "$0")"
echo "exporting poetry deps to requirements.txt..."
#easy to build docker image with python and install with pip. hence converting to requirements.txt :)
poetry export --without-hashes --format=requirements.txt > requirements.txt

echo "building docker image... with version $IMAGE_NAME:$IMAGE_VERSION"
echo "PUSH_REPO FLAG: $PUSH_REPO"
echo "TAGS: $TAGS"
echo "PUSH_LATEST_TAG FLAG: $PUSH_LATEST_TAG"
echo "PYTHON_VERSION FLAG: $PYTHON_VERSION"

sleep 5
export DOCKER_BUILDKIT=1
docker buildx build $DOCKER_ARGS --build-arg PYTHON_VERSION=${PYTHON_VERSION} --platform $PLATFORM $TAGS .

touch /tmp/version
cat /dev/null > /tmp/version
echo $IMAGE_VERSION > /tmp/version