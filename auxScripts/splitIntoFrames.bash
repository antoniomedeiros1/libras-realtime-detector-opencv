#!/bin/bash

input_dir=$1
output_dir=$2
out_h=250

if [ $# -eq 0 ]; then
        echo "No arguments supplied"
        echo "First argument: input directory of videos"
        echo "Second argument: output directory of images"
        echo "Third argument: (optional, default=$out_h): start cropping from height h"
	exit
elif [ $# -eq 3 ]; then
        out_h=$3
fi

for fullfile in $input_dir/* ; do
	file=$(basename -- "$fullfile")
	name="${file%.*}"
	mkdir -p "$output_dir/$name"
        ffmpeg -i "$fullfile" -vf "scale=480:-1,crop=min(iw\,ih):min(iw\,ih),setsar=1" "$output_dir/$name/image-%03d.png"
done
