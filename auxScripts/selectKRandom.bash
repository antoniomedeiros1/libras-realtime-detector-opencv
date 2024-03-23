#!/bin/bash

input_folder=$1
output_folder=$2
k=100

if [ $# -eq 0 ]; then
        echo "No arguments supplied"
        echo "First argument: input directory"
        echo "Second argument: output directory"
        echo "Third argument: (optional, default=$k): select k random images from each directory"
        exit
elif [ $# -eq 3 ]; then
        k=$3
fi

for folder in $input_folder/* ; do
    name=$(basename "$folder")
    files_to_copy=$(ls "$folder" | shuf | head -n "$k")

    mkdir -p "$output_folder/$name"

    # Loop through the randomly selected files and copy them to the output folder
    for file in $files_to_copy; do
        cp "$folder/$file" "$output_folder/$name/"
    done
    exit
done
