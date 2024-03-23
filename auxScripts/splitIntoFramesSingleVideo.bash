#!/bin/bash

input_file=$1
output_dir=$2
out_h=250

if [ $# -eq 0 ]; then
	echo "No arguments supplied"
	echo "First argument: input file"
	echo "Second argument: output directory"
	echo "Third argument: (optional, default=$out_h): start cropping from height h"
	exit
elif [ $# -eq 3 ]; then
	out_h=$3
fi

mkdir -p "$output_dir"
ffmpeg -i "$input_file" -vf "scale=480:-1,crop=min(iw\,ih):min(iw\,ih):0:$out_h,setsar=1" "$output_dir/image-%03d.png"
