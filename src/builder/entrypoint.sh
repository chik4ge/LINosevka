#!/bin/sh

if [ ! -d /fonts/out ]; then
    mkdir -p /fonts/out
fi

python build.py
