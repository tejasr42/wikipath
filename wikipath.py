from bs4 import BeautifulSoup as bs
import requests
import re
class Linktree(object):
	def __init__(self,links,data,tier,parent):
		self.data=data
		self.links=links
		self.children=[]
		self.parent=parent
		self.tier=tier
	def add_child(self,obj):
		self.children.append(obj)
		obj.parent

linkarray=[]
temp=[]
tierlinks=0
def wikipath(term,final,breadth):
	url="https://en.wikipedia.org/w/index.php?search="
	f=requests.get(url+final)
	fin=str(f.url.split('/')[-1])
	r=requests.get(url+term)
	current=str(r.url.split('/')[-1])
	print "| "+current+" |", "to","| "+fin+" |"
	x=wikilink(term,breadth)
	tierlinks=Linktree(x[0],current,1,False)
	temp.append(tierlinks)
	linkarray.append(0)
	linkarray.append(temp)
	backprop=recur(1,fin,breadth)
	path=genpath(backprop,[backprop.data])
	path.insert(0,current)
	path.append(fin)
	print path

def wikilink(term,breadth):
	url="https://en.wikipedia.org/w/index.php?search="
	urlf='https://en.wikipedia.org'
	r=requests.get(url+term)
	data=bs(r.content,'html.parser')
	links=data.select('div#mw-content-text > p a[href^="/wiki/"]')
	articles=[]
	for link in links:
		if ":" in link['href']:
			links.remove(link)
		else:
			articles.append(str(link['href'][6:]))
	ret=[]
	ret.append(list(set(articles))[:breadth])
	ret.append(str(r.url.split('/')[-1]))
	return ret

def recur(tier,final,breadth):
	for article in linkarray[tier]:
		if final in article.links:
			print "Done"
			return article
	temp=[]
	for j,article in enumerate(linkarray[tier]):
		loc=j
		for i,link in enumerate(article.links):
			print "                                                      ",'\r',
			print str(i+1)+"/"+str(len(article.links))+": "+link, '\r',
			x=wikilink(link,breadth)
			x.append(tier+1)
			x.append(loc)
			s=Linktree(x[0],x[1],x[2],x[3])
			if final in x[0]:
				print "Done"
				return s
			article.add_child(s)
			temp.append(s)
	linkarray.append(temp)
	recur(tier+1,final,breadth)

def genpath(article,lis):
	if article.parent==False:
		return lis
	else:
		genpath(linkarray[article.tier-1,article.parent],lis.insert(0,article.data))
	



#print wikilink(raw_input("Enter term:"))
print wikipath(raw_input("Enter term:"),raw_input("Enter final:"),int(raw_input("Breadth:")))

