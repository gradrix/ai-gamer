#!/bin/bash

docker stop game_server || (echo "Skipping.." && true)

docker rm game_server || (echo "Skipping.." && true)

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sudo rm -rf $root_dir/data/db/game_records.db