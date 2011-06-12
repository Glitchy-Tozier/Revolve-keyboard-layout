#!/bin/sh

# Get data from 100 random files from the linux kernel as korpus data

cat $(find /usr/src/linux/ | grep "\.[ch].*" | shuf | head -n 100 | xargs)
