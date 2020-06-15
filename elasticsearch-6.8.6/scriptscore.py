#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv

sourcetocandidatesdict=dict()

sourcetoscoredict=dict()

weights=[0.4,0.3,0.2,0.07,0.03]

with open('xlit_DeepXlitrefv2.csv','r') as r1, open('DeepXlitfuzzymapsourcetoqueriesv2.csv','r') as r2,open('DeepXlitfuzzyscorev2.csv','a') as w1,open('xlit_englishsource.csv','r') as r3:
    l1 =csv.reader(r1)
    l2 =csv.reader(r2)
    l3 =csv.reader(r3)
    w2 = csv.writer(w1)
    for line in l1:
        key=line[0]
        line.remove(line[0])
        line.remove(line[0])
        #print (line)
        sourcetocandidatesdict[key]=line

    for line in l2:
        key=line[0]
        line.remove(line[0])
        line.remove(line[0])

        noofmatches=0
        totalnoofcandidates=len(sourcetocandidatesdict[key])
        for w in line:
            if w!='' and w in sourcetocandidatesdict[key]:
                ind=sourcetocandidatesdict[key].index(w)
                if ind==0:
                    noofmatches+=weights[0]
                elif ind==1:
                    noofmatches+=weights[1]
                elif ind==2:
                    noofmatches+=weights[2]
                elif ind==3:
                    noofmatches+=weights[3]
                elif ind==4:
                    noofmatches+=weights[4]

        row=[]
        row.append(noofmatches)
        #row.append(totalnoofcandidates)
        row.append(1)
        sourcetoscoredict[key]=row

    noofquerymatches=0
    noofqueries=0
    for line in l3:
        row=[]
        row.append(line[0])
        if (line[0] in sourcetoscoredict.keys()):
            row.append(sourcetoscoredict[line[0]][0])
            row.append(sourcetoscoredict[line[0]][1])
            noofquerymatches+=sourcetoscoredict[line[0]][0]
            noofqueries+=sourcetoscoredict[line[0]][1]
        else:
            #print (line[0])
            row.append(0)
            #row.append(len(sourcetocandidatesdict[line[0]]))
            row.append(1)
            #noofqueries+=len(sourcetocandidatesdict[line[0]]) 
            noofqueries+=1

        w2.writerow(row)
    print (float(noofquerymatches/noofqueries))

        

        
