#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from deeptranslit import DeepTranslit
import csv

transliterator = DeepTranslit('hindi')

'''
WordsandScores=list(transliterator.transliterate(input("Enter word: ")))

Top5=[]

for tup in WordsandScores:
	Top5.append(tup[0])

print (Top5)
'''
with open('xlit_movies_syll','r') as r1:
     l1 = csv.reader(r1, delimiter=',')
     l1= r1.readlines()
     for i,line in enumerate(l1):
         line=line.rstrip('\n')
         top5=list(transliterator.transliterate(line))
         print (top5[0][0])


