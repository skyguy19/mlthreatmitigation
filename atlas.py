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
row1 = ['Tactic  ID','Tactic Name','Tactic Description']
row2 =['Technique ID', 'Technique Name','Technique Description']
row3 = ['Attack ID', 'Attack Name','Tactics used in the Attack', 'Techniques used in the attack']
#row4 = ['Attack ID Using Technique', 'Attack Name','Attack Desc Using Technique']

with open('/Users/malaklahlou/Documents/GitHub/atlas-data/dist/ATLAS.yaml') as f:
    # Parse YAML
    data = yaml.safe_load(f)

    first_matrix = data['matrices'][0]
    tactics = first_matrix['tactics']

    writer.writerow(row1)
    for i in range(0, len(tactics)) :
        writer.writerow([tactics[i]['id'], tactics[i]['name'], tactics[i]['description']])
    
    #writer.writerow("   ")
    writer.writerow("   ")
    
    writer.writerow(row2)
    techniques = first_matrix['techniques']
    for i in range(0, len(techniques)) :
        writer.writerow([techniques[i]['id'], techniques[i]['name'], techniques[i]['description']])
        
    #writer.writerow("   ")
    writer.writerow("  ")


    studies = data['case-studies']
    writer.writerow(row3)
    for i in range(0, len(studies)) :
        procedure = studies[i]['procedure']
        #writer.writerow([studies[i]['id'], studies[i]['name'], studies[i]['summary']])
        rowTacticsUsed = []
        rowTechniquesUsed = []
        for j in range(0, len(procedure)) :
            rowTacticsUsed.append(procedure[j]['tactic'])
            rowTechniquesUsed.append(procedure[j]['technique'])
        
        writer.writerow([studies[i]['id'], studies[i]['name'], studies[i]['summary'], rowTacticsUsed, rowTechniquesUsed])
    
f.close()
    