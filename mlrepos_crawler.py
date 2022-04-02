from github import Github
import os
from pprint import pprint
import csv
import requests
import json
import random
import re

'''
   Crawl something interesting :)
'''
class GitCrawler(object):
    api         = None
    repos       = []
    issues      = []
    cves        = []
    
    '''
        Provide Github token 
    '''
    def __init__(self, token):
        token_env = os.getenv('GITHUB_TOKEN',token)
        self.api  = Github(token_env)
    
    '''
       Search all repos given a filtering query
    '''
    def search_repos(self, repo_query, order, shuffle):
        api_repos = self.api.search_repositories(query=repo_query, 
                                                 sort='stars', 
                                                 order=order)
        if shuffle == False:
            self.repos = [repo.name for repo in api_repos]
        else:
            self.repos = random.shuffle([repo.name for repo in api_repos]) 
        # self.repos = self.repos[:MAX]
    
    '''
        Search all issues given a filtering query
    '''
    def search_issues(self, repo_name, issue_query, order):
        rep_query  = ''.join(['repo:', repo_name])
        sch_query  = ' '.join([rep_query, issue_query])
        api_issues = self.api.search_issues(query=sch_query, 
                                            sort='comments', 
                                            order=order)
        self.issues= [ 
                        [
                            issue.title, 
                            ' '.join([
                                        comment.body.encode('utf-8') 
                                        for comment in issue.get_comments()
                                    ]),
                            issue.state,
                            issue.created_at,
                            issue.closed_at,
                            issue.url
                        ] 
                        for issue in api_issues
                     ]

    '''
       Parses CVE IDs in titles and comments of the issues found
    '''
    def get_cves(self):
        cve_pattern = 'CVE-\d{4}-\d{4,7}'
        self.cves   = [] 
        for issue in issues:
            cve_comments = []
            cve_titles   = []
            if 'cve' in comments:
                cve_comments = re.findall(cve_pattern, issue[1])
                cve_comments = list(dict.fromkeys(cve_comments))
                self.cves += cve_comments
            if 'cve' in titles:
                cve_titles = re.findall(cve_pattern, issue[0])
                cve_titles = list(dict.fromkeys(cve_titles))
                self.cves += cve_titles

    '''
        Getter for repos
    '''
    def get_repos(self):
        return self.repos

    ''' 
        Getter for issues
    '''
    def get_issues(self):
        return self.issues

    ''' 
        Getter for cves
    '''
    def get_cves(self):
        return self.cves

    '''
       Output repo names in CSV 
    '''
    def to_csv(self, path, opt):
        csv_file = open(path, 'w')
        csv_out  = csv.writer(csv_file)
        if opt == 'r':  # repo
            csv_file.write('repo_name')
            for name in self.repos:
                csv_file.write(name)
                csv_file.write('\n')
            csv_file.close()
        elif opt == 'i': # issue
            csv_out.writerow(('title','comments','state',
                              'created_at','closed_at','url'))
            for issue in self.issues:
                csv_out.writerow(issue)
            csv_file.close()
        elif opt == 'c': # CVE 
            csv_file.write('cve_id')
            for cve in self.cves:
                csv_file.write(cve)
                csv_file.write('\n')
            csv_file.close()


'''
   Test with machine learning samples
'''
if __name__ == "__main__":
    # auth
    # Need to use GitHub Entreprise to increase the
    # limit rate to 15 000 requests/hour/repository
    MY_TOKEN = '<YOUR_TOKEN>'
    MY_BASE_DIR = '<YOUR_BASE_DIR>\\'
    gc  = GitCrawler(MY_TOKEN)

    # get all repo topics containing machine-learning and most starred
    query = 'machine-learning in:topic stars:>1000'
    path  = ''.join([MY_BASE_DIR, 'repos.csv'])
    
    gc.search_repos(repo_query=query, order='desc', shuffle=True)
    gc.to_csv(path, 'r')
    
    # get all issues containing threat patterns
    comment_queries = ' OR '.join(['cve in:comments'   , 'vuln in:comments'  ,
                                   'secur in:comments' , 'attack in:comments',
                                   'threat in:comments'])
    title_queries   = ' OR '.join(['cve in:title'   , 'vuln in:title'  ,
                                   'secur in:title' , 'attack in:title',
                                   'threat in:title'])
    #query           = title_queries
    query           = comment_queries

    for name in gc.get_repos():
        gc.search_issues(repo_name=name, issue_query=query, order='desc')
        path = ''.join([MY_BASE_DIR, name, '.csv'])
        gc.to_csv(path, 'i')

    # get CVE IDs
    path  = ''.join([MY_BASE_DIR, 'cves.csv'])
    gc.get_cves()
    gc.to_csv(path, 'c')

    '''
       EOF
    '''
