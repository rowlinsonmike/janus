#!/bin/bash

# Run the build command
uv build

# Find the source file matching the pattern
SOURCE_FILE=$(ls dist/janus-*.tar.gz)
WHL_FILE=$(ls dist/janus-*.whl)

# Define the destination file path
DEST_FILE="dist/janus.tar.gz"

# Check if the source file exists and rename it, overwriting if it already exists
if [ -f "$SOURCE_FILE" ]; then
  mv -f "$SOURCE_FILE" "$DEST_FILE"
  rm "$WHL_FILE"
else
  echo "Source file not found."
fi