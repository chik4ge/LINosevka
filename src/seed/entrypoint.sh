#!/bin/bash
set -e

echo "==> Running: make build"
make build

echo "==> Copying artifacts to /work"
if [ -d "LINESeedJP/fonts/ttf" ]; then
    cp -r LINESeedJP/fonts/ttf/* /work/
fi

echo "==> Artifacts have been copied to /work"
