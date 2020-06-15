#!/bin/bash

#curl -s -XDELETE 'http://localhost:9200/hi_analyze'

touch xlit_Gglehindiquery.csv
touch xlit_Ggleref.csv

IFS=$'\r\n' GLOBIGNORE='*' command eval  'hisourcearray=($(cat xlit_hindisource.csv))'

i=0
while read -r line; do
	URL="https://inputtools.google.com/request?itc=hi-t-i0-und&num=5&cp=0&cs=0&ie=utf-8&oe=utf-8&app=demopage"
    IFS="," getcandidates=$(curl -s -G -XGET $URL --data-urlencode "text="$line | awk -F'[][]' '{print $5}' | tr -d \") arr=($getcandidates)
    qry1=$(echo "${arr[0]//\'/}" | awk '{$1=$1};1')
    qry2=$(echo "${arr[1]//\'/}" | awk '{$1=$1};1')
    qry3=$(echo "${arr[2]//\'/}" | awk '{$1=$1};1')
    qry4=$(echo "${arr[3]//\'/}" | awk '{$1=$1};1')
    qry5=$(echo "${arr[4]//\'/}" | awk '{$1=$1};1')
    echo "${qry1}" >> xlit_Gglehindiquery.csv
    if [[ "${qry2}" ]]; then 
    	echo "${qry2}"  >> xlit_Gglehindiquery.csv
    	echo "${qry3}"  >> xlit_Gglehindiquery.csv
    	echo "${qry4}"  >> xlit_Gglehindiquery.csv
    	echo "${qry5}"  >> xlit_Gglehindiquery.csv
    fi
    #echo "${line}","${hisourcearray[$i]}","${qry1}","${qry2}","${qry3}","${qry4}","${qry5}"
    echo "${line}","${hisourcearray[$i]}","${qry1}","${qry2}","${qry3}","${qry4}","${qry5}" >> xlit_Ggleref.csv
    ((i=i+1))
done < xlit_englishsource.csv

