from pygithub3 import Github
from urllib2 import urlopen
import json
import operator
from collections import Counter
import LRM
p=[]
import re
import requests

def langPercent(user, languages,repo):
    
    c=[]
    final_byte_count={}
    final_list={}
    final_percent_list={}
    other=[]
    x1=''
    y1=''
    """link1=["https://api.github.com/users/"]
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
    print repo"""
                      
    
    try:
        for i in range(0,len(repo)):
            link2=["https://api.github.com/repos/"]
            link2.append(repo[i])
            link2.append("/languages")
            link2.append("?client_id=3553ff878aa2222e9bfc&client_secret=28f4870866e637170fffa9031d89567ae9378b41")
            y="".join(link2)
            req=urlopen(y).read()
            data=json.loads(req)
            c.append(data)
    except ValueError,e:
        print e
    pred_commits,indi_commits=commits_prediction(user,repo)
    #print c
    ###Add bytes of code of same language
    
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
                #print key
                other.append(key)
        
    #print final_list
    ###percentage calculation
    denom=sum(final_list.values())
    #print denom
    for key,value in final_list.iteritems():
        #print value
        k=[]
        percentage=(float(value)/denom*1.0)*100.0
        #print percentage
        final_percent_list[key]=round(percentage)
        
    print final_percent_list
    'Find language with highest percentage'
    if(final_percent_list):
        
        c1=max(final_percent_list.iteritems(), key=operator.itemgetter(1))
        x1=c1[0]
        y1=str(c1[1])
    return x1+"- "+y1,list(set(other)),pred_commits,indi_commits
    

def commits_prediction(user,repo):
    #print len(repo),user
    dates=[]
    commits=[]
    week_list=[]
    commitcount_list=[]
    final_commit_count={}
    for i in range(0,len(repo)):
        weekly_commits={}
        link3=["https://api.github.com/repos/"]
        link3.append(repo[i])
        link3.append('/stats/contributors?client_id=3553ff878aa2222e9bfc&client_secret=28f4870866e637170fffa9031d89567ae9378b41')
        link3="".join(link3)
        #print link3
        """ Check if a repo is empty or not"""
        """try:
            req1=urlopen(link3).read()
            data=json.loads(req1)
            if(data):
                
                for j in range(0,len(data)):
                    if(data[j]['author']['login']==user):
                        for z in range(0,len(data[j]['weeks'])):
                            
                            hash1=data[j]['weeks'][z]['w']
                            weekly_commits[hash1]=data[j]['weeks'][z]['c']
                        #print weekly_commits
                        #print "\n\n"
                        week_list.append(weekly_commits)
            else:
                print repo[i]
                print kereela"""
            
        try:
            cou=0
            data=[]
            'Retry getting data from repo[i] if data returned is empty'
            while(not data and cou!=5):
                req1=urlopen(link3).read()
                data=json.loads(req1)
                cou=cou+1
                print cou
            if(data):
                for j in range(0,len(data)):
                    if(data[j]['author']['login']==user):
                        for z in range(0,len(data[j]['weeks'])):
                            hash1=data[j]['weeks'][z]['w']
                            weekly_commits[hash1]=data[j]['weeks'][z]['c']
                        #print weekly_commits
                        #print "\n\n"
                        week_list.append(weekly_commits)
            
        except ValueError,e:
            #print repo[i]
            #print"\n"
            #print e
            continue
            
    #print week_list
    ###Add same week hash commits, sort commits based on week hash and add commits to seperate list
    if(week_list):
        
        counter = Counter()
        for d in week_list:
            counter.update(d)
        for key,value in sorted(counter.iteritems()):
            final_commit_count[key]=value
        #print final_commit_count
        for key in sorted(final_commit_count.iterkeys()):
            commitcount_list.append(final_commit_count[key])
        #print sorted(final_commit_count.iterkeys())
        print commitcount_list
        for i in range(0,len(commitcount_list)):
            dates.insert(i,i)
        sum1=0
        for i in range(0,len(commitcount_list)):
            #print commitcount_list[i]
            sum1+=commitcount_list[i]
            commits.insert(i,sum1)
        #print dates
        print commits
        print commits[i]
        LRM.show_plot(dates,commits)
        predicted_commits, coefficient, constant = LRM.predict_commits(dates,commits,100)
        #print "Commits Prediction: ",int(predicted_commits)
        #print "The regression coefficient is ",str(coefficient),", and the constant is ", str(constant)
        #print "the relationship equation between weeks and commits is: commits = ",str(coefficient),"* date + ",str(constant)
        return int(predicted_commits),commits[i]
    else:
        return 0,0
         

    


