# upload folder

Upload subprojects data
# subprojects-upload
chmod +x run.sh


# When running the system for upload data outside doocker container. 
## 1. Build the Docker Image

docker build -t folder_uploader .

## 2. Create the Host Folder for Uploads

mkdir -p /absolute/path/on/host/uploads

example
mkdir -p /home/username/folder_uploads


## 3. Run the Docker Container with Volume Mapping

docker run -d -p 5010:5010 -v /absolute/path/on/host/uploads:/app/uploads --name uploader_app folder_uploader


## Example Command:
docker run -d -p 5010:5010 -v /home/melahi/code/uploads:/app/uploads --name uploader_app folder_uploader


## 4. Access the App

http://localhost:5010


# When running the system for upload data inside doocker container. 

## 1. change access
chmod +x manage.sh

## 2. run command
./manage.sh stop       # Stop the container
./manage.sh build      # Build the image
./manage.sh start      # Start the container

## 3. all options command
./manage.sh build      # Build the image
./manage.sh start      # Start the container
./manage.sh stop       # Stop the container
./manage.sh remove     # Remove the container
./manage.sh logs       # Show logs
./manage.sh restart    # Restart the container
./manage.sh status     # Check if running

## 4. Access the App
http://localhost:5000


