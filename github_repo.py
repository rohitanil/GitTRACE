from pygithub3 import Github
from urllib2 import urlopen
import json
import requests
repo=[]

def langPercent(user, languages):
    
    link1=["https://api.github.com/users/"]
    str1=user
    str2="/repos"
    link1.append(str1)
    link1.append(str2)
    link1.append("?client_id=<"INSERT CLIENT ID">&client_secret=<"INSERT CLIENT SECRET TOKEN">")
    x="".join(link1)
    req=urlopen(x).read()
    data=json.loads(req)
    for i in range(0,len(data)):
        repo.append(str(data[i]["full_name"]))
               
    print repo

    for i in range(0,len(repo)):
        link2=["https://api.github.com/repos/"]
        link2.append(repo[i])
        link2.append("/languages")
        link2.append("?client_id=<"INSERT CLIENT ID">&client_secret=<"INSERT CLIENT SECRET TOKEN">")
        y="".join(link2)
        req=urlopen(y).read()
        data=json.loads(req)
        print data
        
if __name__=="__main__":
    langPercent("rohitanil",0)

