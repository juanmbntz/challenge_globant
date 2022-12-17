#!/bin/bash

export PROJECT=project_id
export REPO=Rest-API
export TAG=latest
export IMAGE_URI=gcr.io/$PROJECT/$REPO:$TAG

docker build . --tag $IMAGE_URI
docker push $IMAGE_URI