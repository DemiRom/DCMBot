#!/bin/bash

cp example.env .env

python3 -m venv ./.venv
source .venv/bin/activate
pip3 install -r requirements.txt