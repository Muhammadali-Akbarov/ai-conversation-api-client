#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Attempting to install Docker..."
    # Install Docker (this assumes a Debian-based system, adjust if needed)
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and log back in, then run this script again."
    exit 0
fi

# Pull and run the Docker image
echo "Pulling and running the Docker image..."
docker pull hlohaus789/g4f
docker run \
  -p 8080:8080 -p 1337:1337 -p 7900:7900 \
  --shm-size="2g" \
  -v ${PWD}/har_and_cookies:/app/har_and_cookies \
  -v ${PWD}/generated_images:/app/generated_images \
  -d \
  hlohaus789/g4f:latest

echo "Docker container is now running."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install requests

echo "Installation completed successfully!"
echo "To activate the virtual environment, run: source venv/bin/activate"
