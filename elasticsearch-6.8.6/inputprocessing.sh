#!/bin/bash

#curl -s -XDELETE 'http://localhost:9200/hi_analyze'

declare -A xlit_sourcetohindi

while read -r line; do
	IFS=',' read -r -a array <<< $line
	sourceinEn=${array[0]}
        sourceinHi=${array[1]}
        xlit_sourcetohindi[$sourceinEn]=$sourceinHi
done < input.csv

touch xlit_englishsource.csv
rm xlit_englishsource.csv
touch xlit_englishsource.csv
touch xlit_hindisource.csv
rm xlit_hindisource.csv
touch xlit_hindisource.csv

for line in "${!xlit_sourcetohindi[@]}"; do
        echo $line | awk '{$1=$1};1' >> xlit_englishsource.csv
	echo ${xlit_sourcetohindi[$line]} | awk '{$1=$1};1' >> xlit_hindisource.csv
done
