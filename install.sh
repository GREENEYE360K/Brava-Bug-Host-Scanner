#!/bin/bash

echo "Installing your script and dependencies..."

# Update the system (optional)
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip

# Clone your repository
git clone https://github.com/GREENEYE360K/Brava-Bug-Host-Scanner.git

# Navigate to the repository directory
cd Brava-Bug-Host-Scanner

# Install Python dependencies
pip3 install -r requirements.txt

echo "Installation complete! You can now use the script. using python main.py command
