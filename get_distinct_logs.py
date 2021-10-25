import os
import pandas as pd

def get_distinct_logs(dataset_name):
    distinct_logs = []
    if(dataset_name == 'Battle and Heer'):
        provenance_log_path = 'Provenance Datasets/Battle and Heer/master_file.csv'
        df = pd.read_csv (provenance_log_path, delimiter='|')
        distinct_logs = df['interactionTypeRaw'].unique()

    elif(dataset_name == 'Liu and Heer'):
        provenance_log_path = 'Provenance Datasets/Liu and Heer/triggered-evt-logs'
        all_files = []
        triggered_files = os.listdir(provenance_log_path)
        participants = set()
        for i in triggered_files:
            t = i.split('-')
            participants.add(t[0])
            all_files.append(provenance_log_path+'/'+i)
        
        all_logs = []
        for file in all_files:
            f = open(file, 'r') 
            lines = f.readlines()
            if(file.find('mouseEvt') != -1):
                for line in lines:
                    all_logs.append(line.split(',')[4])
            else:
                for line in lines:
                    all_logs.append(line.split(',')[2])
        distinct_logs = set(all_logs)

    elif(dataset_name == 'Wall'):
        provenance_log_path = "Provenance Datasets/Wall"
        all_files = [f for f in os.listdir(provenance_log_path) if not f.startswith('.')]
        all_files = sorted(all_files)

        all_logs = []
        for i in range(0, len(all_files)):
            pathdir = provenance_log_path + '/' + all_files[i]
            li = os.listdir(pathdir)
            individual_log = provenance_log_path + '/' + all_files[i] +'/' + li[0]
            with open(individual_log) as f:
                lis = [line.split('\t') for line in f]
                for p in range(1, len(lis)):
                    all_logs.append(lis[p][5])

        distinct_logs = set(all_logs)

    elif(dataset_name == 'Lumos'):
        provenance_log_path1 = "Provenance Datasets/Lumos/AWARENESS"
        provenance_log_path2 = "Provenance Datasets/Lumos/CONTROL"
        all_files1 = [f for f in os.listdir(provenance_log_path1)]
        all_files2 = [f for f in os.listdir(provenance_log_path2)]

        all_logs = []
        for i in range(0, len(all_files1)):
            pathdir = provenance_log_path1 + '/' + all_files1[i]
            li = os.listdir(pathdir)
            individual_log = provenance_log_path1 + '/' + all_files1[i] +'/' + li[0]
            with open(individual_log) as f:
                lis = [line.split('\t') for line in f]
                for p in range(1, len(lis)):
                    all_logs.append(lis[p][7])

        for i in range(0, len(all_files2)):
            pathdir = provenance_log_path2 + '/' + all_files2[i]
            li = os.listdir(pathdir)
            individual_log = provenance_log_path2 + '/' + all_files2[i] +'/' + li[0]
            with open(individual_log) as f:
                lis = [line.split('\t') for line in f]
                for p in range(1, len(lis)):
                    all_logs.append(lis[p][7])

        distinct_logs = set(all_logs)
    
    return distinct_logs

distinct_logs = []
# distinct_logs = get_distinct_logs("Battle and Heer")
# print("Battle and Heer")
# print(len(distinct_logs))
# # print(distinct_logs)
# print("")

# distinct_logs = get_distinct_logs("Liu and Heer")
# print("Liu and Heer")
# print(len(distinct_logs))
# # print(distinct_logs)
# print("")

distinct_logs = get_distinct_logs("Wall")
print("Wall")
print(len(distinct_logs))
print(distinct_logs)
print("")

distinct_logs = get_distinct_logs("Lumos")
print("Lumos")
print(len(distinct_logs))
print(distinct_logs)