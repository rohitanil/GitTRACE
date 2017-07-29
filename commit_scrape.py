from bs4 import BeautifulSoup as bs
import re
import urllib2 



def contrib(item):
	profile="https://github.com/"
	url = urllib2.urlopen(profile+item)
	sample = url.read()
	soup=bs(sample,"lxml")

	text = soup.find('div',attrs={"class":"js-contribution-graph"}).findAll('h2')  # Find the <h2> tag inside div class
	
	new=[]
	
	for x in text:
		new.append(str(x))


	x="".join(new)
	z=re.findall(r'\d+', x)
	return z[3]

#name="cypherix"
contrib(name) #pass the profile name as parameter
