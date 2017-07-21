from pygithub3 import Github
from urllib2 import urlopen
import json
repo=[]
c=[]
final_byte_count={}
final_list={}
final_percent_list=[]
other=[]
import re
import requests

def langPercent(user, languages):
    
    link1=["https://api.github.com/users/"]
    str1=user
    str2="/repos"
    link1.append(str1)
    link1.append(str2)
    link1.append("?client_id=3553ff878aa2222e9bfc&client_secret=28f4870866e637170fffa9031d89567ae9378b41")
    x="".join(link1)
    req=urlopen(x).read()
    data=json.loads(req)
    for i in range(0,len(data)):
        repo.append(str(data[i]["full_name"]))
               
    #print repo

    for i in range(0,len(repo)):
        link2=["https://api.github.com/repos/"]
        link2.append(repo[i])
        link2.append("/languages")
        link2.append("?client_id=3553ff878aa2222e9bfc&client_secret=28f4870866e637170fffa9031d89567ae9378b41")
        y="".join(link2)
        req=urlopen(y).read()
        data=json.loads(req)
        c.append(data)
    #print c
    ###Add bytes of code of same language
    from collections import Counter
    counter=Counter()
    for i in c:
        counter.update(i)
    for key,value in sorted(counter.iteritems()):
        final_byte_count[key]=value
    #print final_byte_count,languages
    ###segregate languages based on language list returned by lang function
    for i in languages:
        for key,value in final_byte_count.iteritems():
            if(i==key):
                final_list[key]=value
            else:
                other.append(key)
        
    #print final_list
    ###percentage calculation
    denom=sum(final_list.values())
    #print denom
    for key,value in final_list.iteritems():
        #print value
        percentage=(float(value)/denom*1.0)*100.0
        #print percentage
        final_percent_list=(str(key),str(round(percentage)))
    return final_percent_list,list(set(other))


