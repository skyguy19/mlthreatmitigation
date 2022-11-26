import pandas as pd
import yaml
import csv

# 'Tactic  ID',
# 'Tactic Description',
# 'Technique ID',
# 'Technique Description',
# 'Attack ID Using Tactic',
# 'Attack Desc Using Tactic',
# 'Attack ID Using Technique',
# 'Attack Desc Using Technique'

f = open('/Users/malaklahlou/Downloads/mlthreatmitigation-main/atlas.csv', 'w')
writer = csv.writer(f)
row = ['Tactic  ID', 'Tactic Description', 'Technique ID', 'Technique Description', 'Tactics used in the Attack','Attack Desc Using Tactics', 'Techniques used in the attack', 'Attack Desc Using Technique' ]


with open('/Users/malaklahlou/Documents/GitHub/atlas-data/dist/ATLAS.yaml') as f:
    data = yaml.safe_load(f)

    first_matrix = data['matrices'][0]
    tactics = first_matrix['tactics']
    studies = data['case-studies']

    writer.writerow(row)
    techniques = first_matrix['techniques']
    for i in range(0, len(techniques)) :
        if(techniques[i].get('tactics')) : 
            s = techniques[i]['tactics'][0]
            for k in range(0, len(tactics)) :
                if(s == tactics[k]['id'] ) :
                    for l in range(0, len(studies)) :
                        procedure = studies[l]['procedure']
                        for j in range(0, len(procedure)) :
                            if(procedure[j]['tactic'] == s) :
                                writer.writerow([s, tactics[k]['description'], techniques[i]['id'], techniques[i]['description'], procedure[j]['tactic'], studies[l]['summary'], procedure[j]['technique'], studies[l]['summary']])
                            # else :
                            #     writer.writerow([s, tactics[k]['description'], techniques[i]['id'], techniques[i]['description']])
        

    
f.close()
    
