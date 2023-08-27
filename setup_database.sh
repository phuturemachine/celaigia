#!/bin/bash

# Prompt for MySQL details
read -p "Enter MySQL database name [default: celagia]: " DB_NAME
DB_NAME=${DB_NAME:-celagia}  # Default to celagia if nothing is entered

read -p "Enter your MySQL username: " DB_USER
read -s -p "Enter your MySQL password: " DB_PASS
echo

# Save environment variables to user's bash profile
echo "export CELAIGIA_DB_NAME=$DB_NAME" >> ~/.bashrc
echo "export CELAIGIA_USER=$DB_USER" >> ~/.bashrc
echo "export CELAIGIA_PASSWORD=$DB_PASS" >> ~/.bashrc
source ~/.bashrc

# Create database and table
mysql -u$DB_USER -p$DB_PASS -e "CREATE DATABASE IF NOT EXISTS $DB_NAME; USE $DB_NAME; CREATE TABLE IF NOT EXISTS download_logs (id INT AUTO_INCREMENT PRIMARY KEY, video_title VARCHAR(255) NOT NULL, video_url VARCHAR(512) NOT NULL, video_query VARCHAR(255) NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);"

echo "Database setup complete!"
