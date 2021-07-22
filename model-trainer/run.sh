#!/bin/bash

cd /mnt/c/"$2"/uploads
python3 -m venv env
activate () {
  . ./env/bin/activate
}
activate
pip3 install -r requirements.txt
echo $(which python3)
python3 "$1"
echo "trained"