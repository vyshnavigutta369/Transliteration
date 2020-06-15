# -*- coding: utf-8 -*-
# encoding: utf-8



import unicodedata
import ast
import itertools
from sonoripy import SonoriPy


class Syllabification:

	def __init__(self):
		

		self.mapping={'क':['ck','k','c','q'],'ख': ['kh','k','q'],'ग':['g'], 'घ':['gh','g'], 'ङ':['ng'], 'च':['tch','ch'], 'छ':['chh'], 'ज':['g','j'],'झ':['jh','j'],'ञ':['kn','n','y'], 'ट':['t'], 'ठ':['t'],'ड':['d'], 'ढ':['d'], 'ण':['n'], 'त':['t'], 'थ':['th','t'], 'द':['d'], 'ध':['dh','d'],'न':['n','kn'],'प':['p'], 'फ':['ph'], 'ब':['b'],'भ':['bh','b'], 'म':['m'], 'र':['r'], 'ल':['l'], 'व':['v','w','o'], 'स':['s'],'ह':['h'], 'श':['ssio','sio','tio','sh','ti', 'si','s'], 'ष':['ssio','sio','tio','sh','ti', 'si','s'], 'ं':['n'], 'य':['y','u'], 'ळ':['l'] , 'ज्ञ':['gn', 'gy','g'], 'ॐ':['om'],
		            'क़':['ck','k','c','q'],'ख़': ['kh','k','q'],'ग़':['g'], 'घ़':['gh','g'], 'च़':['tch','ch'], 'छ़':['chh'], 'ज़':['g','j'],'झ़':['jh','j'],'ञ़':['n'], 'ट़':['t'], 'ठ़':['t'],'ड़':['d'], 'ढ़':['d'], 'ण़':['n'], 'त़':['t'], 'थ़':['th','t'], 'द़':['d'], 'ध़':['dh','d'],'ऩ':['n','kn'],'प़':['p'], 'फ़':['ph'], 'ब़':['b'],'भ़':['bh','b'], 'म़':['m'], 'ऱ':['r'], 'ल़':['l'], 'व़':['v','w'], 'स़':['s'],'ह़':['h'], 'श़':['ssio','sio','tio','sh','ti', 'si','s'], 'ष़':['ssio','sio','tio','sh','ti', 'si','s'] }

		self.excepts='ं'

		self.shandlers=['श','ष', 'श़', 'ष़']



	def mappingbetweenscript(self,word1,word2):

		vowelshin = 'McMnअआऑइईउऊऋएऐऍओऔयय़'
		vowelsen='aeiouy'
		if 'ञ' in word2:
			vowelsen='aeiou'

		if 'व' in word2:
			vowelsen='aeiuy'


		pos=[]

		pos1t=[char for k,char in enumerate(word1)  if char not in vowelsen]
		pos2=[k for k,char in enumerate(word2)  if (unicodedata.category(char)[0]=='L' and char not in vowelshin) or char in self.excepts]
		pos2t=[char for k,char in enumerate(word2)  if (unicodedata.category(char)[0]=='L' and char not in vowelshin) or char in self.excepts]

	 	
		pos1=[]
		s="".join(pos1t)
		#print (s)
		pos1t=[k for k,char in enumerate(word1)  if char not in vowelsen]
		start=0


		
		for k,char in enumerate(pos2t):
		    for val in self.mapping[char]:
		        ind=s.find(val,start)
		        if (ind!=-1):
		        	start+=len(val)
		        	pos1.append(pos1t[ind])
		        	break
		    if (ind==-1) and start<len(s):
		    	pos1.append(pos1t[start])
		    	start+=1



		while start<len(s):
		    pos1.append(pos1t[start])
		    start+=1

		pos.append(pos1)
		pos.append(pos2)
		

		return pos

	def sonoripy(self,word,lang):
		List=SonoriPy(word, lang)

		res=""
		for i,syll in enumerate(List):
			res+=syll
			if i+1<len(List) and List[i+1]!=' ' and List[i]!=' ':
				res+='@'

		return res

	def filesonoripy(self,pathtofile,lang):
		OutEnfile='Son-'+pathtofile.split('/')[-1]
		with open(pathtofile,'r') as r1, open(OutEnfile,'w') as w1:
			l=r1.readlines()
			for line in l:
				List=SonoriPy(line.rstrip('\n'), lang)
				res=""
				for i,syll in enumerate(List):
					res+=syll
					if i+1<len(List) and List[i+1]!=' ' and List[i]!=' ':
						res+='@'
				w1.write(res+'\n')


	def filenormalize(self,pathtoEnfile,pathtoHinfile):
		OutEnfile='Nrm-'+pathtoEnfile.split('/')[-1]
		OutHinfile='Nrm-'+pathtoHinfile.split('/')[-1]
		with open(pathtoEnfile,'r') as r1,open(pathtoHinfile,'r') as r2, open(OutEnfile,'w') as w1, open(OutHinfile,'w') as w2:
		    l1=r1.readlines()
		    l2=r2.readlines()
		    for index,(line1,line2) in enumerate(zip(l1,l2)):
		        # line1 = ast.literal_eval(line1)
		        # line2 = ast.literal_eval(line2)
		        # line1 = [list(v) for k,v in itertools.groupby(line1,key=str.isspace) if not k] 
		        # line2 = [list(v) for k,v in itertools.groupby(line2,key=str.isspace) if not k] 
		        line1=SonoriPy(line1.rstrip('\n'), lang='en')
		        line2=SonoriPy(line2.rstrip('\n'),lang='hin')

		        #print (line1,line2)

		        normalizedline1,normalizedline2= self.normalize(line1,line2)

		        w1.write(str(normalizedline1)+'\n')
		        w2.write(str(normalizedline2)+'\n')



	def normalize(self,line1,line2):
		line1 = [list(v) for k,v in itertools.groupby(line1,key=str.isspace) if not k]
		line2 = [list(v) for k,v in itertools.groupby(line2,key=str.isspace) if not k]
		newline1=[]
		newline2=[] 
		for (word1,word2) in zip(line1,line2):
			i=0
			j=0
			temp1=[]
			temp2=[]
			while(i<len(word1) and j<len(word2)):
				vowelsen='aeiouy'
				vowelshin = 'McMnअआऑइईउऊऋएऐऍओऔयय़'

				if (word1[i]=='' and word2[i]==''):
					i+=1
					j+=1
					continue
				elif (word1[i]==''):
				    i+=1
				    continue
				elif (word2[j]==''):
				    j+=1
				    continue
		       
				word1[i]=word1[i].strip(' ')
				word2[j]=word2[j].strip(' ')

				if (word2[j][-1] in self.shandlers and len(word1[i])>1 and (word1[i][-2:]=='ti' or word1[i][-2:]=='si') and i+1<len(word1) and word1[i+1][0]=='o'):
					word1[i]+=word1[i+1]
					word1[i+1]=''

				if j+1<len(word2) and len(word1[i])>0 and word1[i][-1]=='n' and word2[j+1][0] in self.excepts:
					word2[j]+=word2[j+1][0]
					word2[j+1]=word2[j+1][1:]

				#print (word1[i],word2[j])
				pos=self.mappingbetweenscript(word1[i],word2[j])
				pos1=pos[0]
				pos2=pos[1]

		        #print (word1[i],word2[j])
		        #print (pos1,pos2)
		                       
				if len(pos1)<len(pos2) and j+1<len(word2):
				    word2[j+1]=word2[j][pos2[len(pos1)]:]+word2[j+1]
				    word2[j]=word2[j][:pos2[len(pos1)]]
				    #print ("hello")

				elif len(pos1)>len(pos2) and j+1<len(word2):
					#print(pos2nxt,len(pos2nxt))
				    # if word2[j+1][0] in self.mapping.keys() and any(word1[i+1].find(char)==0 for char in self.mapping[word2[j+1][0]]) and word1[pos1nxt[-1]] in self.mapping[word2[pos2nxt[-1]]]:
				    #     pass
				    
					if i+1<len(word1):
						pos=self.mappingbetweenscript(word1[i+1],word2[j+1])
						pos1nxt=pos[0]
						pos2nxt=pos[1]

						if len(pos1nxt)==len(pos2nxt) and word2[j+1][0] in self.mapping.keys() and any(word1[i+1].find(char)==0 for char in self.mapping[word2[j+1][0]]):
							pass
						elif len(pos1)-len(pos2)<len(pos2nxt):
							word2[j]=word2[j]+word2[j+1][:pos2nxt[len(pos1)-len(pos2)]]
							word2[j+1]=word2[j+1][pos2nxt[len(pos1)-len(pos2)]:]
						else:
							word2[j]=word2[j]+word2[j+1]
							word2[j+1]=''
					else:
						word2[j]=word2[j]+word2[j+1]
						word2[j+1]=''

				elif len(pos1)==len(pos2) and i+1 < len(word1) and j+1<len(word2):
				    pos2nxt=[k for k,char in enumerate(word2[j+1])  if (unicodedata.category(char)[0]=='L' and char not in vowelshin) or char in self.excepts]
				    pos1nxt=[k for k,char in enumerate(word1[i+1])  if char not in vowelsen]

				    if (j+2<len(word2) and word2[j+2][0] in self.mapping.keys() and any(word1[i+1].find(char)==0 for char in self.mapping[word2[j+2][0]]) and len(pos2nxt)==0 and len(pos1nxt)!=0 and len(word2[j])>0):
				        word2[j]=word2[j]+word2[j+1]
				        word2[j+1]=''

				if word1[i]!='':
				    temp1.append(word1[i])
				if word2[j]!='':
				    temp2.append(word2[j])

				i+=1
				j+=1

			while i<len(word1) and len(temp1)>0:
			    temp1[-1]+=word1[i]
			    i+=1
			while j<len(word2) and len(temp2)>0:
			    temp2[-1]+=word2[j]
			    j+=1

			newline1.append(temp1)
			newline2.append(temp2)

		s1=''
		list1=[]
		for spaceseplist in newline1:
			for syllable in spaceseplist:
				s1+=syllable
				list1.append(syllable)
				s1+='@'
			s1=s1[:-1]
			s1+=' '
			list1.append(' ')
		s1=s1[:-1]
		list1=list1[:-1]
		s2=''
		list2=[]
		for spaceseplist in newline2:
			for syllable in spaceseplist:
				s2+=syllable
				list2.append(syllable)
				s2+='@'
			s2=s2[:-1]
			s2+=' '
			list2.append(' ')
		s2=s2[:-1]
		list2=list2[:-1]
		
		return (list1,list2)


if __name__ == '__main__':

	syllabify=Syllabification()

	#syllabify.filesonoripy('wrdsen.txt','en')

	syllabify.filenormalize('Englishtraining.txt','GgleHin.txt')


        
        
