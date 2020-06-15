#!/bin/bash

IFS=$'\r\n' GLOBIGNORE='*' command eval  'arr=($(cat xlit_DeepXlithindiqueryv2.csv))' ## CHANGE FILE NAME ACCORDINGLY

touch DeepXlitfuzzymapsourcetoqueriesv2.csv
touch queryHin.json
rm queryHin.json

chunksize=520

for((j=0; j < ${#arr[@]}; j+=chunksize))
do

  touch queryHin.json
  echo '{' >> queryHin.json
  echo '"query": {' >> queryHin.json
  echo '"bool": {' >> queryHin.json
  echo '"should": [' >> queryHin.json

  part=( "${arr[@]:j:chunksize}" )
  size=${#part[@]}
  for((i=0; i < ${#part[@]}; i+=1))
  do
        echo '{' >> queryHin.json
        echo '"multi_match": {' >> queryHin.json
        echo '"query": "'${part[$i]}'",' >> queryHin.json
        echo '"_name": "'${part[$i]}'",' >> queryHin.json
        echo '"fuzziness": "AUTO",' >> queryHin.json
        echo '"operator":  "and",' >> queryHin.json
	echo '"fields": [ "Hiscript^2", "base" ],' >> queryHin.json
	echo '"type":  "most_fields"' >> queryHin.json
        echo '}' >> queryHin.json
        echo '}' >> queryHin.json
        if [ $i -lt $((size-1)) ]
        then
            echo ',' >> queryHin.json
        fi
   done

   echo ']' >> queryHin.json
   echo '}' >> queryHin.json
   echo '}' >> queryHin.json
   echo '}' >> queryHin.json
  #echo "Elements in this group: ${#part[*]}"
   IFS=$'\r\n' GLOBIGNORE='*' command eval  'invrsemappng=($(curl -XGET "http://localhost:9200/xlit/words/_search?size=120" -H "Content-Type: application/json" -d @queryHin.json | jq -r "(.hits.hits[] | [._source.Enscript,._source.Hiscript,.matched_queries[]]) | @sh"))'
   declare -A dictmappings
   #echo ${#invrsemappng[@]}
   for((i=0; i < ${#invrsemappng[@]}; i+=1))
   do
           IFS=$'\r\n' GLOBIGNORE='*' command eval  'tup=($( for word in '${invrsemappng[$i]}'; do echo $word; done))'

           if [[ ${dictmappings[${tup[0]}]} ]];
           then
                for((k=2; k < ${#tup[@]}; k+=1))
                do
                        dictmappings[${tup[0]}]="${dictmappings[${tup[0]}]}${dictmappings[${tup[0]}]:+,}${tup[$k]}"
                done
           else
                for((k=1; k < ${#tup[@]}; k+=1))
                do
                        dictmappings[${tup[0]}]="${dictmappings[${tup[0]}]}${dictmappings[${tup[0]}]:+,}${tup[$k]}"
                done
            fi

   done
   #break
   mv queryHin.json DeepXlitqueryHinv2.json
done


for key in "${!dictmappings[@]}"; do
    echo -n $key"," >> DeepXlitfuzzymapsourcetoqueriesv2.csv
    IFS=',' read -ra mappings <<< "${dictmappings[$key]}"
    for k in "${mappings[@]}"; do
    	echo -n $k"," >> DeepXlitfuzzymapsourcetoqueriesv2.csv
    done
    echo >> DeepXlitfuzzymapsourcetoqueriesv2.csv
done

python3 scriptscore.py ## CHANGE REFERENCE FILES ACCORDINGLY 
