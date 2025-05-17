#!/bin/bash

set -e  # Exit if any command fails

echo "========== Updating System =========="
sudo apt update -y
sudo apt upgrade -y

# ----------------------
# AWS CLI INSTALLATION
# ----------------------
echo "========== Installing AWS CLI =========="
sudo apt install unzip curl -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -o awscliv2.zip
sudo ./aws/install
aws --version

# ----------------------
# DOCKER INSTALLATION
# ----------------------
echo "========== Installing Docker =========="
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

sudo systemctl start docker
sudo systemctl enable docker
docker --version

# Allow current user to use docker without sudo
sudo usermod -aG docker $USER

# ----------------------
# JENKINS INSTALLATION
# ----------------------
echo "========== Installing Jenkins =========="
sudo apt install openjdk-17-jdk -y
java -version

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install jenkins -y

# Optional: add user to jenkins group
sudo usermod -aG jenkins $USER

sudo systemctl start jenkins
sudo systemctl enable jenkins

echo "========== Setup Complete =========="
echo "You may need to log out and log back in for group changes to take effect."
