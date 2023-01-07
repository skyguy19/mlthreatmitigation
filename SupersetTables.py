import csv
from collections import Counter

def readUniqueColumn(readers, column, firstrow, file):
    h = open(file, 'w')
    writer = csv.writer(h)   
    writer.writerow(firstrow)
    techniques = []

    for reader in readers[1:] :
        attacks = reader[column].replace('[', '').replace(']', '').split(',') 
        for attack in attacks :
            if(attack != "" and attack != "[]") :
                techniques.append(attack.lower().rstrip().lstrip().rstrip("'").lstrip("'").rstrip('"').lstrip('"')) 

    counter = Counter(techniques)
    resultList = list(map(list, counter.items()))
    writer.writerows(resultList)
    h.close()
        

class NVDInformations :  

    f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/nvd3.csv', 'r')
    data = csv.reader(f)
    readers = list(data)
    
    # NVD Unique Related attacks and their counts 
    readUniqueColumn(readers, 6, ["Related Attacks", "Count"], '/Users/malaklahlou/Downloads/mlthreatmitigation-main/uniqueRelatedAttacks.csv') 
    
    # NVD Unique CPE dependency and their counts
    readUniqueColumn(readers, 3, ["CPE Dependency Name", "Count"], '/Users/malaklahlou/Downloads/mlthreatmitigation-main/uniqueDependencyNames.csv')



class informationsAI :

    def domainOccurences(readers) :
        h = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI_Incident_Informations.csv', 'w')
        writer = csv.writer(h)   

        writer.writerow(["Domain", "Count"])
        allDomain = []

        for reader in readers[1:] :
            domainsOfAnAttack = reader[6].split(',') 
            for domain in domainsOfAnAttack :
                if(domain != "") :
                    splitDomain = domain.split('/')
                    for split in splitDomain :
                        if(split != "") :
                            allDomain.append(split.lower().rstrip().lstrip()) 

        counter = Counter(allDomain)
        resultList = list(map(list, counter.items()))
        writer.writerows(resultList)

        h.close()
        

    def counts(readers) :
        h = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AIIncidentsStatistiques.csv', 'w')
        writer = csv.writer(h)
        writer.writerow(["Domains", "Count"])
        allDomains = []

        for reader in readers[1:] :
            domainsOfAnAttack = reader[12].split(',') 
            for domain in domainsOfAnAttack :
                if("data related security related" == domain.lower().rstrip().lstrip()):
                    allDomains.append("data related")
                    allDomains.append("security related")
                elif(domain != "") :
                    allDomains.append(domain.lower().rstrip().lstrip()) 

        counter = Counter(allDomains)
        resultList = list(map(list, counter.items()))
        writer.writerows(resultList)

        h.close()

# remove "data related security related" from the original file
    f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI Incident2.csv', 'r')
    data = csv.reader(f)
    readers = list(data)
    domainOccurences(readers)
    # Time Line Incidents (number of incidents by year)
    readUniqueColumn(readers, 3, ["Year", "Number of accidents"], '/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI_Incident_InformationsTimeLine.csv')

    counts(readers)


class tacticsandtechniquesusedbyAI :
        
    f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI Incident2.csv', 'r')
    data = csv.reader(f)
    readers = list(data)

    # Unique tactics used by AI Incident with their count
    readUniqueColumn(readers, 13, ["Techniques", "Count"], '/Users/malaklahlou/Downloads/mlthreatmitigation-main/TacticsUsedByAIIncident.csv')

    # Unique techniques used by AI Incident with their count
    readUniqueColumn(readers, 14, ["Techniques", "Count"], '/Users/malaklahlou/Downloads/mlthreatmitigation-main/TechniquesUsedByAIIncident.csv')



