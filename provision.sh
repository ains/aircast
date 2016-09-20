#!/usr/bin/env bash
#make sure the vagrant user is in the audio group
sudo usermod -a -G audio vagrant

#install the newest alsa kernel modules
sudo apt-add-repository ppa:ubuntu-audio-dev/alsa-daily
sudo apt-get update
sudo apt-get install oem-audio-hda-daily-dkms

#reload sound module
sudo modprobe snd-hda-intel

sudo apt-get install -yq git wget autoconf libtool libdaemon-dev libasound2-dev libpopt-dev libconfig-dev avahi-daemon libavahi-client-dev libssl-dev libsoxr-dev alsa-utils

#also do https://wiki.ubuntuusers.de/Soundkarten_konfigurieren/HDA?redirect=no
sudo apt-get -yq remove --purge alsa-base pulseaudio
sudo apt-get -yq install alsa-base pulseaudio
sudo alsa force-reload
echo "options snd-hda-intel model=3stack" | sudo tee -a /etc/modprobe.d/alsa-base.conf

#install shairport-sync
git clone --depth=1 https://github.com/mikebrady/shairport-sync.git
cd shairport-sync
autoreconf -i -f
./configure --with-alsa --with-avahi --with-ssl=openssl --with-metadata --with-soxr --with-stdout
make
sudo make install

#install python dependencies
sudo apt-get -yq install python-dev python-pip
sudo apt-get -yq install flac libflac-dev
sudo pip install -r /vagrant/requirements.txt

sudo apt-get -yq autoremove

# Install supervisor to auto start Aircast
sudo apt-get -yq install supervisor

cat | sudo tee /etc/supervisor/conf.d/aircast.conf > /dev/null <<- EOM
[program:aircast]
command=python /vagrant/main.py --iface=eth1
autostart=true
autorestart=true
stderr_logfile=/var/log/aircast.err.log
stdout_logfile=/var/log/aircast.out.log
username=vagrant
EOM

sudo service supervisor restart