#!/bin/bash
# Install Tor on Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y tor
sudo systemctl enable tor
sudo systemctl start tor
echo "Tor installed and running on port 9050"
