#!/bin/bash
# install python, virtualenv and ansible
# get directly from sources
git clone https://github.com/pypa/virtualenv.git
cd virtualenv
python2.7 virtualenv.py venv
cd venv/
source bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python2.7 get-pip.py
pip install ansible
