#!/bin/bash

# running, debug mode is best used in development,
# false debug to run without the debugging
export FLASK_APP='run.py'
export FLASK_DEBUG='true'
# export FLASK_DEBUG='false'

flask run