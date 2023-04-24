#!/bin/bash

sleep 30

# Application directory
dir_path="/home/setup"
if [ ! -d $dir_path ]; then
        echo CRITICAL ERROR: $dir_path does not exist
        exit
fi

serial=$(cat /proc/device-tree/serial-number)
echo -e "SERIAL_NUMBER="$serial > $dir_path/fedge-variables.env
chmod 777 $dir_path/fedge-variables.env

echo Downloading configuration files...
wget https://raw.githubusercontent.com/meontechno/edgedepyml/main/lulu/device_config.py -O $dir_path/device_config.py
sleep 10
chmod 777 $dir_path/device_config.py
wget https://raw.githubusercontent.com/meontechno/edgedepyml/main/lulu/dkart-docker-compose.yml -O $dir_path/docker-compose.yml
sleep 10
chmod 777 $dir_path/docker-compose.yml
wget https://raw.githubusercontent.com/meontechno/edgedepyml/main/lulu/items_mapping.py -O $dir_path/items_mapping.py
sleep 10
chmod 777 $dir_path/items_mapping.py
cred_dir="/home/.registry_cred"
if [ ! -d $cred_dir ]; then
        mkdir $cred_dir
        exit
fi
wget https://raw.githubusercontent.com/meontechno/edgedepyml/main/lulu/config.json -O $cred_dir/config.json
chmod 777 $cred_dir/config.json

var=$(python3 $dir_path/device_config.py)
echo $var
if [[ "$var" == "Login Succeeded"  ]]; then
        /usr/local/bin/docker-compose -f $dir_path/docker-compose.yml up -d
else
        echo CRITICAL/usr/local/bin/docker-compose ERROR: Unable to login to docker...
fi
