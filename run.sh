#!/bin/bash

IMAGE_NAME=folder_uploader
CONTAINER_NAME=uploader_app
HOST_UPLOAD_PATH=$(pwd)/uploads
PORT=5000

echo "Creating upload folder if it doesn't exist..."
mkdir -p ${HOST_UPLOAD_PATH}

echo "Building Docker image..."
docker build -t ${IMAGE_NAME} .

echo "Running Docker container..."
docker run -d -p ${PORT}:5000 -v ${HOST_UPLOAD_PATH}:/app/uploads --name ${CONTAINER_NAME} ${IMAGE_NAME}

echo "Application is running at http://localhost:${PORT}"

