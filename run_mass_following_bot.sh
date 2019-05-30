#!/usr/bin/env bash

sleep .$[ ( $RANDOM % 20 ) + 1 ]m

python3 run_mass_following_bot.py $1 $2 $3 $4 $5