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

# Inner function of the wall_to_gotzzhou2009 and liuheer_to_gotzzhou2009 function
def checkWhetherSame(a, b):
    return (a['id'] == b['id'] and a['xy'] == b['xy'])

# Get gotz and wen for liu and heer dataset
def liuheer_to_gotzzhou2009(data):
    idata = []
    for index, row in data.iterrows():
        temp = {}
        temp['interactionTypeRaw'] = row['interactionTypeRaw']
        temp['interaction'] = row['gotzzhou2009']
        a = row['dimension']
        if(temp['interaction'] == "inspect" or temp['interaction'] == "change-metaphor"):
            if('-' in a):
                t = a.split('-')
                if(t[0] == "geo" or t[0] == "scatterplot"):
                    temp['dimension'] = t[2]
                else:
                    temp['dimension'] = t[1]
            else:
                temp['dimension'] = "null"
        else:
            temp['dimension'] = "null"
        sequence_coverage_labels = json.load(open("Mappings/sequence_level.json"))
        temp['sequence'] = sequence_coverage_labels["gotzzhou2009-gotzwen2009-sequences"][temp['interaction']]
        idata.append(temp)
        
    labelClasses = []
    i = 0
    while(i < len(idata)):
        if(idata[i]['sequence'] != "inspect"):
            labelClasses.append(idata[i]['interaction'])
            i += 1
        elif(idata[i]['dimension'] == "null"):
            labelClasses.append("null")
            i += 1
        else:
            if(i < len(idata) - 2 and idata[i]['dimension'] == idata[i + 1]['dimension']):
                labelClasses.append("inspectsame")
                i += 1
            else:
                labelClasses.append("inspectdiff")
                i += 1
    return labelClasses

# Get gotz and wen for wall dataset
def wall_to_gotzzhou2009(data):
    idata = []
    for index, row in data.iterrows():
        temp = {}
        a = row['input_type']
        b = a.split("'data'")
        if(row['interactionTypeRaw'] == 'filter_changed' or row['interactionTypeRaw'] == 'change_attribute_distribution' or row['interactionTypeRaw'] == 'change_attribute_distribution_results' or row['interactionTypeRaw'] == 'axes_attribute_changed'):
            temp['id'] = 'null'
            temp['xy'] = 'null'
        else:
            idd = b[1].split("'id': ")[1]
            idd = idd.split(',')[0]
            temp['id'] = idd

            if(row['interactionTypeRaw'] == 'add_to_list_via_scatterplot_click' or row['interactionTypeRaw'] == 'mouseover' or row['interactionTypeRaw'] == 'mouseout'):
                t = b[1].split("'x': ")[1]
                xy = t.split(", 'eventX'")[0]
                xy = "{'x': " + xy
                temp['xy'] = xy
            else:
                t = b[1].split(", 'id':")[0]
                xy = t[2:]
                temp['xy'] = xy
        temp['interaction'] = row['interactionTypeRaw']
        temp['gotzzhou2009'] = row['gotzzhou2009']
        idata.append(temp)

    innerseq = []
    i = 0
    iteratedPoints = set()
    
    while(i < len(idata)):
        interactionMapping = idata[i]['gotzzhou2009']
        if(interactionMapping == 'null'):
            i += 1
        elif(interactionMapping != 'inspect' or interactionMapping != 'change-metaphor'):
            innerseq.append(interactionMapping)
            i += 1
        else:
            # Check this for wall2020
            if(i < len(idata) - 2 and (idata[i]['interaction'] == 'mouseover' and idata[i + 1]['interaction'] == 'add_to_list_via_scatterplot_click' and idata[i + 2]['interaction'] == 'mouseout')):
                if(checkWhetherSame(idata[i], idata[i + 1]) and checkWhetherSame(idata[i], idata[i + 2])):
                    p = idata[i]['id'] + "|" + idata[i]['xy']
                    # Check if this point was already visited. If yes then its inspectsame, otherwise its inspectdiff
                    if(p in iteratedPoints):
                        innerseq.append("inspectsame")
                    else:
                        innerseq.append("inspectdiff")
                    iteratedPoints.add(p)
                    i += 3
                else:
                    i += 1
            elif(i < len(idata) - 1 and ((idata[i]['interaction'] == 'mouseover' and idata[i + 1]['interaction'] == 'mouseout') or (idata[i]['interaction'] == 'mouseover_from_list' and idata[i + 1]['interaction'] == 'mouseout_from_list'))):
                if(checkWhetherSame(idata[i], idata[i + 1])):
                    p = idata[i]['id'] + "|" + idata[i]['xy']
                    # Check if this point was already visited. If yes then its inspectsame, otherwise its inspectdiff
                    if(p in iteratedPoints):
                        innerseq.append("inspectsame")
                    else:
                        innerseq.append("inspectdiff")
                    iteratedPoints.add(p)
                    i += 2
                else:
                    i += 1
            elif(i < len(idata) - 2 and (idata[i]['interaction'] == 'mouseover' and idata[i + 1]['interaction'] == 'remove_from_list_via_card_click' and idata[i + 2]['interaction'] == 'mouseout')):
                if(checkWhetherSame(idata[i], idata[i + 1]) and checkWhetherSame(idata[i], idata[i + 2])):
                    p = idata[i]['id'] + "|" + idata[i]['xy']
                    # Check if this point was already visited. If yes then its inspectsame, otherwise its inspectdiff
                    if(p in iteratedPoints):
                        innerseq.append("inspectsame")
                    else:
                        innerseq.append("inspectdiff")
                    iteratedPoints.add(p)
                    i += 3
                else:
                    i += 1
            elif(i < len(idata) - 1 and (idata[i]['interaction'] == 'mouseover_from_list' and idata[i + 1]['interaction'] == 'remove_from_list_via_list_item_click')):
                if(checkWhetherSame(idata[i], idata[i + 1])):
                    p = idata[i]['id'] + "|" + idata[i]['xy']
                    # Check if this point was already visited. If yes then its inspectsame, otherwise its inspectdiff
                    if(p in iteratedPoints):
                        innerseq.append("inspectsame")
                    else:
                        innerseq.append("inspectdiff")
                    iteratedPoints.add(p)
                    i += 2
                else:
                    i += 1
            else:
                i += 1
    return innerseq

# Get gotz and wen for battle and heer dataset
def get_gotz_wen_battleheer2019(data):
    st = []
    for j in range(0, len(data)):
        if(data[j]['gotzzhou2009'] == 'inspect' or data[j]['gotzzhou2009'] == 'change-metaphor'):
            st.append(data[j]['state'])
        else:
            st.append('null')
    subseq = []
    for j in range(0, len(data)):
        if(data[j]['gotzzhou2009'] != 'inspect' and data[j]['gotzzhou2009'] != 'change-metaphor' and data[j]['gotzzhou2009'] != 'null'):
            subseq.append(data[j]['gotzzhou2009'])
        else:
            currst = st[j]
            if(currst in st[:j]):
                subseq.append("inspectsame")
            else:
                subseq.append("inspectdiff")
    return subseq

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
    gotzwen_expressions = list(sequence_mapping["gotzzhou2009-gotzwen2009-mapping"]["expression"].keys())
    data = combine(data)
    combine_gotzwen = re.sub(gotzwen_expressions[0], ' scan ', data)
    combine_gotzwen = re.sub(gotzwen_expressions[1], ' flip ', combine_gotzwen)
    combine_gotzwen = re.sub(gotzwen_expressions[2], ' swap ', combine_gotzwen)
    combine_gotzwen = re.sub(gotzwen_expressions[3], ' drill-down ', combine_gotzwen)
    gotzwen = disjoint(combine_gotzwen)
    return gotzwen

final_data = []

def add_to_final_data(dataset, internal_dataset, user_id, task, gotzzhou2009_interactions, gotzzhou2009_guo2015, gotzzhou2009_shneiderman1996, gotzzhou2009_gotzwen2009):
    individual_data_point = {}
    individual_data_point['dataset'] = dataset
    individual_data_point['internal_dataset'] = internal_dataset
    individual_data_point['user_id'] = user_id
    individual_data_point['task'] = task
    individual_data_point['gotzzhou2009_interactions'] = gotzzhou2009_interactions
    individual_data_point['gotzzhou2009_guo2015'] = gotzzhou2009_guo2015
    individual_data_point['gotzzhou2009_shneiderman1996'] = gotzzhou2009_shneiderman1996
    individual_data_point['gotzzhou2009_gotzwen2009'] = gotzzhou2009_gotzwen2009
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

                gotzwenData = []
                for index, row in individual_task.iterrows():
                    temp = {}
                    temp['gotzzhou2009'] = battleHeerToGZInteraction(row['interactionTypeRaw'])
                    temp['interactionTypeRaw'] = row['interactionTypeRaw']
                    temp['state'] = row['state']
                    temp['seqId'] = row['seqId']
                    gotzwenData.append(temp)
                prep_for_gotzwen = get_gotz_wen_battleheer2019(gotzwenData)
                gotzzhou2009_gotzwen2009 = convert_to_gotzwen2009(prep_for_gotzwen)
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
                            temp['gotzzhou2009'] = liuHeerToGZInteraction(temp['interaction'])
                            allLogs.append(temp)
                    else:
                        for line in lines:
                            temp = {}
                            temp['file'] = a
                            temp['timestamp'] = line.split(',')[1]
                            temp['interaction'] = line.split(',')[2]
                            temp['gotzzhou2009'] = liuHeerToGZInteraction(temp['interaction'])
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
                            temp['gotzzhou2009'] = liuHeerToGZInteraction(temp['interactionTypeRaw'])
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
                            temp['gotzzhou2009'] = liuHeerToGZInteraction(temp['interactionTypeRaw'])
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
            gotzzhou2009_interactions = liuheer_to_gotzzhou2009(individual_task)
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
                dictt['gotzzhou2009'] = wallToGZInteraction(lis[p][5])
                temp.append(dictt)
        sortedAllLogs = sorted(temp, key = lambda ii: (ii['processed_at']))
        df = pd.DataFrame.from_dict(sortedAllLogs)
        interactions = list(df['interactionTypeRaw'])
        gotzzhou2009_interactions = []
        for i in interactions:
            gotzzhou2009_interactions.append(wallToGZInteraction(i))
        gotzzhou2009_guo2015 = convert_to_guo2015(gotzzhou2009_interactions)
        gotzzhou2009_shneiderman1996 = convert_to_shneiderman1996(gotzzhou2009_interactions)
        gotzzhou2009_interactions = wall_to_gotzzhou2009(df)
        gotzzhou2009_gotzwen2009 = convert_to_gotzwen2009(gotzzhou2009_interactions)
        add_to_final_data("Wall2020", '-', p, '-', gotzzhou2009_interactions, gotzzhou2009_guo2015, gotzzhou2009_shneiderman1996, gotzzhou2009_gotzwen2009)
        
process_battleheer2019()
process_liuheer2014()
process_wall2020()
df = pd.DataFrame.from_dict(final_data)
print(len(df))
df.to_csv('dataset_for_task_level.csv')