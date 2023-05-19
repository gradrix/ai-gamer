#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 [Agent Name]"
    exit 1
fi

agentName=$1
python app/start-random-client.py "$agentName"
