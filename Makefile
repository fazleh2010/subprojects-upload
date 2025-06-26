# Variables
IMAGE_NAME=folder_uploader
CONTAINER_NAME=uploader_app
HOST_UPLOAD_PATH=$(CURDIR)/uploads
PORT=5000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container with volume mapping
run:
	mkdir -p $(HOST_UPLOAD_PATH)
	docker run -d -p $(PORT):5000 -v $(HOST_UPLOAD_PATH):/app/uploads --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop the container
stop:
	docker stop $(CONTAINER_NAME)

# Start the container
start:
	docker start $(CONTAINER_NAME)

# Remove the container
remove:
	docker rm -f $(CONTAINER_NAME)

# Show logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Clean everything
clean: stop remove
	docker rmi $(IMAGE_NAME)
	rm -rf $(HOST_UPLOAD_PATH)

# Help
help:
	@echo "Usage:"
	@echo "  make build    - Build the Docker image"
	@echo "  make run      - Run the container"
	@echo "  make stop     - Stop the container"
	@echo "  make start    - Start the container"
	@echo "  make remove   - Remove the container"
	@echo "  make logs     - Show container logs"
	@echo "  make clean    - Stop, remove container, delete image and uploads folder"

