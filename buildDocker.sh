#!/bin/bash
cd "$(dirname "$0")"
echo "exporting poetry deps to requirements.txt..."
poetry export --without-hashes --format=requirements.txt > requirements.txt
echo "building docker image..."
docker build -t  jaihind213/radio-duck:1.0 -t jaihind213/radio-duck:latest .

#for Macs-m1
#docker buildx build --platform linux/x86_64 -t  jaihind213/radio-duck:1.0 -t jaihind213/radio-duck:latest .
