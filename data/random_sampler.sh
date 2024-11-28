#!/bin/bash

# Source and destination directories
src_dir="/home/roy/beaver_interface/data/Resume"
dest_dir="/home/roy/beaver_interface/data/temp"

# Check if destination directory exists, create it if it doesn't
if [ ! -d "$dest_dir" ]; then
  mkdir -p "$dest_dir"
fi

# Get a random sample of 100 files from the source directory
shuf -zn100 -e "$src_dir"/* | xargs -0 -I {} cp "{}" "$dest_dir"

# Print a message indicating completion
echo "100 random files copied to $dest_dir"
