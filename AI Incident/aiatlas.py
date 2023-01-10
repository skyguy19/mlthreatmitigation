import csv

f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI Incident - Feuille 1.csv', 'r')
data = csv.reader(f)
readers = list(data)
g = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/atlas.csv', 'r')
data2 = csv.reader(g)
readers2 = list(data2)
h = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/AI Incident2.csv', 'w')
writer = csv.writer(h)   

writer.writerow(readers[0])

for reader in readers[1:] :
    techniques = reader[8].split(',')
    list_techniques = []
    list_tactics = []
    for technique in techniques :
        if(technique != "") :
            for reader2 in readers2[1:] :
                if(technique == "Data Collection") :
                    if("data collect" in reader2[5]) and (reader2[4] not in list_techniques):
                        list_techniques.append(reader2[4])
                        if(reader2[1] not in list_tactics):
                            list_tactics.append(reader2[1])
                if("Facial" in technique) or ("Face" in technique) or ("facial" in reader[5]):
                    if(("face" in reader2[5]) or ("facial" in reader2[5]) ) and (reader2[4] not in list_techniques):
                        list_techniques.append(reader2[4])
                        if(reader2[1] not in list_tactics):
                            list_tactics.append(reader2[1])
                if (technique in reader2[5]) and (reader2[4] not in list_techniques):
                    list_techniques.append(reader2[4])
                    if (reader2[1] not in list_tactics):
                        list_tactics.append(reader2[1])
                l = technique.split(' ')
                for l1 in l :
                    if(l1 != "" and l1!= "learning" and l1 != "attack" and l1 != "manipulating" and l1 != "collection") :
                        if (l1 in reader2[5]) and (reader2[4] not in list_techniques):
                            list_techniques.append(reader2[4])
                            if (reader2[1] not in list_tactics):
                                list_tactics.append(reader2[1])
                        
    e = reader[:-2]
    e.append(list_tactics)
    e.append(list_techniques)
    writer.writerow(e)
    
h.close()
