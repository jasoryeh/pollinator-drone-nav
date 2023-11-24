#!/bin/bash

# run with source ./init.sh
#set -x

if [ ! -d ./venv ]; then
  echo "making venv in ./venv"
  python3 -m venv ./venv
  echo "activating venv"
  source ./venv/bin/activate
  echo "installing requirements.txt"
  pip install -r requirements.txt
  deactivate
fi

echo "activating into local venv"
source ./venv/bin/activate

