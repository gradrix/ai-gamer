#!/bin/bash

if [ $# -gt 0 ]; then
    agentName=$1
    python console_client/start-console-client.py "$agentName"
else
    python console_client/start-console-client.py
fi