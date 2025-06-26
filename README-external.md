✅ 1. Build the Docker Image

docker build -t folder_uploader .

✅ 2. Create the Host Folder for Uploads

mkdir -p /absolute/path/on/host/uploads

example
mkdir -p /home/username/folder_uploads


✅ 3. Run the Docker Container with Volume Mapping

docker run -d -p 5000:5000 -v /absolute/path/on/host/uploads:/app/uploads --name uploader_app folder_uploader


/absolute/path/on/host/uploads with your local path (e.g., /home/username/folder_uploads)

✅ Example Command:

docker run -d -p 5000:5000 -v /home/username/folder_uploads:/app/uploads --name uploader_app folder_uploader


✅ 4. Access the App

http://localhost:5000


🚀 Optional: Using Docker Compose

version: '3'
services:
  uploader:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads


docker compose up -d

