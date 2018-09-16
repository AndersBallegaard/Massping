#!/bin/sh

#Very simple system wide install for Massping 

#Right now it only works on ubuntu/debian based distros

#go to tmp working dir
cd /tmp


#update distro
echo Updating distro
sudo apt-get update -qy

#install python3
echo Installing python3
echo Python3.6+ required
sudo apt-get install -y python3


#download Massping
echo Installing massping
sudo apt-get install git -y
git clone https://github.com/AndersBallegaard/Massping.git
sudo mv Massping/massping.py /usr/local/bin/massping
rm -rf Massping

echo Install finished


