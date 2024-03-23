#!/bin/bash

input_dir=$1

if [ $# -eq 0 ]; then
        echo "No arguments supplied"
        echo "First argument: input directory"
        exit
fi

echo -e "Directory\tSize\tNumber of contents"

du -hd 1 "$input_dir" | while read -r size dir; do 
	output=$(ls -l "$dir" | wc -l) 
	echo -e "$dir\t$size\t$((output-1))" 
done
