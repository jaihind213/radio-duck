#!/usr/bin/env sh
#change internal version/duckdbversion
DUCKDB_VERSION=0.9.0
INTERNAL_VERSION=0.2
PUSH_REPO=remote
PLATFORM=linux/x86_64,linux/amd64
#linux/arm/v8
DUCK_AZURE_GITHUB_COMMIT=e4fb5a31dc8b014adeac990fb25cf549c7eba962
#######################################
export VERSION=${DUCKDB_VERSION}-${INTERNAL_VERSION}
export IMAGE_NAME=jaihind213/ubuntu-python3
export DUCK_IMAGE_NAME=jaihind213/duckdbx
#######################################


if [ "$PUSH_LOCAL_REPO" == "local" ];then
  DOCKER_ARGS="--load"
else
  #push to remote
  DOCKER_ARGS="--output=type=registry"
fi


export DOCKER_BUILDKIT=1

docker buildx build --platform $PLATFORM $DOCKER_ARGS -f DockerFileUbuntuPython3 -t  $IMAGE_NAME:$VERSION -t $IMAGE_NAME:latest .

docker buildx build --build-arg DUCK_AZURE_GITHUB_COMMIT=${DUCK_AZURE_GITHUB_COMMIT} --build-arg DUCKDB_VERSION=${DUCKDB_VERSION} --platform $PLATFORM $DOCKER_ARGS -f DockerFileDuckDb -t $DUCK_IMAGE_NAME:$VERSION -t $DUCK_IMAGE_NAME:latest .
