from __future__ import unicode_literals  # for python2 compatibility
# -*- coding: utf-8 -*-
# encoding: utf-8
# created at UC Berkeley 2015
# Authors: Christopher Hench & Alex Estes © 2015-2019

import codecs
import sys
from syllabipy.util import cleantext
from datetime import datetime
import unicodedata
import math

def SonoriPy(word, IPA=False, lang='en'):
    '''
    This program syllabifies words based on the Sonority Sequencing Principle (SSP)

    >>> SonoriPy("justification")
    ['jus', 'ti', 'fi', 'ca', 'tion']
    '''
    
    def no_syll_no_vowel(ss):
        '''
        cannot be a syllable without a vowel
        '''

        nss = []
        front = ""
        #print (len(ss))
        for i, syll in enumerate(ss):
            # if following syllable doesn't have vowel,
            # add it to the current one
            if syll==" ":
                #print ("0 ",i)
                if front!="":
                    nss.append(front)
                    front = ""
                nss.append(syll)
            elif lang=="en" and ((len(nss)>0 and len(nss[-1])==1 and nss[-1].isalpha() and nss[-1] not in vowels) or not any(char in vowels for char in syll)) :
                #print ("1 ",i)
                if len(nss) == 0:
                    front += syll
                elif nss[-1]!=" ":
                    nss = nss[:-1] + [nss[-1] + syll]
                else:
                    nss.append(syll)
            #elif lang=="hin" and ( (len(nss)>0 and sum(nss[-1].count(char) for char in excepts1)==math.ceil(len(nss[-1])/2) )  or not any(char or unicodedata.category(char) in vowels for char in syll) or sum(syll.count(char) for char in excepts1)==math.ceil(len(syll)/2) ):
            elif lang=="hin" and ( (len(nss)>0 and nss[-1].count('्')==math.ceil(len(nss[-1])/2) )  or not any(char or unicodedata.category(char) in vowels for char in syll) or syll.count('्')==math.ceil(len(syll)/2) ):
                #print ("2 ",i)
                if len(nss) == 0:
                    front += syll
                elif nss[-1]!=" ":
                    nss = nss[:-1] + [nss[-1] + syll]
                else:
                    nss.append(syll)
                    
            else:
                #print ("3 ",i)
                if len(nss) == 0:
                    nss.append(front + syll)
                    front = ""
                else:
                    nss.append(syll)

        return nss

    # SONORITY HIERARCHY, MODIFY FOR LANGUAGE BELOW
    # categories should be collapsed into more general groups
    
    if lang=='en':
        vowels = 'aeiouyàáâäæãåāèéêëēėęîïíīįìôöòóœøōõûüùúūůÿ'
        approximates = ''
        nasals = 'lmnrw'
        fricatives = 'zvsf'
        affricates = ''
        stops = 'bcdgtkpqxjhy'
        hhandlers='bcdgjkpqstwx'
        ehandlers='lmnrwzvsbcdgtkpq'

    else:
        #print (word.split()[0])
        #word=[part for part in word.split()[0]]
        #print (word)
        vowels = 'McMnअआइईउऊऋएऐओऔय​'
        approximates = ''
        nasals = 'ल​​​म​न​र​व​'
        fricatives = 'ज़व​स​फफ़​'
        affricates = ''
        #stops = 'कगचजटडतदपब‌यखघछझथधफभषशक़ख़ग़ज़ड़ढ़'
        stops='Lo'
        hhandlers=''
        excepts1='़्'
        excepts2='ँं'
        
    iosounds='ीिiोइई'
    aeandosounds='aoअआओऔऑऒएऍऎइई'
    

    # assign numerical values to phonemes (characters)
    vowelcount = 0  # if vowel count is 1, syllable is automatically 1
    sylset = []  # to collect letters and corresponding values
    last=''
    lastlist=['','']

    for i,letter in enumerate(word):
        #print ("letter ",letter," ","categ ",unicodedata.category(letter))
        if letter==' ':
            sylset.append((letter, 0))
        elif lang=='en' and letter.lower()=='h' and last in hhandlers:
            sylset.append((last+'h', 2))
            last=''
        elif lang=='en' and (letter.lower()=='q') and last=='s':
            sylset.append((last+letter.lower(), 0))
            last=''
        elif lang=='en' and letter.lower()=='k' and last=='c':
            sylset.append((last+'k', 5))
            last=''
        elif lang=='en' and letter.lower() in stops and letter.lower()!='y' and last=='n':
            sylset.append((last+letter.lower(), 0))
            last=''
        #elif lang=='en' and letter.lower()=='a' and i-1>=0 and word[i-1].lower()=='i':
        #    sylset.append((letter.lower(), 0))
        
        # elif lang=='en' and letter.lower()=='e' and lastlist[0] not in vowels and ( ( i+1<len(word) and word[i+1]==' ') or ( i+2<len(word) and word[i+2]==' ') or i+1==len(word) or i+2==len(word)):
        #     #print ("4 ",lastlist)
        #     sylset.append((lastlist[0]+'e', lastlist[1]))
        #     lastlist=['','']
        #     vowelcount += 1
        # elif lang=='en' and letter.lower()=='e' and lastlist[0] not in vowels:
        #     #print ("5 ",lastlist)
        #     sylset.append((lastlist[0],lastlist[1] ))
        #     sylset.append((letter.lower(), 5))
        #     lastlist=['','']
        #     vowelcount += 1
        elif lang=='en' and letter.lower() in hhandlers and i+1<len(word) and word[i+1]=='h':
            last=letter.lower()
        elif lang=='en' and letter.lower()=='s' and i+1<len(word) and (word[i+1]=='q'):
            last=letter.lower()
        elif lang=='en' and letter.lower()=='c' and i+1<len(word) and word[i+1]=='k':
            last=letter.lower()
        elif lang=='en' and letter.lower()=='n' and i+1<len(word) and word[i+1]!='y' and word[i+1] in stops:
            last=letter.lower()
        # elif lang=='en' and letter.lower() not in vowels and i+1<len(word) and word[i+1]=='e':
        #     lastlist=[]
        #     lastlist.append(letter.lower())
        #     if letter.lower() in nasals:
        #         lastlist.append(3)
        #     elif letter.lower() in fricatives:
        #         lastlist.append(2)
        #     else:
        #         lastlist.append(0)
        elif lang=='en' and letter.lower()=='y' and i+1<len(word) and word[i+1].lower() in vowels:
            sylset.append((letter.lower(), 0))
        elif lang=='en' and letter.lower() in vowels:
            sylset.append((letter.lower(), 5))
            vowelcount += 1
        elif lang=='en' and letter.lower() in approximates:
            sylset.append((letter.lower(), 4))
        elif lang=='en' and letter.lower() in nasals:
            sylset.append((letter.lower(), 3))
        elif lang=='en' and letter.lower() in fricatives:
            sylset.append((letter.lower(), 2))
        elif lang=='en' and letter.lower() in affricates:
            sylset.append((letter.lower(), 1))
        elif lang=='en' and letter.lower() in stops:
            sylset.append((letter.lower(), 0))
        elif lang=='en':
            sylset.append((letter.lower(), 0))

        elif lang=='hin' and letter in excepts2: 
            #print ("h2 ",letter)
            last=letter
        elif  lang=='hin' and i>0 and word[i-1] in excepts2:
            #print ("h1 ",letter)
               
            if lang=='hin' and i+1<len(word) and word[i+1] in excepts1: 
                lastlist=[]
                lastlist.append(last+letter)
                lastlist.append(5)
                
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((last+letter+word[i+1], 0))
                sylset.append(('', 5))
            else:
                sylset.append((last+letter, 0))
                if (i+1<len(word) and unicodedata.category(word[i+1])[0]=='L' ):
                    sylset.append(('',5))
            

        elif lang=='hin' and letter in excepts1: 
            temp=letter
            letter=lastlist[0]+letter
            letterno=lastlist[1]
            lastlist=['','']
            # if i+1<len(word) and word[i+1]==r'े':
            #     lastlist=[]
            #     lastlist.append(letter)
            #     lastlist.append(letterno)
            # else:

            if (i+1<len(word) and word[i+1]=='्'):
                lastlist[0]=letter
                lastlist[1]=letterno
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and temp=='़'):
                sylset.append((letter, letterno))
                sylset.append(('', 5))  
                if (unicodedata.category(word[i+1])[0]=='M'):
                    sylset.append((word[i+1], 5))          
            
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((letter+word[i+1], letterno))
                sylset.append(('', 5))
            else:
                sylset.append((letter, letterno))
         
        elif lang=='hin' and i+1<len(word) and word[i+1] in excepts1: 
           
            lastlist=[]
            lastlist.append(letter)
            if letter in nasals:
                lastlist.append(3)
            elif letter in fricatives:
                lastlist.append(2)
            else:
                lastlist.append(0)

        # elif lang=='hin' and letter='य' and i+1<len(word) and (word[i+1] or unicodedata.category(word[i+1]) in vowels):
        #     sylset.append((letter, 0))
        
        elif lang=='hin' and unicodedata.category(letter)[0]=='M':
            
            if (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((word[i+1], 5))
            elif len(sylset)>0 and ( (i+2<len(word) and word[i+2]==' ' and word[i+1] in excepts2) or (i+2==len(word) and word[i+1] in excepts2) ):
                temp=sylset[-1]
                sylset.pop()
                sylset.append((temp[0]+word[i+1],temp[1]))
            else:
                continue

        elif lang=='hin' and letter in vowels and letter!='य':
            
            if (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((letter+word[i+1], 5))
                sylset.append(('', 5))
            else:
                sylset.append((letter, 5))

        elif lang=='hin' and letter in nasals:
            
            if i+1== len(word) or (i+1<len(word) and (unicodedata.category(word[i+1])=='Lo' or word[i+1] in excepts2  or word[i+1]==' ')):
                sylset.append((letter, 3))
                sylset.append(('', 5))
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((letter+word[i+1], 3))
                sylset.append(('', 5))

            else:
                sylset.append((letter, 0))                
        elif lang=='hin' and letter in fricatives:
            
            if i+1== len(word) or (i+1<len(word) and (unicodedata.category(word[i+1])=='Lo' or word[i+1] in excepts2  or word[i+1]==' ')):
                sylset.append((letter, 2))
                sylset.append(('', 5))
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((letter+word[i+1], 2))
                sylset.append(('', 5))

            else:
                sylset.append((letter, 0))                

        elif lang=='hin' and (unicodedata.category(letter)=='Lo'):
            
            if i+1== len(word) or (i+1<len(word) and (unicodedata.category(word[i+1])=='Lo' or word[i+1] in excepts2  or word[i+1]==' ')):
                sylset.append((letter, 0))
                sylset.append(('', 5))
            elif (i+1<len(word) and word[i+1]!=' ' and word[i+1] not in excepts2 and unicodedata.category(word[i+1])[0]=='M'):
                sylset.append((letter+word[i+1], 0))
                sylset.append(('', 5))

            else:
                sylset.append((letter, 0))                

        elif lang=='hin':
            sylset.append((letter, 0))


    #print (sylset)
    # SSP syllabification follows
    final_sylset = []
    if vowelcount == 1:  # finalize word immediately if monosyllabic
        #print ("no")
        final_sylset=[i for j in word.split() for i in (j, ' ')][:-1] 
        #final_sylset.append(word)
    if vowelcount != 1:
        syllable = ''  # prepare empty syllable to build upon
        for i, tup in enumerate(sylset):

            if i == 0:  # if it's the first letter, append automatically
                syllable += tup[0]
            else:

                if tup[0] in aeandosounds and sylset[i-1][0] in iosounds:
                    
                    if syllable!='':
                        final_sylset.append(syllable)
                    syllable = tup[0]
                    if i+1<len(sylset) and sylset[i+1][0]!=tup[0]: 
                        final_sylset.append(syllable)
                        syllable = ''

                # add whatever is left at end of word, last letter
                elif i == len(sylset) - 1:
                    syllable += tup[0]
                    final_sylset.append(syllable)

                # MAIN ALGORITHM BELOW
                elif tup[0]==' ':
                    if syllable!='':
                        final_sylset.append(syllable)
                    syllable = tup[0]
                    final_sylset.append(syllable)
                    syllable = ''

                

                # these cases DO NOT trigger syllable breaks
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    #print ("1 ",i)
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    #print ("2 ",i)
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    #print ("3 ",i)
                    #print ("7",i)
                    syllable += tup[0]
                # elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                #          tup[1] > sylset[i - 1][1] and tup[0]=='य':
                     
                #     final_sylset.append(syllable)
                #     syllable = ""
                #     syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]:
                    #print ("5 ",i)
                    #print ("8",i," ",syllable)
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    #print ("6 ",i)
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]:
                    #print ("7 ",i)
                    syllable += tup[0]
                elif ((i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]) and tup[1]==5:
                    #print ("8 ",i)
                    #print ("9 ",tup[0])
                    syllable += tup[0]
                # elif ((i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                #         tup[1] == sylset[i - 1][1]) and tup[1]==5 and tup[0]=='य':
                #     #print ("9 ",i)
                #     final_sylset.append(syllable)
                #     syllable = ""
                #     syllable += tup[0]

                # these cases DO trigger syllable break
                # if phoneme value is equal to value of preceding AND following
                # phoneme
                elif ((i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]):
                    #print ("10 ",i)
                    #print ("syllable,",tup[0]," ",i)
                    syllable += tup[0]
                    #print (syllable)
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    final_sylset.append(syllable)
                    syllable = ""

                # if phoneme value is less than preceding AND following value
                # (trough)
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    #print ("11 ",i)
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    final_sylset.append(syllable)
                    syllable = ""
                    syllable += tup[0]

                # if phoneme value is less than preceding value AND equal to
                # following value
                elif (i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    #print ("12 ",i)
                    syllable += tup[0]
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    final_sylset.append(syllable)
                    syllable = ""
            #print (syllable)
            #print ("sylset ",final_sylset)
    #print (final_sylset)     
    final_sylset = no_syll_no_vowel(final_sylset)

    

    return (final_sylset)

# command line usage
if __name__ == '__main__':
    print("\n\nSonoriPy-ing...\n")

    sfile = sys.argv[1]  # input text file to syllabify
    with open(sfile, 'r', encoding='utf-8') as f:
        text = f.read()

    sylls = [SonoriPy(w) for w in cleantext(text).split()]

    toprint = ""
    for word in sylls:
        for syll in word:
            if syll != word[-1]:
                toprint += syll
                toprint += "-"
            else:
                toprint += syll
        toprint += " "

    fmt = '%Y/%m/%d %H:%M:%S'
    date = "SonoriPyed on " + str(datetime.now().strftime(fmt))

    finalwrite = date + "\n\n" + toprint

    with open('SonoriPyed.txt', 'w', encoding='utf-8') as f:
        f.write(finalwrite)

    print("\nResults saved to SonoriPyed.txt\n\n")
