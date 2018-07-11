#!/bin/sh

# Run the following in the command shell
# wget --no-check-certificate  https://raw.githubusercontent.com/mauricecyril/pidustsensor/master/install.sh
# chmod +x install.sh
# bash install.sh


# Install the Basic Packages and Infrastructure

echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Starting the install of Pi Dust Sensor...."
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Installing the Packages from Apt"
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"

# Upgrade and Install Packages
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade

# Install basic packages
# sudo apt-get -y install git zip unzip tar bzip2 nano byobu screen tmux

# Install PIGPIO
# sudo apt-get -y pigpio 

# Install Python related Packages
# python python-pip python-gpiozero python-pigpio ptyhon-django python-flask
# python3 python3-pip python3-gpiozero python3-pigpio python3-django python3-flask python3-pandas python3-pandas-lib python3-numpy python3-matplotlib

# Packages needed if a captive portal is needed:
# sudo apt-get -y install lighttpd dnsmasq isc-dhcp-server hostapd perl php-cgi avahi-daemon 

# Replace Sh with Bash [Optional]
# echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
# echo "Replace Sh with Bash"
# echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
#
# sudo rm /bin/sh
# sudo ln /bin/bash /bin/sh
# sudo chmod a+rw /bin/sh

# Prepare folder for pidustsensor
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Create a folder for the Pi Dust Sensor and Copy Script"
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
cd ~
mkdir pidustsensor

# Copy script from Github
cd ~/pidustsensor
wget --no-check-certificate https://raw.githubusercontent.com/mauricecyril/pidustsensor/master/pidustsensor.py

# Install startup jobs
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Installing the startup job & scripts at boot."
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"

# Add a new Crontab entry to start script on boot
# ( crontab -l ; echo "0 0 0 0 * /bin/true" ) | crontab -
# crontab -l | { cat; echo "0 0 0 0 0 some entry"; } | crontab -
# crontab -l lists the current crontab jobs, 
# cat prints it, 
# echo prints the new command 
# crontab - adds all the printed stuff into the crontab file. 
# You can see the effect by doing a new crontab -l.

# Set PiGPIO to start at boot and also start daemon now
# crontab -l | { cat; echo "@reboot /usr/bin/ & > /dev/null 2>&1"; } | crontab -
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# Start Python Script
crontab -l | { cat; echo "@reboot /usr/bin/python3 -H /home/pi/pidustsensor/pidustsensor.py & > /dev/null 2>&1"; } | crontab -


# Install UFW as firewall
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Setting Up Firewall"
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"

# Install ufw
sudo apt-get -y install ufw

# Setup default rules with incoming blocked
sudo ufw default allow outgoing
sudo ufw default deny incoming

# Update the incoming to allow DHCP(67 and 68) and DNS(53)
sudo ufw allow from any port 68 to any port 67 proto udp
sudo ufw allow to any port 67 proto udp
sudo ufw allow to any port 68 proto udp
sudo ufw allow 53
sudo ufw allow bootps
sudo ufw allow dnsmasq
sudo ufw allow dhclient
# sudo ufw allow domain


# Update the incoming to only allow SSH (22), HTTP (80), HTTPS (443)
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Enable firewall
sudo ufw --force enable

# Run the Script
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"
echo "Running the Script"
echo "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_"


# Incase PIGPIOD is not running run
sudo pigpiod
python3 /home/pi/pidustsensor/pidustsensor.py
