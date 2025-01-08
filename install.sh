#!/bin/bash

# Update and upgrade Termux packages
echo "[*] Updating Termux repositories..."
pkg update -y
pkg upgrade -y

# Install required dependencies
echo "[*] Installing required dependencies..."
pkg install -y python
pkg install -y git
pkg install -y curl
pkg install -y clang
pkg install -y make

# Install Python packages from requirements.txt (if available)
if [ -f "requirements.txt" ]; then
    echo "[*] Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "[*] No requirements.txt file found."
fi

# Clone the repository
echo "[*] Cloning the repository..."
git clone https://github.com/GREENEYE360K/Brava-Bug-Host-Scanner.git

# Navigate to the project folder
cd Brava-Bug-Host-Scanner

# Instructions for user
echo "[*] Installation complete!"
echo "[*] You can now run the project using the command: python3 your_script.py"
