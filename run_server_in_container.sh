#!/bin/bash

docker build -t game_server -f ./app/game_server/Dockerfile .

docker run game_server