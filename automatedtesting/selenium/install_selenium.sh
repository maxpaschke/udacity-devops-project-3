#!/bin/bash
sudo apt-get upgrade -y
sudo apt-get install unzip -y
sudo apt-get install -y chromium-browser
pip3 install selenium

chromium-browser --version