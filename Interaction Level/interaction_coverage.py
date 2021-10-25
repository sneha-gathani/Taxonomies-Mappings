import json
import os
from operator import itemgetter
from collections import OrderedDict

labels = json.load(open("../Mappings/interaction_level.json"))

def calculate_coverage(mapping):
    unique_interactions = len(labels[mapping])
    null_interactions = 0
    for i in labels[mapping]:
        if(labels[mapping][i]["mapping"] == "null"):
            null_interactions += 1
    return round((float(null_interactions) / float(unique_interactions)) * 100, 3)

def calculate_inverse_coverage(mapping, dataset, data):
    count = {}
    unique_interactions = labels[mapping + "-mapping"]
    for i in unique_interactions:
        count[i] = 0
    null_interactions = 0
    for i in range(0, len(data)):
        interactionTypeRaw = data[i]['interactionTypeRaw']
        embedding = labels[dataset + "-" + mapping + "-mapping"][interactionTypeRaw]["mapping"]
        if(embedding != "null"):
            count[embedding] += 1
        else:
            null_interactions += 1
    for i in count:
        count[i] = round(float(count[i]) / (len(data) - null_interactions) * 100, 3)
    return count

# Reads the three provenance datasets
def read_battleheer2019_dataset():
    path = '../Provenance Datasets/Battle and Heer/master_file.json'
    dataset = json.load(open(path))
    return dataset

def read_liuheer2014_dataset():
    path = "../Provenance Datasets/Liu and Heer/triggered-evt-logs"
    all_files = []
    a = os.listdir(path)
    for i in a:
        all_files.append(path + "/" + i)
    allLogs = []
    for i in all_files:
        file1 = open(i, 'r') 
        lines = file1.readlines()
        if(i.find('mouseEvt') != -1):
            for line in lines:
                temp = {}
                temp['interactionTypeRaw'] = line.split(',')[4]
                allLogs.append(temp)
        else:
            for line in lines:
                temp = {}
                temp['interactionTypeRaw'] = line.split(',')[2]
                allLogs.append(temp)
    return allLogs

def read_wall2020_dataset():
    path = "../Provenance Datasets/Wall"
    all_folders = [f for f in os.listdir(path) if not f.startswith('.')]
    all_files = []
    for i in all_folders:
        a = os.listdir(path + "/" + i)
        for j in a:
            all_files.append(path + "/" + i + "/" + j)
    temp = []
    for i in all_files:
        with open(i) as f:
            lis = [line.split('\t') for line in f]
            for p in range(1, len(lis)):
                dictt = {}
                dictt['interactionTypeRaw'] = lis[p][5]
                temp.append(dictt)
    return temp

def print_inverse_coverage(c):
    c = OrderedDict(sorted(c.items(), key=itemgetter(1), reverse=True))
    for i in c:
        print("{} --> {}%".format(i, c[i]))
    print("")


# Main program
if __name__ == '__main__':

    coverages = []

    # Amar et al. coverage for all 3 provenance datasets
    total = 0
    print("\033[1mAmar et al.\033[0m programmatic mapping coverage:")
    coverage = 100 - calculate_coverage("battleheer2019-amar2005-mapping")
    total += coverage
    print("Battle and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("liuheer2014-amar2005-mapping")
    total += coverage
    print("Liu and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("wall2020-amar2005-mapping")
    total += coverage
    print("Wall: {}%".format(coverage))

    coverages.append(total / 3)
    print("\033[1mAverage Amar et al. programmatic mapping coverage: \033[0m {}%".format(total / 3))
    print("")

    # Brehmer and Munzner coverage for all 3 provenance datasets
    total = 0
    print("\033[1mBrehmer and Munzner\033[0m programmatic mapping coverage:")
    coverage = 100 - calculate_coverage("battleheer2019-brehmermunzner2013-mapping")
    total += coverage
    print("Battle and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("liuheer2014-brehmermunzner2013-mapping")
    total += coverage
    print("Liu and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("wall2020-brehmermunzner2013-mapping")
    total += coverage
    print("Wall: {}%".format(coverage))

    coverages.append(total / 3)
    print("\033[1mAverage Brehmer and Munzner programmatic mapping coverage: \033[0m {}%".format(total / 3))
    print("")

    # Gotz and zhou coverage for all 3 provenance datasets
    total = 0
    print("\033[1mGotz and Zhou\033[0m programmatic mapping coverage:")
    coverage = 100 - calculate_coverage("battleheer2019-gotzzhou2009-mapping")
    total += coverage
    print("Battle and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("liuheer2014-gotzzhou2009-mapping")
    total += coverage
    print("Liu and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("wall2020-gotzzhou2009-mapping")
    total += coverage
    print("Wall: {}%".format(coverage))

    coverages.append(total / 3)
    print("\033[1mAverage Gotz and Zhou programmatic mapping coverage: \033[0m {}%".format(total / 3))
    print("")

    # Yi et al. coverage for all 3 provenance datasets
    total = 0
    print("\033[1mYi et al.\033[0m programmatic mapping coverage:")
    coverage = 100 - calculate_coverage("battleheer2019-yi2007-mapping")
    total += coverage
    print("Battle and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("liuheer2014-yi2007-mapping")
    total += coverage
    print("Liu and Heer: {}%".format(coverage))

    coverage = 100 - calculate_coverage("wall2020-yi2007-mapping")
    total += coverage
    print("Wall: {}%".format(coverage))

    coverages.append(total / 3)
    print("\033[1mAverage Yi et al. programmatic mapping coverage: \033[0m {}%".format(total / 3))
    print("")
    print("-----------------------------------------------")
    print("-----------------------------------------------")
    print("")


    # This is main program to get inverse coverage
    # Amar et al.
    print("\033[1mAmar et al. Inverse Coverage\033[0m -->")
    print("\033[1mBattle and Heer\033[0m")
    battleheer_dataset = read_battleheer2019_dataset()
    c = calculate_inverse_coverage("amar2005", "battleheer2019", battleheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mLiu and Heer\033[0m")
    liuheer_dataset = read_liuheer2014_dataset()
    c = calculate_inverse_coverage("amar2005", "liuheer2014", liuheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mWall\033[0m")
    wall_dataset = read_wall2020_dataset()
    c = calculate_inverse_coverage("amar2005", "wall2020", wall_dataset)
    print_inverse_coverage(c)
    print("-----------------------------------------------")
    print("")

    # Brehmer and Munzner
    print("\033[1mBrehmer and Munzner Distribution Coverage\033[0m:")
    print("\033[1mBattle and Heer\033[0m")
    battleheer_dataset = read_battleheer2019_dataset()
    c = calculate_inverse_coverage("brehmermunzner2013", "battleheer2019", battleheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mLiu and Heer\033[0m")
    liuheer_dataset = read_liuheer2014_dataset()
    c = calculate_inverse_coverage("brehmermunzner2013", "liuheer2014", liuheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mWall\033[0m")
    wall_dataset = read_wall2020_dataset()
    c = calculate_inverse_coverage("brehmermunzner2013", "wall2020", wall_dataset)
    print_inverse_coverage(c)
    print("-----------------------------------------------")
    print("")

    # Gotz and Zhou
    print("\033[1mGotz and Zhou Inverse Coverage\033[0m -->")
    print("\033[1mBattle and Heer\033[0m")
    battleheer_dataset = read_battleheer2019_dataset()
    c = calculate_inverse_coverage("gotzzhou2009", "battleheer2019", battleheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mLiu and Heer\033[0m")
    liuheer_dataset = read_liuheer2014_dataset()
    c = calculate_inverse_coverage("gotzzhou2009", "liuheer2014", liuheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mWall\033[0m")
    wall_dataset = read_wall2020_dataset()
    c = calculate_inverse_coverage("gotzzhou2009", "wall2020", wall_dataset)
    print_inverse_coverage(c)
    print("-----------------------------------------------")
    print("")

    # Yi et al.
    print("\033[1mYi et al. Inverse Coverage\033[0m -->")
    print("\033[1mBattle and Heer\033[0m")
    battleheer_dataset = read_battleheer2019_dataset()
    c = calculate_inverse_coverage("yi2007", "battleheer2019", battleheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mLiu and Heer\033[0m")
    liuheer_dataset = read_liuheer2014_dataset()
    c = calculate_inverse_coverage("yi2007", "liuheer2014", liuheer_dataset)
    print_inverse_coverage(c)

    print("\033[1mWall\033[0m")
    wall_dataset = read_wall2020_dataset()
    c = calculate_inverse_coverage("yi2007", "wall2020", wall_dataset)
    print_inverse_coverage(c)
    print("-----------------------------------------------")
    print("")