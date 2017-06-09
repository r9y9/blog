#!/bin/bash

set -e

SCRIPT_DIR=$(cd $(dirname $0);pwd)
cd $SCRIPT_DIR/..

echo "Generating website by hugo..."
time hugo
cd public
mv index.xml atom.xml
cd -

echo "Finished!"
echo "Please commit and push to Github manually at the public directory."
