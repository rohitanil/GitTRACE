from pygithub3 import Github
import urllib2
from urllib2 import urlopen
import json
req=[]
import re
import requests
from requests.exceptions import HTTPError
import github_repo

def count_user_commits(user):
    r = requests.get('https://api.github.com/users/%s/repos?client_id="INSERT CLIENT ID"&client_secret="INSERT CLIENT SECRET TOKEN"' % user)
    repos = json.loads(r.content)

    for repo in repos:
        if repo['fork'] is True:
            # skip it
            continue
        n = count_repo_commits(repo['url'] + '/commits')
        repo['num_commits'] = n
        yield repo


def count_repo_commits(commits_url, _acc=0):
    r = requests.get(commits_url)
    commits = json.loads(r.content)
    n = len(commits)
    if n == 0:
        return _acc
    link = r.headers.get('link')
    if link is None:
        return _acc + n
    next_url = find_next(r.headers['link'])
    if next_url is None:
        return _acc + n
    
    return count_repo_commits(next_url, _acc + n)


# given a link header from github, find the link for the next url which they use for pagination
def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]


def commits(user):
    import sys
    total_commits = 0
    for repo in count_user_commits(user):
        #print "Repo `%(name)s` has %(num_commits)d commits, size %(size)d." % repo
        total_commits += repo['num_commits']
    #print "Total commits: %d" % total_commits
    return total_commits    

def gitScrape(s):
        
        
            link=["https://api.github.com/users/"]
            link.append(s)
            link.append("?client_id="INSERT CLIENT ID"&client_secret="INSERT CLIENT SECRET TOKEN"")
            x="".join(link)
            try:
                
                req=urlopen(x).read()
                data=json.loads(req)
                str1=s
                print(str1)
                if (data["type"]=='User'):
                    #print(str1)
                    gitlang2=gitLanguages(str1)
                    totalCommits=commits(str1)
                    language_percent,other_skills=github_repo.langPercent(str1,gitlang2)
                    return(1,data['public_repos'],data['followers'],data['html_url'],totalCommits,language_percent,other_skills)
                else:
                    return 'Account type is not User',0,0,0,0,0,0
            except urllib2.HTTPError,e:
                return 'User not found!',0,0,0,0,0,0              


def gitLanguages(user):
        
        username="INSERT USERNAME"
        password="INSERT PASSWORD"
        #user = raw_input("Please enter the requested Github username: ")

        #Connect to github
        gh = Github(login=username, password = password)

        get_user = gh.users.get(user)

        user_repos = gh.repos.list(user = user).all()
        gitlang=[]

        #Count language in each repo
        for repo in user_repos:
                gitlang.append(repo.language)

        #print(gitlang)
        #remove None from languages list
        gitlang=filter(lambda a: a != None, gitlang)
        #print gitlang
        gitlang=list(set(gitlang))
        return gitlang
        


        
