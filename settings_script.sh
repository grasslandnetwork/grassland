#!/bin/bash


source /usr/local/bin/virtualenvwrapper.sh

workon grassland

python python/get_settings.py 

# quit virtual environment
deactivate


exit 0
