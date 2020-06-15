#!/bin/bash

#curl -s -XDELETE 'http://localhost:9200/xlit'

#bash inputprocessing.sh #alignement to english and hindi source files

# inserting source words
#curl -s -XPUT -H "Content-Type: application/json" http://localhost:9200/xlit --data-binary @mappingEnanalyzer.json >  /dev/null
#python3 csvtojsonformatter.py
#curl -s -XPOST "http://localhost:9200/_bulk" -H "Content-Type: application/json" --data-binary @insertsourcewordsHin.json

bash DeepXlitQryGen.sh #generate google xlit's query candidates CHANGE ACCORDINGLY

bash ESscoringonQueries.sh ##  CHANGE THE QUERY FILE IN THE SCRIPT
