import json
import csv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def readFileaAndWrite(file, readers, writer) :
    l = open(file)
    data2 = json.load(l)

    for i in range(0, len(data2['CVE_Items'])) :
        
        # CPE dependency name and version
        dep = data2['CVE_Items'][i]['configurations']['nodes']
        if(len(dep)> 0) : 
            dep = dep[0]['cpe_match']
            if(len(dep)> 0) : 
                dep = dep[0]['cpe23Uri']
                # CVE severity
            cve = data2['CVE_Items'][i]['cve']['CVE_data_meta']['ID']
            metric = data2['CVE_Items'][i]['impact']['baseMetricV3']
            severity = 'N/A'
            if metric:
                severity = str(metric['cvssV3']['baseSeverity']).lower()
            else:
                metric = data2['CVE_Items'][i]['impact']['baseMetricV2']
                if metric:
                    severity = str(metric['severity']).lower()
        
            availability = 0
            confidentiality = 0
            integrity = 0
            accessControl = 0
            nonRepudiation = 0
            
            # CWE name
            cwe = data2['CVE_Items'][i]['cve']['problemtype']['problemtype_data'][0]['description']
            if(len(cwe) > 0) :
                cwe = cwe[0]['value']
                description = data2['CVE_Items'][i]['cve']['description']['description_data'][0]['value']
                
                #related Attacks
                relatedAttacks = []
                if ("XSS" in description) or ("cross-site" in description) : relatedAttacks.append("Stored Cross-Site Scripting (XSS) attack")
                if ("DoS" in description) or ("denial" in description) : 
                    relatedAttacks.append("Denial of Service (DoS)")
                    availability = 1
                if ("RCE" in description) or ("remote" in description) : 
                    relatedAttacks.append("Remote code execution (RCE) attack")
                if "CSRF" in description : relatedAttacks.append("Cross-site request forgery (CSRF) attack")
                if "after free" in description : relatedAttacks.append("Use-after-free attack")
                if "bypass" in description : relatedAttacks.append("Bypass authentication attack")
                if "SQL" in description : relatedAttacks.append("SQL injection attack")
                if "privilege" in description : 
                    relatedAttacks.append("Privilege esclation attack")
                    confidentiality = 1
                    integrity = 1
                    accessControl = 1
                if "RPC" in description : relatedAttacks.append(" RPC attack ")
                if ("authoriz" in description) or ("authentica" in description): 
                    confidentiality = 1
                    accessControl = 1
                if ("sensitive" in description) : 
                    integrity = 1
                if ("XML" in description): 
                    relatedAttacks.append(" XML Injection attack ")
                    confidentiality = 1
                    integrity = 1
                if ("NULL" in description): 
                    relatedAttacks.append(" NULL pointer dereference attack ")
                    confidentiality = 1
                    integrity = 1
                if ("modif" in description) or ("inject" in description): 
                    confidentiality = 1
                    accessControl = 1
                if ("integrity" in description) : integrity = 1
                if ("confidentiality" in description) : confidentiality = 1
                if ("availability" in description) : availability = 1
                if ("access control" in description) : accessControl = 1
                if ("non repudiation" in description) : nonRepudiation = 1
                if ("arbitrary code" in description) : 
                    relatedAttacks.append("Arbitrary code attack ")
                    confidentiality = 1
                    integrity = 1  
                if "vulnerability" in description[8:120] :
                    if(len(relatedAttacks)==0) :
                        relatedAttacks.append(description.partition("vulnerability")[0] + " attack")

               
            if(len(cwe) < 10) :
                for row2 in readers :
                    if(row2[0]== cwe[4:8]) :
                        availability = int(row2[1])
                        confidentiality = int(row2[2])
                        integrity = int(row2[3])
                        accessControl = int(row2[4])
                        nonRepudiation = int(row2[5])
            #Categories Path  
            categoriesPath = []      
            if (availability == 1) : categoriesPath.append("Availability")
            if(confidentiality == 1) : categoriesPath.append("Confidentiality")
            if(integrity == 1) : categoriesPath.append("Integrity")
            if(accessControl == 1) : categoriesPath.append("Access Control")
            if(nonRepudiation == 1) : categoriesPath.append("Non-Repudiation")
            categoriesPathString = ", ".join(categoriesPath)
                
            dep = str(dep[10:]).split(':')
            cpeDependecyName = dep[0]
            cpeDependecyVersion = " " 
            if(len(dep)> 2) : cpeDependecyVersion = dep[2]                
            if(len(dep)> 1): cpeDependecyName =dep[0]+':'+dep[1]             
                
            writer.writerow([cve, cwe, severity, cpeDependecyName, cpeDependecyVersion, description, ', '.join(relatedAttacks), 
                             availability, confidentiality, integrity, accessControl, nonRepudiation, categoriesPathString]) 
    
    l.close()
    
    
#File that already contains informations using the cwe name   
with open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/cwefull.csv', 'r') as b: 
    data3 = csv.reader(b)
    readers = list(data3)
    
    g = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/nvd3.csv', 'w')
    writer = csv.writer(g)   
    
    row=['CVE ID','CWE name', 'CVE severity', 'CPE dependency name ', 'CPE dependency version', 'Description' ,
         'Related attacks', 'Availability', 'Confidentiality', 'Integrity', 'Access Control', 'Non-Repudiation', 'Categories path']
    writer.writerow(row)
    
    readFileaAndWrite('/Users/malaklahlou/Downloads/mlthreatmitigation-main/nvdcve-1.1-2022.json', readers, writer)
    readFileaAndWrite('/Users/malaklahlou/Downloads/mlthreatmitigation-main/nvdcve-1.1-2021.json', readers, writer)
    readFileaAndWrite('/Users/malaklahlou/Downloads/mlthreatmitigation-main/nvdcve-1.1-recent.json', readers, writer)
    
