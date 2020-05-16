#!/usr/bin/env bash

sudo apt update && sudo apt upgrade -y

sudo apt install python3 \
                 python3-dev \
                 python3-venv \
                 python3-sdl2

python3 -m venv env
. env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p images
