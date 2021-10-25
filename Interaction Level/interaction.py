import json
import os

# Reading the interaction level mapping from the json file
interaction_mapping = json.load(open("../Mappings/interaction_level.json"))

# Gives the Amar et al. taxonomy interaction category for Battle and Heer interaction logs
def battleHeerToAmarInteraction(interactionTypeRaw):
    return interaction_mapping["battleheer2019-amar2005-mapping"][interactionTypeRaw]["mapping"]

# Gives the Amar et al. taxonomy interaction category for Liu and Heer interaction logs
def liuHeerToAmarInteraction(interactionTypeRaw):
    return interaction_mapping["liuheer2014-amar2005-mapping"][interactionTypeRaw]["mapping"]

# Gives the Amar et al. taxonomy interaction category for Wall interaction logs
def wallToAmarInteraction(interactionTypeRaw):
    return interaction_mapping["wall2020-amar2005-mapping"][interactionTypeRaw]["mapping"]

# Gives the Brehmer and Munzner taxonomy interaction category for Battle and Heer interaction logs
def battleHeerToBrehmerInteraction(interactionTypeRaw):
    return interaction_mapping["battleheer2019-brehmermunzner2013-mapping"][interactionTypeRaw]["mapping"]

# Gives the Brehmer and Munzner interaction level label for immens logs
def liuHeerToBrehmerInteraction(interactionType):
    return interaction_mapping["liuheer2014-brehmermunzner2013-mapping"][interactionType]["mapping"]

# Gives the Brehmer and Munzner interaction level label for emilywall logs
def wallToBrehmerInteraction(interactionType):
    return interaction_mapping["wall2020-brehmermunzner2013-mapping"][interactionType]["mapping"]

# Gives the Gotz and Zhou taxonomy interaction category for Battle and Heer interaction logs
def battleHeerToGZInteraction(interactionTypeRaw):
    return interaction_mapping["battleheer2019-gotzzhou2009-mapping"][interactionTypeRaw]["mapping"]

# Gives the Gotz and Zhou taxonomy interaction category for Liu and Heer interaction logs
def liuHeerToGZInteraction(interactionType):
    return interaction_mapping["liuheer2014-gotzzhou2009-mapping"][interactionType]["mapping"]

# Gives the Gotz and Zhou taxonomy interaction category for Wall interaction logs
def wallToGZInteraction(interactionType):
    return interaction_mapping["wall2020-gotzzhou2009-mapping"][interactionType]["mapping"]

# Gives the Yi et al. taxonomy interaction category for Battle and Heer interaction logs
def battleHeerToYiInteraction(interactionTypeRaw):
    return interaction_mapping["battleheer2019-yi2007-mapping"][interactionTypeRaw]["mapping"]

# Gives the Yi et al. taxonomy interaction category for Liu and Heer interaction logs
def liuHeerToYiInteraction(interactionType):
    return interaction_mapping["liuheer2014-yi2007-mapping"][interactionType]["mapping"]

# Gives the Yi et al. taxonomy interaction category for Wall interaction logs
def wallToYiInteraction(interactionType):
    return interaction_mapping["wall2020-yi2007-mapping"][interactionType]["mapping"]


# Main program
if __name__ == '__main__':
    # Enter provenance log dataset and interaction level taxonomy 
    dataset = input('Enter a provenance dataset from the following: Battle and Heer, Liu and Heer and Wall')
    taxonomy = input('Enter an interaction level taxonomy from the following: Amar, Brehmer and Munzner, Gotz and Zhou, Yi')
    mapped_data = []

    # Get the interaction level mappings for Battle and Heer provenance log dataset
    if(dataset == 'Battle and Heer'):
        path = '../Provenance Datasets/Battle and Heer/master_file.json'
        tableauFile = json.load(open(path))
        allData = []
        for i in range(0, len(tableauFile)):
            interactionTypeRaw = tableauFile[i]['interactionTypeRaw']
            allData.append(interactionTypeRaw)

        if(taxonomy == 'Amar'):
            for i in range(0, len(allData)):
                mapped_data.append(battleHeerToAmarInteraction(allData[i]))
        elif(taxonomy == 'Brehmer and Munzner'):
            for i in range(0, len(allData)):
                mapped_data.append(battleHeerToBrehmerInteraction(allData[i]))
        elif(taxonomy == 'Gotz and Zhou'):
            for i in range(0, len(allData)):
                mapped_data.append(battleHeerToGZInteraction(allData[i]))
        elif(taxonomy == 'Yi'):
            for i in range(0, len(allData)):
                mapped_data.append(battleHeerToYiInteraction(allData[i]))
        else:
            print("Taxonomy not mapped currently!")
    
    # Get the interaction level mappings for Liu and Heer provenance log dataset
    elif(dataset == 'Liu and Heer'):
        path = "../Provenance Datasets/Liu and Heer/triggered-evt-logs"
        all_files = []
        triggeredParticipantFiles = os.listdir(path)
        participants = set()
        for i in triggeredParticipantFiles:
            t = i.split('-')
            participants.add(t[0])
            all_files.append(path+'/'+i)

        allData = []
        for a in all_files:
            file1 = open(a, 'r') 
            lines = file1.readlines()
            if(a.find('mouseEvt') != -1):
                for line in lines:
                    allData.append(line.split(',')[4])
            else:
                for line in lines:
                    allData.append(line.split(',')[2])

        if(taxonomy == 'Amar'):
            for i in range(0, len(allData)):
                mapped_data.append(liuHeerToAmarInteraction(allData[i]))
        elif(taxonomy == 'Brehmer and Munzner'):
            for i in range(0, len(allData)):
                mapped_data.append(liuHeerToBrehmerInteraction(allData[i]))
        elif(taxonomy == 'Gotz and Zhou'):
            for i in range(0, len(allData)):
                mapped_data.append(liuHeerToGZInteraction(allData[i]))
        elif(taxonomy == 'Yi'):
            for i in range(0, len(allData)):
                mapped_data.append(liuHeerToYiInteraction(allData[i]))
        else:
            print("Taxonomy not mapped currently!")

    # Get the interaction level mappings for Wall provenance log dataset
    elif(dataset == 'Wall'):
        path = "../Provenance Datasets/Wall"
        all_files = [f for f in os.listdir(path) if not f.startswith('.')]
        all_files = sorted(all_files)

        allData = []
        for i in range(0, len(all_files)):
            pathdir = '../Provenance Datasets/Wall/' + all_files[i]
            li = os.listdir(pathdir)
            path = '../Provenance Datasets/Wall/' + all_files[i] +'/' + li[0]
            with open(path) as f:
                lis = [line.split('\t') for line in f]
                for p in range(1, len(lis)):
                    allData.append(lis[p][5])

        if(taxonomy == 'Amar'):
            for i in range(0, len(allData)):
                mapped_data.append(wallToAmarInteraction(allData[i]))
        elif(taxonomy == 'Brehmer and Munzner'):
            for i in range(0, len(allData)):
                mapped_data.append(wallToBrehmerInteraction(allData[i]))
        elif(taxonomy == 'Gotz and Zhou'):
            for i in range(0, len(allData)):
                mapped_data.append(wallToGZInteraction(allData[i]))
        elif(taxonomy == 'Yi'):
            for i in range(0, len(allData)):
                mapped_data.append(wallToYiInteraction(allData[i]))
        else:
            print("Taxonomy not mapped currently!")

    else:
        print("Provenance Dataset not mapped to interaction level taxonomies!")

    # Make an interaction_embeddings.txt file with the interaction level embeddings found
    with open('interaction_embeddings.txt', 'w') as f:
        f.write(json.dumps(mapped_data))
    print('Interaction level programmatic mappings made and added to interaction_embeddings.txt file')