#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker and try again."
    echo "Visit https://docs.docker.com/get-docker/ for installation instructions."
    exit 1
fi

# Pull and run the Docker image
echo "Pulling and running the Docker image..."
docker pull hlohaus789/g4f
docker run \
  -p 8080:8080 -p 1337:1337 -p 7900:7900 \
  --shm-size="2g" \
  -v "${PWD}/har_and_cookies:/app/har_and_cookies" \
  -v "${PWD}/generated_images:/app/generated_images" \
  -d \
  --name g4f_container \
  hlohaus789/g4f:latest

echo "Docker container 'g4f_container' is now running."

# Check if Python is installed
if ! command_exists python3 && ! command_exists python; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Use python or python3 command based on availability
PYTHON_CMD=$(command_exists python3 && echo "python3" || echo "python")

# Check if pip is installed
if ! command_exists pip3 && ! command_exists pip; then
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

# Use pip or pip3 command based on availability
PIP_CMD=$(command_exists pip3 && echo "pip3" || echo "pip")

# Create a virtual environment
$PYTHON_CMD -m venv venv

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
$PIP_CMD install --upgrade pip

# Install the required packages
$PIP_CMD install requests

echo "Installation completed successfully!"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "To activate the virtual environment, run: venv\\Scripts\\activate"
else
    echo "To activate the virtual environment, run: source venv/bin/activate"
fi
