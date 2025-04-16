#!/bin/bash

# This script installs and configures MySQL

sudo apt-get update
sudo apt-get install -y mysql-server

# Start MySQL service
sudo systemctl start mysql

# Secure installation
sudo mysql_secure_installation <<EOF
y
$DB_PASSWORD
$DB_PASSWORD
y
y
y
y
EOF

# Create database and user
sudo mysql -u root -p$DB_PASSWORD <<EOF
CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
CREATE USER '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON ecommerce_analytics.* TO '$DB_USER'@'%';
FLUSH PRIVILEGES;
EOF

# Update MySQL config to allow external connections
sudo sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql

echo "MySQL setup complete"
