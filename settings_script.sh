#!/bin/bash

cd python

source /usr/local/bin/virtualenvwrapper.sh

workon grassland

python get_settings.py 

# quit virtual environment
deactivate


exit 0
