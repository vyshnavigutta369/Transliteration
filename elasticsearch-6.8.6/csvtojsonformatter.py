#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import csv
import unicodedata, sys

def splitclusters(s):
    """Generate the grapheme clusters for the string s. (Not the full
    Unicode text segmentation algorithm, but probably good enough for
    Devanagari.)

    """
    virama = u'\N{DEVANAGARI SIGN VIRAMA}'
    cluster = u''
    last = None
    for c in s:
        cat = unicodedata.category(c)[0]
        if cat == 'M' or cat == 'L' and last == virama:
            cluster += c
        else:
            if cluster:
                yield cluster
            cluster = c
        last = c
    if cluster:
        yield cluster


with open('xlit_englishsource.csv','r') as r1,open('xlit_hindisource.csv','r') as r2,open('insertsourcewordsHin.json','w',encoding="utf-8") as w1:
    l1 = csv.reader(r1, delimiter=',')
    l2 = csv.reader(r2, delimiter=',')
    
    for i,(line1,line2) in enumerate(zip(l1,l2)):
        
        if (len(line2)==0):
            continue
        
        splitlist=list(splitclusters(line2[0]))

        base=''
        for chars in splitlist:
            base+=str(chars[0])

        w1.write('{ "index" : { "_index" : "xlit", "_type" : "words", "_id" :')
        w1.write(repr(i))
        w1.write('} }')
        w1.write('\n')
        w1.write('{ "Enscript" : "')
        w1.write(line1[0])
        w1.write('",')
        w1.write(' "base" : "')
        w1.write(base)
        w1.write('",')
        w1.write(' "Hiscript" : "')
        w1.write(line2[0])
        #print repr(line[0]).decode('utf-8')
        w1.write('" }')
        w1.write('\n')
     
