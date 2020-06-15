#!/bin/bash
touch xlit_DeepXlithindiqueryv4.csv
touch xlit_DeepXlitrefv4.csv

IFS=$'\r\n' GLOBIGNORE='*' command eval  'hisourcearray=($(cat xlit_hindisource.csv))'

i=0
while read -r line; do
    IFS=$'[,]' GLOBIGNORE='*' command eval  'arr=($(echo $line | python3 ../DeepTranslit-master/deeptranslit/script.py))'
    qry1=$(echo "${arr[1]//\'/}" | awk '{$1=$1};1')
    qry2=$(echo "${arr[2]//\'/}" | awk '{$1=$1};1')
    qry3=$(echo "${arr[3]//\'/}" | awk '{$1=$1};1')
    qry4=$(echo "${arr[4]//\'/}" | awk '{$1=$1};1')
    qry5=$(echo "${arr[5]//\'/}" | awk '{$1=$1};1')
    echo "${qry1}" >> xlit_DeepXlithindiqueryv4.csv 
    if [[ "${qry2}" ]]; then
        echo "${qry2}" >> xlit_DeepXlithindiqueryv4.csv
        echo "${qry3}" >> xlit_DeepXlithindiqueryv4.csv
        echo "${qry4}" >> xlit_DeepXlithindiqueryv4.csv
        echo "${qry5}" >> xlit_DeepXlithindiqueryv4.csv
    fi
    echo "${line}","${hisourcearray[$i]}","${qry1}","${qry2}","${qry3}","${qry4}","${qry5}" >> xlit_DeepXlitrefv4.csv
    ((i=i+1))
done < xlit_englishsource.csv

