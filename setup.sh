\#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Java (needed for Jenkins)
sudo apt install -y openjdk-17-jdk

# Install Jenkins
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Install Python + venv
sudo apt install -y python3 python3-pip python3-venv

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install app dependencies
pip install -r requirements.txt

# Run Flask app (background)
nohup python app.py &
