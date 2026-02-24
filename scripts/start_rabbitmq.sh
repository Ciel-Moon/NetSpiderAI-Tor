#!/bin/bash
# Start RabbitMQ server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
echo "RabbitMQ started"
