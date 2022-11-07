import csv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# We extracted here some parameters from a website for the unique cwe names to faster the process

f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/cwe.csv', 'r')
data = csv.reader(f)
#File that contains the unique cwe names
g = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/cwefull.csv', 'w')
writer = csv.writer(g)   
row=['CWE name', 'Availability', 'Confidentiality', 'Integrity', 'Access Control', 'Non-Repudiation']
writer.writerow(row)

base_url = 'https://cwe.mitre.org/data/definitions/{endpoint}.html'
for row in data :
    
        cweName = row[0]
        availability = 0
        confidentiality = 0
        integrity = 0
        accessControl = 0
        nonRepudiation = 0
  
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cwename = cweName[4:-1]
        driver.get(base_url.format(endpoint=cwename))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        elem = soup.find("div", {"id": "Common_Consequences"})
        if elem is not None:
                elem = elem.find("tbody")
                tl_div = elem.find_all('td', valign='middle')
                for result in tl_div :
                    if ("Availability" in result)& (availability==0): 
                        availability = 1                                  
                    if ("Confidentiality" in result)& (confidentiality==0) : 
                        confidentiality = 1   
                    if ("Integrity" in result)& (integrity==0) : 
                        integrity = 1
                    if ("Access Control" in result)& (accessControl==0) : 
                        accessControl = 1 
                    if ("Non-Repudiation" in result)& (nonRepudiation==0) : 
                        nonRepudiation = 1 
        
        writer.writerow([cwename, availability, confidentiality, integrity, accessControl, nonRepudiation]) 
          
g.close()