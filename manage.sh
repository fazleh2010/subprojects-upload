#!/bin/bash

CONTAINER_NAME="uploader_app"
IMAGE_NAME="uploader_image"

case "$1" in
    build)
        echo "Building Docker image..."
        docker build -t $IMAGE_NAME .
        ;;
    start)
        echo "Starting Docker container..."
        docker run -d --name $CONTAINER_NAME -p 5010:5010 -v "$(pwd)/uploads:/app/uploads" $IMAGE_NAME
        ;;
    stop)
        echo "Stopping Docker container..."
        docker stop $CONTAINER_NAME
        ;;
    remove)
        echo "Removing Docker container..."
        docker rm $CONTAINER_NAME
        ;;
    logs)
        echo "Displaying container logs..."
        docker logs -f $CONTAINER_NAME
        ;;
    restart)
        echo "Restarting Docker container..."
        docker restart $CONTAINER_NAME
        ;;
    status)
        docker ps -a | grep $CONTAINER_NAME
        ;;
    *)
        echo "Usage: $0 {build|start|stop|remove|logs|restart|status}"
        exit 1
esac

