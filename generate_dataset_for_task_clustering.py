import os
import pandas as pd
import json
import re


interaction_mapping = json.load(open("Mappings/interaction_level.json"))
# Gives the Gotz and Zhou taxonomy interaction category for Battle and Heer interaction logs
def battleHeerToGZInteraction(interactionTypeRaw):
    return interaction_mapping["battleheer2019-gotzzhou2009-mapping"][interactionTypeRaw]["mapping"]

# Gives the Gotz and Zhou taxonomy interaction category for Liu and Heer interaction logs
def liuHeerToGZInteraction(interactionType):
    return interaction_mapping["liuheer2014-gotzzhou2009-mapping"][interactionType]["mapping"]

# Gives the Gotz and Zhou taxonomy interaction category for Wall interaction logs
def wallToGZInteraction(interactionType):
    return interaction_mapping["wall2020-gotzzhou2009-mapping"][interactionType]["mapping"]

def disjoint(data):
    interactions = ["filter", "inspect", "query", "restore", "brush", "change-metaphor", "change-range", "merge", "sort", "split", "annotate", "bookmark", "create", "modify", "remove", "delete", "edit", "redo", "revisit", "undo"]
    for i in interactions:
        data = re.sub(i, ' ' + i + ' ', data)
    data = re.sub('  ', ' ', data)
    disjoint = data.split()
    return disjoint

def combine(data):
    res = ""
    for d in data:
        if(d != "null"):
            res += d
    return res

def get_count_battleheer2019(data, expression):
    return len(re.findall(expression, data))

sequence_mapping = json.load(open("Mappings/sequence_level.json"))
def convert_to_guo2015(data):
    guo = []
    guo_expressions = list(sequence_mapping["gotzzhou2009-guo2015-mapping"]["expression"].keys())
    data = combine(data)
    combine_guo = re.sub(guo_expressions[0], ' sampling ', data)
    combine_guo = re.sub(guo_expressions[1], ' locating ', combine_guo)
    combine_guo = re.sub(guo_expressions[2], ' elaborating ', combine_guo)
    combine_guo = re.sub(guo_expressions[3], ' orienting ', combine_guo)
    guo = disjoint(combine_guo)
    return guo

def convert_to_shneiderman1996(data):
    shneiderman = []
    shneiderman_expressions = sequence_mapping["gotzzhou2009-shneiderman1996-mapping"]["expression"]
    data = combine(data)
    combine_shneiderman = re.sub(shneiderman_expressions, ' ISM ', data)
    shneiderman = disjoint(combine_shneiderman)
    return shneiderman

def convert_to_gotzwen2009(data):
    gotzwen = []
    return gotzwen

final_data = []

def add_to_final_data(dataset, internal_dataset, user_id, task, brehmermunzner2013_interactions, brehmermunzner2013_guo2015, brehmermunzner2013_shneiderman1996, brehmermunzner2013_gotzwen2009):
    individual_data_point = {}
    individual_data_point['dataset'] = dataset
    individual_data_point['internal_dataset'] = internal_dataset
    individual_data_point['user_id'] = user_id
    individual_data_point['task'] = task
    individual_data_point['brehmermunzner2013_interactions'] = brehmermunzner2013_interactions
    individual_data_point['brehmermunzner2013_guo2015'] = brehmermunzner2013_guo2015
    individual_data_point['brehmermunzner2013_shneiderman1996'] = brehmermunzner2013_shneiderman1996
    # individual_data_point['brehmermunzner2013_gotzwen2009'] = brehmermunzner2013_gotzwen2009
    final_data.append(individual_data_point)

def process_battleheer2019():
    path = 'Provenance Datasets/Battle and Heer/master_file.json'
    tableauFile = json.load(open(path))
    
    certainUserIDLogs = {}
    
    for i in range(0, len(tableauFile)):
        userId = tableauFile[i]['userid']
        if userId in certainUserIDLogs.keys():
            certainUserIDLogs[userId].append(tableauFile[i])
        else:
            certainUserIDLogs[userId] = []
            certainUserIDLogs[userId].append(tableauFile[i])

    # Take participant ID, dataset as input
    s = [sub['userid'] for sub in tableauFile]
    unique_userid = sorted(list(set(s)))
    
    for p in unique_userid:
        cnt1 = 0
        cnt2 = 0
        cnt3 = 0
        for i in range(0, len(certainUserIDLogs[p])):
            if(certainUserIDLogs[p][i]['dataset'] == 'birdstrikes1'):
                cnt1 += 1
            elif(certainUserIDLogs[p][i]['dataset'] == 'faa1'):
                cnt2 += 1
            else:
                cnt3 += 1
                
        unique_dataset = []
        if(cnt1 > 0):
            unique_dataset.append('birdstrikes1')
        if(cnt2 > 0):
            unique_dataset.append('faa1')
        if(cnt3 > 0):
            unique_dataset.append('weather1')
        
        for d in unique_dataset:
            participantIDDataset = certainUserIDLogs[p]
            logDataset = []
            for i in range(0, len(participantIDDataset)):
                if(participantIDDataset[i]['dataset'] == d):
                    logDataset.append(participantIDDataset[i])
            df = pd.DataFrame.from_dict(logDataset)
            uid = df['userid'].unique()
            tasks = df['task'].unique()
            for t in tasks:
                individual_task = df['task'] == t
                individual_task = df[individual_task].sort_values(by='timestamp', ascending=True)
                interactions = list(individual_task['interactionTypeRaw'])
                gotzzhou2009_interactions = []
                for i in interactions:
                    gotzzhou2009_interactions.append(battleHeerToGZInteraction(i))
                gotzzhou2009_guo2015 = convert_to_guo2015(gotzzhou2009_interactions)
                gotzzhou2009_shneiderman1996 = convert_to_shneiderman1996(gotzzhou2009_interactions)
                gotzzhou2009_gotzwen2009 = convert_to_gotzwen2009(gotzzhou2009_interactions)
                add_to_final_data("BattleHeer2019", d, uid[0], t, gotzzhou2009_interactions, gotzzhou2009_guo2015, gotzzhou2009_shneiderman1996, gotzzhou2009_gotzwen2009)

def process_liuheer2014():
    path = "Provenance Datasets/Liu and Heer/triggered-evt-logs"
    all_files = []
    triggeredParticipantFiles = os.listdir(path)
    participants = set()
    for i in triggeredParticipantFiles:
        t = i.split('-')
        participants.add(t[0])
        all_files.append(path+'/'+i)

    participants = sorted(participants)
    dictionary = {}

    for i in participants:
        if i in dictionary.keys():
            allLogs = []
            for a in all_files:
                if(a.find(i) != -1):
                    file1 = open(a, 'r') 
                    lines = file1.readlines()
                    if(a.find('mouseEvt') != -1):
                        for line in lines:
                            temp = {}
                            temp['file'] = a
                            temp['timestamp'] = line.split(',')[1]
                            temp['interaction'] = line.split(',')[4]
                            allLogs.append(temp)
                    else:
                        for line in lines:
                            temp = {}
                            temp['file'] = a
                            temp['timestamp'] = line.split(',')[1]
                            temp['interaction'] = line.split(',')[2]
                            allLogs.append(temp)
            sortedAllLogs = sorted(allLogs, key = lambda p: (p['timestamp']))
            dictionary[i] = sortedAllLogs
        else:
            dictionary[i] = 0
            allLogs = []
            for a in all_files:
                if(a.find(i) != -1):
                    file1 = open(a, 'r') 
                    lines = file1.readlines()
                    if(a.find('mouseEvt') != -1):
                        for line in lines:
                            temp = {}
                            temp['participant'] = line.split(',')[0]
                            t = a.split('/')[3]
                            temp['task'] = t.split('-')[1]
                            temp['timestamp'] = line.split(',')[1]
                            temp['interactionTypeRaw'] = line.split(',')[4]
                            temp['dimension'] = line.split(',')[5]
                            allLogs.append(temp)
                    else:
                        for line in lines:
                            temp = {}
                            temp['participant'] = line.split(',')[0]
                            t = a.split('/')[3]
                            temp['task'] = t.split('-')[1]
                            temp['timestamp'] = line.split(',')[1]
                            temp['interactionTypeRaw'] = line.split(',')[2]
                            temp['dimension'] = line.split(',')[3]
                            allLogs.append(temp)
            sortedAllLogs = sorted(allLogs, key = lambda p: (p['timestamp']))
            dictionary[i] = sortedAllLogs

    for i in participants:
        data = dictionary[i]
        send = []
        for d in data:
            send.append(d)
        df = pd.DataFrame.from_dict(send)
        tasks = df['task'].unique()
        for t in tasks:
            individual_task = df['task'] == t
            individual_task = df[individual_task].sort_values(by='timestamp', ascending=True)
            interactions = list(individual_task['interactionTypeRaw'])
            gotzzhou2009_interactions = []
            for i in interactions:
                gotzzhou2009_interactions.append(liuHeerToGZInteraction(i))
            gotzzhou2009_guo2015 = convert_to_guo2015(gotzzhou2009_interactions)
            gotzzhou2009_shneiderman1996 = convert_to_shneiderman1996(gotzzhou2009_interactions)
            gotzzhou2009_gotzwen2009 = convert_to_gotzwen2009(gotzzhou2009_interactions)
            add_to_final_data("LiuHeer2014", t, i, '-', gotzzhou2009_interactions, gotzzhou2009_guo2015, gotzzhou2009_shneiderman1996, gotzzhou2009_gotzwen2009)
        
def process_wall2020():
    path = "Provenance Datasets/Wall"
    all_files = [f for f in os.listdir(path) if not f.startswith('.')]

    all_files = sorted(all_files)

    for i in range(0, len(all_files)):
        pathdir = 'Provenance Datasets/Wall/' + all_files[i]
        li = os.listdir(pathdir)
        path = 'Provenance Datasets/Wall/' + all_files[i] +'/' + li[0]
        temp = []
        with open(path) as f:
            lis = [line.split('\t') for line in f]
            for p in range(1, len(lis)):
                dictt = {}
                dictt['participant'] = all_files[i]
                dictt['interactionTypeRaw'] = lis[p][5]
                dictt['processed_at'] = lis[p][8]
                dictt['input_type'] = lis[p][4]
                temp.append(dictt)
        sortedAllLogs = sorted(temp, key = lambda ii: (ii['processed_at']))
        df = pd.DataFrame.from_dict(sortedAllLogs)
        interactions = list(df['interactionTypeRaw'])
        gotzzhou2009_interactions = []
        for i in interactions:
            gotzzhou2009_interactions.append(wallToGZInteraction(i))
        gotzzhou2009_guo2015 = convert_to_guo2015(gotzzhou2009_interactions)
        gotzzhou2009_shneiderman1996 = convert_to_shneiderman1996(gotzzhou2009_interactions)
        gotzzhou2009_gotzwen2009 = convert_to_gotzwen2009(gotzzhou2009_interactions)
        add_to_final_data("Wall2020", '-', p, '-', gotzzhou2009_interactions, gotzzhou2009_guo2015, gotzzhou2009_shneiderman1996, gotzzhou2009_gotzwen2009)
        
process_battleheer2019()
process_liuheer2014()
process_wall2020()
df = pd.DataFrame.from_dict(final_data)
print(len(df))
df.to_csv('dataset_for_task_level.csv')