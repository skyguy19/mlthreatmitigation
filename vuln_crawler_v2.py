import pandas as pd
import urllib.request
import json
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from collections import defaultdict
from requests.auth import HTTPBasicAuth


def get_tokens():    
        tokens = [
            "<token 1>",
            "<token 2>",
            "<token 3>",
            "<token 4>"
        ]
        return tokens

class GitURL:
    def __init__(self, url, ct):
        self.ct = ct
        self.url = url
        
    def getResponse(self):
        jsonData = None
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            jsonData = json.loads(content)
            #return jsonData, self.ct
        except Exception as e:
            pass
            print(e)
        return jsonData, self.ct
    
    def url_header(self):
        jsonData = None
        try:
            if self.ct == len(get_tokens()):
                self.ct = 0
            reqr = urllib.request.Request(self.url)
            reqr.add_header('Accept', 'application/vnd.github.mercy-preview+json')
            reqr.add_header('Authorization', 'token %s' % get_tokens()[self.ct])
            opener = urllib.request.build_opener(urllib.request.HTTPHandler(debuglevel=1))
            content = opener.open(reqr).read()
            self.ct += 1
            jsonData = json.loads(content)

        except Exception as e:
            pass
            print(e)
        return jsonData, self.ct

class GitHubMeta:
    def __init__(self, repo, ct):
        self.ct = ct
        self.repo = repo

    def commit_counts_(self, created_at=None):
        p = 1
        total_contrib = 0
        while True:
            if created_at != None:
                url2 = 'https://api.github.com/repos/' + self.repo + '/commits?page=' + str(p) + '&per_page=100&since='+created_at
            else:
                url2 = 'https://api.github.com/repos/' + self.repo + '/commits?page=' + str(p) + '&per_page=100'
            com_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if com_arrays != None:
                if len(com_arrays) == 0:
                    break
                total_contrib += len(com_arrays)
                if total_contrib % 500 == 0:
                    print(' ---- commits: ', total_contrib)
            else:
                break
        return total_contrib, self.ct
    
    def get_issues(self):
        issues = [] 
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/issues?page=' + str(p) + '&per_page=100&state=all'
            issues_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if issues_arrays != None:
                if len(issues_arrays) == 0:
                    break
                issues += issues_arrays
            else:
                break
        return issues, self.ct

    def get_pulls(self):
        pulls = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/pulls?page=' + str(p) + '&per_page=100&state=all'
            pulls_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if pulls_arrays != None:
                if len(pulls_arrays) == 0:
                    break
                pulls += pulls_arrays
            else:
                break
        return pulls, self.ct
    
    def get_commits(self):
        commits = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/commits?page=' + str(p) + '&per_page=100&state=all'
            commits_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if commits_arrays != None:
                if len(commits_arrays) == 0:
                    break
                commits += commits_arrays
            else:
                break
        return commits, self.ct

    def get_commits_stats(self,url):
        print(url,end='\r')
        commits_arrays, self.ct = GitURL(url, self.ct).getResponse()
        return commits_arrays, self.ct


    def get_repos(self,stars):
        issues = []
        p = 1
        while True:
            url2 = 'https://api.github.com/search/repositories?q=stars:'+str(stars)+'&sort=stars&order=desc&page='+ str(p) +'&per_page=100'
            issues_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if issues_arrays != None:
                if p== 11:
                    break
                issues += issues_arrays['items']
            else:
                break
        return issues, self.ct

    def get_repo_desc(self):
        repos = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/'+ self.repo+'?page='+ str(p) +'&per_page=100'
            repos_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            if repos_arrays != None:
                if p == 1:
                    repos.append(repos_arrays)
                    return repos , self.ct
                else:
                    break               
            else:
                break
            p += 1
        return repos, self.ct

    def get_repo_contributors(self):
        contributors = []
        p = 1
        while True:
            url2 = 'https://api.github.com/repos/' + self.repo + '/contributors?page=' + str(p) + '&per_page=100'
            contributors_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if contributors_arrays != None:
                if len(contributors_arrays) == 0:
                    break
                contributors += contributors_arrays
            else:
                break
        return contributors, self.ct

    def get_contributors_events(self,login):
        repos = []
        p = 1
        while True:
            url2 = 'https://api.github.com/users/'+str(login)+'/events?page='+str(p)+'&per_page=100'
            repos_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            if repos_arrays != None:
                if len(repos_arrays) == 0 or p==4:
                    break
                repos += repos_arrays
            else:
                break
        return repos, self.ct


    def get_user_desc(self,login):
        users = []
        url2 = 'https://api.github.com/users/'+str(login)+'?page=1&per_page=100'
        repos_arrays, self.ct = GitURL(url2, self.ct).getResponse()
        users.append(repos_arrays)
        return users , self.ct

    def get_repos(self):
        url2 = 'https://api.github.com/repos/' + self.repo
        repo, self.ct = GitURL(url2, self.ct).getResponse()
        return repo, self.ct

    def get_repos_releases(self):
        url2 = 'https://api.github.com/repos/{}/releases'.format(self.repo)
        repo, self.ct = GitURL(url2, self.ct).getResponse()
        return repo, self.ct


    def get_repos_by_language(self,lang):
        codes = []
        p = 1
        while True:
            url2 = 'https://api.github.com/search/repositories?q=language:'+str(lang)+'&page='+ str(p) +'&per_page=100'
            codes_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            import json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(codes_arrays, f, ensure_ascii=False, indent=4)
            p += 1
            print(p)
            if codes_arrays != None:
                if len(codes_arrays)==0:
                    break
                codes += codes_arrays["items"]
            else:
                break
        return codes, self.ct


    def get_repos_by_code(self,code):
        codes = []
        p = 1
        while True:
            url2 = 'https://api.github.com/search/code?q='+str(code)+'&sort=stars&order=desc&page='+ str(p) +'&per_page=100'
            codes_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            import json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(codes_arrays, f, ensure_ascii=False, indent=4)
            p += 1
            print(p)
            if codes_arrays != None:
                if len(codes_arrays)==0:
                    break
                codes += codes_arrays["items"]
            else:
                break
        return codes, self.ct

    def get_repos_by_topics(self,topic):
        repos = []
        p = 1
        while True:
            url2 = 'https://api.github.com/search/repositories?q=topic:'+str(topic)+'&sort=stars&order=desc&page='+str(p)+'&per_page=100'
            codes_arrays, self.ct = GitURL(url2, self.ct).getResponse()
            p += 1
            print(p)
            if codes_arrays != None:
                if len(codes_arrays)==0:
                    break
                repos += codes_arrays["items"]
            else:
                break
        return repos, self.ct

class IncidentDB:
    def __init__(self, base_url):
        self.url = base_url
        self.df  = pd.DataFrame()
        self.it  = 15
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def update_query_params(self, params):
        if len(params) < 2:
            return
        # req = urllib.request.Request(
        #     self.url + '&page=' + params[0] + '&s=' + params[1],
        #     data=None,
        #     headers={
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
        #     }
        # )
        # _url = urllib.request.urlopen(req)
        # self.htmlsrc = _url.read()
        # self.htmlsrc = self.htmlsrc.decode("utf8")
        self.driver.get(self.url + '&page=' + params[0] + '&s=' + params[1])

        try:
            out = WebDriverWait(self.driver, 1).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"___gatsby")))
        except TimeoutException:
            pass
        self.htmlsrc = self.driver.page_source
        self.htmlsrc = self.htmlsrc.encode('utf8')

    def collect_dataset(self):
        soup = BeautifulSoup(self.htmlsrc, 'lxml')
        root = soup.find('main')

        for div in root.find_all('div', class_='h-100 card'):
            _id = 'AML.CS00' + str(self.it)
            for img in div.find_all('img', alt=True):
                title = img['alt']
            for cnt in div.find_all('p',class_='flex-fill card-text'):
                content = cnt.getText()
            for a in div.find_all('a', class_='btn btn-link px-1'):
                url = a['href']
            for caption in div.find_all('div', class_='mb-2 text-muted card-subtitle h6'):
                date = re.sub("[^0-9]","",str(caption))
                date = date[len(date)-4:]
            _df = {'ID': _id, 'Title': title, 'Description': content, 'Date': date, 'References': url}
            self.df = pd.concat([self.df, _df], ignore_index=True)
            self.it = self.it + 1

    def get_df(self):
        return self.df


def main():
    ###########################################################################################
    base_url = 'https://incidentdatabase.ai/apps/discover?display=details&epoch_date_published_min=1517097600&lang=en'
    query    = 'attack'
    max_pages = 4
    idb = IncidentDB(base_url)
    for count in range(1, max_pages):
        idb.update_query_params(params=[str(count), query])
        idb.collect_dataset()
    idb.get_df().drop_duplicates(['Title']).to_csv('new_attacks.csv',index=False)

    ##########################################################################################
 
    repos = []
    ct = 0
    
    repos, ct = GitHubMeta("", ct).get_repos_by_topics('machine-learning%20stars:%3E=1000')
    pd.DataFrame.from_records(repos).drop_duplicates(['url']).to_csv('repos_collection.csv',index=False)

    ###########################################################################################
    repos = []
    ct = 0
    mainline_repo =pd.read_csv('repos_collection.csv')
    for index , row in mainline_repo.iterrows():
        dict_ = {}
        try:
            print(row['full_name'])
            #repo_commits, ct = GitHubMeta(row['full_name'], ct).commit_counts_()
            #contributors , ct = GitHubMeta(row['full_name'], ct).get_repo_contributors()
            repo_description, ct = GitHubMeta(row['full_name'], ct).get_repo_desc()
            dict_['repository'] = row['full_name']
            dict_['created_at'] = repo_description[0]['created_at']
            dict_['updated_at'] = repo_description[0]['updated_at']
            #dict_['num_commits'] =repo_commits
            #dict_['num_contributors'] = len(contributors)
            dict_['size'] = repo_description[0]['size']  
            dict_['num_stars'] = repo_description[0]['stargazers_count'] 
            dict_['num_forks'] = repo_description[0]['forks_count']
            repos.append(dict_)            
        except Exception as e:
            print(e)
            continue
            
    pd.DataFrame.from_records(repos).to_csv('repo_description.csv',index=False)

    ###########################################################################################
    keys= ['url', 'state', 'repository', 'created_at', 'updated_at', 'closed_at', 'title', 'body'] # body
    pattern_in = lambda x : True if 'cve' in x or 'vuln' in x or 'secur' in x else False
    exclude = lambda key : True if key != 'title' or key != 'body' else False
    # or 'attack' in v or 'threat' in v
    repos = []
    ct = 0

    mainline_repo =pd.read_csv('repo_description.csv')
    for index, row in mainline_repo.iterrows():
        try:
            print(row['repository'])
            repo_issues, ct = GitHubMeta(row['repository'], ct).get_issues()
            for issue in repo_issues:
                comments = ' '.join([str(comment) for comment in issue['body']])
                title = str(issue['title'])
                if pattern_in(comments) or pattern_in(title):
                    dict_ = { key: (str(issue[key]) if key in issue.keys() and exclude(key) else '')  for key in keys }
                    dict_['repository'] = row['repository']
                    dict_['title'] = title
                    dict_['comments'] = comments
                    #dict_['labels_name'] = ','.join(l['name'] for l in issue['labels']) if len(issue['labels'])>0 else ''
                    #dict_['pull_request'] = 'Pull request' if 'pull_request' in issue.keys() else 'Issue'
                    repos.append(dict_)
        except Exception as e:
            print(e)
            continue

    pd.DataFrame.from_records(repos).to_csv('vulnerability_issues.csv',index=False)

    ###########################################################################################

    mainline_repo =pd.read_csv('/content/sample_data/vulnerability_issues.csv')
    regex = ['CVE-\d{4}-\d{4,7}', '(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])']
    base_url_cve = 'https://services.nvd.nist.gov/rest/json/cve/1.0/{endpoint}?addOns=dictionaryCpes'
    base_url_cwe =  'https://www.opencve.io/api/cwe/{endpoint}'
    avg_severity = lambda x, y : x if x==y else ('high' if x=='critical' or y=='critical' else ('medium' if x=='high' or y=='high' else 'low'))  
    username    = '<opencve_userid>'
    password     = '<opencve_pass>'
    repos_mat    = defaultdict(dict)
    keys = ['title', 'comments']
    for index, row in mainline_repo.iterrows():
        try:
            curr_repo = row['repository']
            print(curr_repo)
            cves = []
            for key in keys:           
                if 'cve' in row[key]:
                    cves += list(dict.fromkeys(re.findall(regex[0], row[key])))
                else:
                    urls_ = dict.fromkeys(re.findall(regex[1], row[key]))
                    urls  = ''.join(urls_)
                    for url in urls:
                        response = requests.get(url)
                        cves += list(dict.fromkeys(re.findall(regex[0], response.text)))
            cves = list(set(cves))
            repos_mat[curr_repo]  = repos_mat[curr_repo] if curr_repo in repos_mat.keys() else []
            for cve in cves:
                response = requests.get(base_url_cve.format(endpoint=cve))
                jobj = response.json()
                # CPE dependency name and version
                dep = str(jobj['result']['CVE_Items'][0]['configurations']['nodes'][0]['cpe_match'][0]['cpe23Uri'])
                # CVE severity
                metric = jobj['result']['CVE_Items'][0]['impact']['baseMetricV3']
                severity = 'N/A'
                if metric:
                    severity = str(metric['cvssV3']['baseSeverity']).lower()
                else:
                    metric = jobj['result']['CVE_Items'][0]['impact']['baseMetricV2']
                    if metric:
                        severity = str(metric['severity']).lower()
                # CWE name
                cwe = str(jobj['result']['CVE_Items'][0]['cve']['problemtype']['problemtype_data'][0]['description'][0]['value'])
                response = requests.get(base_url_cwe.format(endpoint=cwe), auth=HTTPBasicAuth(username, password))
                jobj_ = response.json()
                vuln_name = str(jobj_['name'])
                # Vulnerability Matrix
                repos_mat[curr_repo].append({cve : [dep, vuln_name, severity]})
                #repos_mat[curr_repo] = {repos_mat[curr_repo][cve]:v for v in repos_mat[curr_repo]}.values()      
        except Exception as e:
            print(e)
            continue

    # Stats
    vuln_stats, repo_stats, repo_vuln_stats, cves = defaultdict(dict), defaultdict(dict), defaultdict(dict), []
    vuln_matrix, dep_stats, dep_repos, dep_sever = defaultdict(dict), defaultdict(dict), defaultdict(dict), defaultdict(dict)
    total_cves  = 0
    vuln_matrix['name'] = {}
    for rep, libs in repos_mat.items():
        repo_stats[rep] = len(libs)
        vuln_matrix[rep] = vuln_matrix[rep] if rep in vuln_matrix.keys() else {}
        for pair in libs:
            (k, v), = pair.items()
            vuln_matrix['name'][k] = k
            repo_vuln_stats['name'][v[1]] = v[1]
            vuln_stats[v[1]] = (vuln_stats[v[1]] + 1) if v[1] in vuln_stats.keys() else 1 
            repo_vuln_stats[rep][v[1]] = vuln_stats[v[1]]
            dep_repos[v[0]] = (dep_repos[v[0]] + [rep]) if rep in dep_repos[v[0]] else [rep] 
            dep_sever[v[0]] = avg_severity(dep_sever[v[0]], v[2]) if v[0] in dep_sever.keys() else v[2] 
            vuln_matrix[rep][k]= '(' + ','.join(v) + ')'
        total_cves  = total_cves + repo_stats[rep]

    for dep in dep_repos.keys():
        dep_stats['name'][dep] = dep
        dep_stats['count'][dep] = len(dep_sever)
        dep_stats['repos'][dep] = ','.join(dep_repos[dep])
        dep_stats['sever'][dep] = dep_sever[dep] 

    pd.DataFrame(dep_stats).to_csv('dep_stats.csv',index=False)
    pd.DataFrame(repo_vuln_stats).to_csv('repo_vuln_stats.csv',index=False)
    pd.DataFrame(vuln_stats.items()).to_csv('vuln_stats.csv',index=False)
    pd.DataFrame(repo_stats.items()).to_csv('repo_stats.csv',index=False)
    pd.DataFrame(vuln_matrix).to_csv('vuln_matrix.csv',index=False)
    
if __name__ == '__main__':
    main()

