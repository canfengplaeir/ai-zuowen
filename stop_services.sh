#!/bin/bash

echo "Stopping backend service..."
pkill -f gunicorn

echo "Stopping Nginx..."
sudo systemctl stop nginx

echo "Services stopped successfully!" 