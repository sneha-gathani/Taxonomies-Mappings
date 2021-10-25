import json
import os
import regexFormat

# Initialize the counts for every interaction log dataset individually
def initialize():
	countISMAmar = 0
	countISMBrehmer = 0
	countISMGotzZhou = 0
	countISMYi = 0

	countGotzWenAmar = {}
	countGotzWenBrehmer = {}
	countGotzWenGotzZhou = {}
	countGotzWenYi = {}

	countGuoAmar = {}
	countGuoBrehmer = {}
	countGuoGotzZhou = {}
	countGuoYi = {}

	coverage_labels = json.load(open("../Mappings/sequence_level.json"))

	unique_sequences = coverage_labels["gotzwen2009-description"]
	for j in unique_sequences:
		countGotzWenAmar[j] = 0
		countGotzWenBrehmer[j] = 0
		countGotzWenGotzZhou[j] = 0
		countGotzWenYi[j] = 0

	unique_sequences = coverage_labels["guo2015-description"]
	for j in unique_sequences:
		countGuoAmar[j] = 0
		countGuoBrehmer[j] = 0
		countGuoGotzZhou[j] = 0
		countGuoYi[j] = 0

	return countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi


############## INFORMATION SEEKING MANTRA ##############
# Gets sequences of information seeking mantra for all provenance log datasets
def ism_sequence(data, mapping, interactionCoverage, dataset):
	sequence_coverage_labels = json.load(open("../Mappings/sequence_level.json"))
	if(interactionCoverage == 'amar2005'):
		global countISMAmar
	elif(interactionCoverage == 'brehmermunzner2013'):
		global countISMBrehmer
	elif(interactionCoverage == 'gotzzhou2009'):
		global countISMGotzZhou
	else:
		global countISMYi
	if(interactionCoverage == 'amar2005'):
		sequence_expressions = sequence_coverage_labels["amar2005-shneiderman1996-mapping"]["expression"]
		count = 0
		if(dataset == "battleheer2019"):
			count = regexFormat.get_count_battleheer2019(data, sequence_expressions)
		else:
			count = regexFormat.get_count_liuheer2014_wall2020(data, sequence_expressions)
		countISMAmar += count
	elif(interactionCoverage == 'brehmermunzner2013'):
		sequence_expressions = sequence_coverage_labels["brehmermunzner2013-shneiderman1996-mapping"]["expression"]
		count = 0
		if(dataset == "battleheer2019"):
			count = regexFormat.get_count_battleheer2019(data, sequence_expressions)
		else:
			count = regexFormat.get_count_liuheer2014_wall2020(data, sequence_expressions)
		countISMBrehmer += count
	elif(interactionCoverage == 'gotzzhou2009'):
		sequence_expressions = sequence_coverage_labels["gotzzhou2009-shneiderman1996-mapping"]["expression"]
		count = 0
		if(dataset == "battleheer2019"):
			count = regexFormat.get_count_battleheer2019(data, sequence_expressions)
		else:
			count = regexFormat.get_count_liuheer2014_wall2020(data, sequence_expressions)
		countISMGotzZhou += count
	else:
		sequence_expressions = sequence_coverage_labels["yi2007-shneiderman1996-mapping"]["expression"]
		count = 0
		if(dataset == "battleheer2019"):
			count = regexFormat.get_count_battleheer2019(data, sequence_expressions)
		else:
			count = regexFormat.get_count_liuheer2014_wall2020(data, sequence_expressions)
		countISMYi += count


############## GUO ET AL. ##############
# Gets sequence embedding of Guo et al. model for all provenance log datasets
def guo_sequence(data, mapping, interactionCoverage, dataset):
	sequence_coverage_labels = json.load(open("../Mappings/sequence_level.json"))
	if(interactionCoverage == 'amar2005'):
		global countGuoAmar
	elif(interactionCoverage == 'brehmermunzner2013'):
		global countGuoBrehmer
	elif(interactionCoverage == 'gotzzhou2009'):
		global countGuoGotzZhou
	else:
		global countGuoYi

	if(interactionCoverage == 'gotzzhou2009'):
		sequence_expressions = sequence_coverage_labels["gotzzhou2009-guo2015-mapping"]["expression"]
		name_embedding = interactionCoverage + '-guo2015-mapping'
		for expression in sequence_expressions:
			count = 0
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGuoGotzZhou[sequence_coverage_labels[name_embedding]["expression"][expression]] += count
	elif(interactionCoverage == 'yi2007'):
		sequence_expressions = sequence_coverage_labels["yi2007-guo2015-mapping"]["expression"]
		name_embedding = interactionCoverage + '-' + 'guo2015-mapping'
		for expression in sequence_expressions:
			count = 0
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGuoYi[sequence_coverage_labels[name_embedding]["expression"][expression]] += count
	else:
		return

############## GOTZ AND WEN ##############
# Gets sequences of Gotz and Wen for all provenance log datasets
def gotzwen_sequence(data, mapping, interactionCoverage, dataset):
	sequence_coverage_labels = json.load(open("../Mappings/sequence_level.json"))
	if(interactionCoverage == 'amar2005'):
		global countGotzWenAmar
	elif(interactionCoverage == 'brehmermunzner2013'):
		global countGotzWenBrehmer
	elif(interactionCoverage == 'gotzzhou2009'):
		global countGotzWenGotzZhou
	else:
		global countGotzWenYi

	if(interactionCoverage == 'amar2005'):
		sequence_expressions = sequence_coverage_labels["amar2005-gotzwen2009-mapping"]["expression"]
		name_embedding = interactionCoverage + '-gotzwen2009-mapping'
		for expression in sequence_expressions:
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGotzWenAmar[sequence_coverage_labels[name_embedding]["expression"][expression]] += count
	elif(interactionCoverage == 'brehmermunzner2013'):
		sequence_expressions = sequence_coverage_labels["brehmermunzner2013-gotzwen2009-mapping"]["expression"]
		name_embedding = interactionCoverage + '-gotzwen2009-mapping'
		for expression in sequence_expressions:
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGotzWenBrehmer[sequence_coverage_labels[name_embedding]["expression"][expression]] += count
	elif(interactionCoverage == 'gotzzhou2009'):
		sequence_expressions = sequence_coverage_labels["gotzzhou2009-gotzwen2009-mapping"]["expression"]
		name_embedding = interactionCoverage + '-gotzwen2009-mapping'
		for expression in sequence_expressions:
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGotzWenGotzZhou[sequence_coverage_labels[name_embedding]["expression"][expression]] += count
	else:
		sequence_expressions = sequence_coverage_labels["yi2007-gotzwen2009-mapping"]["expression"]
		name_embedding = interactionCoverage + '-gotzwen2009-mapping'
		for expression in sequence_expressions:
			if(dataset == "battleheer2019"):
				count = regexFormat.get_count_battleheer2019(data, expression)
			else:
				count = regexFormat.get_count_liuheer2014_wall2020(data, expression)
			countGotzWenYi[sequence_coverage_labels[name_embedding]["expression"][expression]] += count


# $$$$$$$$$$$$$$$$ WALL TO GOTZ AND ZHOU $$$$$$$$$$$$$$$$ #

def wall_to_gotzzhou2009_sequence(data, M):
	seq = []
	idata = []
	for i in range(0, len(data)):
		temp = {}
		a = data[i]['input_type']
		b = a.split("'data'")
		if(data[i]['interactionTypeRaw'] == 'filter_changed' or data[i]['interactionTypeRaw'] == 'change_attribute_distribution' or data[i]['interactionTypeRaw'] == 'change_attribute_distribution_results' or data[i]['interactionTypeRaw'] == 'axes_attribute_changed'):
			temp['id'] = 'null'
			temp['xy'] = 'null'
		else:
			idd = b[1].split("'id': ")[1]
			idd = idd.split(',')[0]
			temp['id'] = idd

			if(data[i]['interactionTypeRaw'] == 'add_to_list_via_scatterplot_click' or data[i]['interactionTypeRaw'] == 'mouseover' or data[i]['interactionTypeRaw'] == 'mouseout'):
				t = b[1].split("'x': ")[1]
				xy = t.split(", 'eventX'")[0]
				xy = "{'x': " + xy
				temp['xy'] = xy
			else:
				t = b[1].split(", 'id':")[0]
				xy = t[2:]
				temp['xy'] = xy
		temp['interaction'] = data[i]['interactionTypeRaw']
		idata.append(temp)

	innerseq = []
	i = 0
	iteratedPoints = set()

	coverage_labels = json.load(open("../Mappings/interaction_level.json"))
	if(M == "gotzzhou2009"):
		while(i < len(idata)):
			interactionMapping = coverage_labels['wall2020-gotzwen2009-mapping'][idata[i]['interaction']]["mapping"]
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
	elif(M == "yi2007"):
		while(i < len(idata)):
			interactionMapping = coverage_labels['wall2020-yi2007-mapping'][idata[i]['interaction']]["mapping"]
			if(interactionMapping == 'null'):
				i += 1
			elif(interactionMapping != 'explore' and interactionMapping != 'select'):
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
	elif(M == 'brehmermunzner2013'):
		while(i < len(idata)):
			interactionMapping = coverage_labels['wall2020-brehmermunzner2013-mapping'][idata[i]['interaction']]["mapping"]
			if(interactionMapping == 'null'):
				i += 1
			elif(interactionMapping != 'select'):
				innerseq.append(interactionMapping)
				i += 1
			else:
				# Check this for emilywall
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
	else:
		while(i < len(idata)):
			interactionMapping = coverage_labels['wall2020-amar2005-mapping'][idata[i]['interaction']]["mapping"]
			if(interactionMapping == 'null'):
				i += 1
			else:
				innerseq.append(interactionMapping)
				i += 1
	return innerseq

# Inner function of the wall_to_gotzzhou2009_sequence() function
def checkWhetherSame(a, b):
	return (a['id'] == b['id'] and a['xy'] == b['xy'])

# Removes repetes for the ISM sequence
def removeRepetitions(data):
	nonRepeats = []
	i = 1
	while(i < len(data)):
		if(data[i - 1] != data[i]):
			nonRepeats.append(data[i - 1])
		i += 1
	nonRepeats.append(data[i - 1])
	return nonRepeats

# Get Gotz and Wen sequence for Liu and Heer provenance log dataset
def get_gotzwen_sequence_liuheer2014(data, interactionCoverage):
	idata = []
	coverage_labels = json.load(open("../Mappings/interaction_level.json"))
	sequence_coverage_labels = json.load(open("../Mappings/sequence_level.json"))
	nameMapping = interactionCoverage + '-gotzwen2009-sequences'
	for i in range(0, len(data)):
		temp = {}
		if(interactionCoverage == 'gotzzhou2009'):
			temp['interactionTypeRaw'] = data[i]['interactionTypeRaw']
			temp['interaction'] = coverage_labels['liuheer2014-gotzwen2009-mapping'][data[i]['interactionTypeRaw']]["mapping"]
			a = data[i]['dimension']
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
			temp['sequence'] = sequence_coverage_labels[nameMapping][temp['interaction']]
			idata.append(temp)
		elif(interactionCoverage == "yi2007" or interactionCoverage == "brehmermunzner2013"):
			temp['interactionTypeRaw'] = data[i]['interactionTypeRaw']
			if(interactionCoverage == 'yi2007'):
				temp['interaction'] = coverage_labels['liuheer2014-yi2007-mapping'][data[i]['interactionTypeRaw']]["mapping"]
			else:
				temp['interaction'] = coverage_labels['liuheer2014-brehmermunzner2013-mapping'][data[i]['interactionTypeRaw']]["mapping"]
			a = data[i]['dimension']
			if(temp['interaction'] == "select" or temp['interaction'] == 'explore'):
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
			temp['sequence'] = sequence_coverage_labels[nameMapping][temp['interaction']]
			idata.append(temp)
		else:
			temp['interactionTypeRaw'] = data[i]['interactionTypeRaw']
			temp['interaction'] = coverage_labels['liuheer2014-amar2005-mapping'][data[i]['interactionTypeRaw']]["mapping"]
			temp['sequence'] = sequence_coverage_labels[nameMapping][temp['interaction']]
			temp['dimension'] = "null"
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

# Get the Gotz and Wen squences for the Battle and Heer provenance log dataset
def get_gotzwen_sequence_battleheer2019(data, mapping):
	i = 0
	subs = []
	t = []
	while(i < len(data)):
		if(data[i]['seqId'] == 0):
			t = []
			subs.append(t)
		else:
			t.append(data[i])
		i += 1

	innerseq = []
	if(mapping == "gotzzhou2009"):
		for i in range(0, len(subs)):
			s = subs[i]
			st = []
			for j in range(0, len(s)):
				if(s[j]['gotzzhou2009'] == 'inspect' or s[j]['gotzzhou2009'] == 'change-metaphor'):
					st.append(s[j]['state'])
				else:
					st.append('null')
			subseq = []
			for j in range(0, len(s)):
				if(s[j]['gotzzhou2009'] != 'inspect' and s[j]['gotzzhou2009'] != 'change-metaphor' and s[j]['gotzzhou2009'] != 'null'):
					subseq.append(s[j]['gotzzhou2009'])
				else:
					currst = st[j]
					if(currst in st[:j]):
						subseq.append("inspectsame")
					else:
						subseq.append("inspectdiff")
			innerseq.append(subseq)
	elif(mapping == "yi2007" or mapping == "brehmermunzner2013"):
		for i in range(0, len(subs)):
			s = subs[i]
			st = []
			for j in range(0, len(s)):
				if(s[j]['yi2007'] == 'explore' or s[j]['yi2007'] == 'select' or s[j]['brehmermunzner2013'] == 'select'):
					st.append(s[j]['state'])
				else:
					st.append('null')
			subseq = []
			for j in range(0, len(s)):
				if((s[j]['yi2007'] != 'explore' and s[j]['yi2007'] != 'select') and s[j]['brehmermunzner2013'] != 'select' and data[j]['yi2007'] != 'null'):
					if(mapping == "yi2007"):
						subseq.append(s[j]['yi2007'])
					else:
						subseq.append(s[j]['brehmermunzner2013'])
				else:
					currst = st[j]
					if(currst in st[:j]):
						subseq.append("inspectsame")
					else:
						subseq.append("inspectdiff")
			innerseq.append(subseq)
	elif(mapping == "amar2005"):
		for i in range(0, len(subs)):
			subseq = []
			for j in range(0, len(subs[i])):
				subseq.append(subs[i][j]['amar2005'])
			innerseq.append(subseq)
	return innerseq


################################ GET ALL SEQUENCES ################################ 

# Get all sequences for the Battle and Heer provenance log dataset
def get_battleheer2019_sequence(data):
	amarClassification = []
	brehmerClassification = []
	gotzZhouClassification = []
	yiClassification = []

	amar = []
	brehmer = []
	gotzZhou = []
	yi = []

	interaction_coverage_labels = json.load(open("../Mappings/interaction_level.json"))
	for i in range(0, len(data)):
		label = "null"
		if(data[i]['seqId'] == 0):
			amarClassification.append(amar)
			brehmerClassification.append(brehmer)
			gotzZhouClassification.append(gotzZhou)
			yiClassification.append(yi)
			amar = []
			brehmer = []
			gotzZhou = []
			yi = []

			amar.append(interaction_coverage_labels["battleheer2019-amar2005-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			brehmer.append(interaction_coverage_labels["battleheer2019-brehmermunzner2013-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			gotzZhou.append(interaction_coverage_labels["battleheer2019-gotzzhou2009-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			yi.append(interaction_coverage_labels["battleheer2019-yi2007-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		else:
			amar.append(interaction_coverage_labels["battleheer2019-amar2005-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			brehmer.append(interaction_coverage_labels["battleheer2019-brehmermunzner2013-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			gotzZhou.append(interaction_coverage_labels["battleheer2019-gotzzhou2009-mapping"][data[i]['interactionTypeRaw']]["mapping"])
			yi.append(interaction_coverage_labels["battleheer2019-yi2007-mapping"][data[i]['interactionTypeRaw']]["mapping"])

	amarClassification.append(amar)
	brehmerClassification.append(brehmer)
	gotzZhouClassification.append(gotzZhou)
	yiClassification.append(yi)

	amarClassification = amarClassification[1:]
	brehmerClassification = brehmerClassification[1:]
	gotzZhouClassification = gotzZhouClassification[1:]
	yiClassification = yiClassification[1:]

	amarISM = []
	brehmerISM = []
	gotzZhouISM = []
	yiISM = []

	amarGotzWen = []
	brehmerGotzWen = []
	gotzZhouGotzWen = []
	yiGotzWen = []

	amarGuo = []
	brehmerGuo = []
	gotzZhouGuo = []
	yiGuo = []

	for i in range(0, len(amarClassification)):
		tempamarISM = []
		tempbrehmerISM = []
		tempgotzZhouISM = []
		tempyiISM = []
		tempamarGuo = []
		tempbrehmerGuo = []
		tempgotzZhouGuo = []
		tempyiGuo = []
		tempamarGotzWen = []
		tempbrehmerGotzWen = []
		tempgotzZhouGotzWen = []
		tempyiGotzWen = []
		for j in range(0, len(amarClassification[i])):
			tempamarISM.append(amarClassification[i][j])
			tempbrehmerISM.append(brehmerClassification[i][j])
			tempgotzZhouISM.append(gotzZhouClassification[i][j])
			tempyiISM.append(yiClassification[i][j])

			tempamarGotzWen.append(amarClassification[i][j])
			tempbrehmerGotzWen.append(brehmerClassification[i][j])
			tempgotzZhouGotzWen.append(gotzZhouClassification[i][j])
			tempyiGotzWen.append(yiClassification[i][j])

			tempamarGuo.append(amarClassification[i][j])
			tempbrehmerGuo.append(brehmerClassification[i][j])
			tempgotzZhouGuo.append(gotzZhouClassification[i][j])
			tempyiGuo.append(yiClassification[i][j])
		
		amarISM.append(tempamarISM)
		brehmerISM.append(tempbrehmerISM)
		gotzZhouISM.append(tempgotzZhouISM)
		yiISM.append(tempyiISM)

		amarGuo.append(tempamarGuo)
		brehmerGuo.append(tempbrehmerGuo)
		gotzZhouGuo.append(tempgotzZhouGuo)
		yiGuo.append(tempyiGuo)

		amarGotzWen.append(tempamarGotzWen)
		brehmerGotzWen.append(tempbrehmerGotzWen)
		gotzZhouGotzWen.append(tempgotzZhouGotzWen)
		yiGotzWen.append(tempyiGotzWen)

	amarISM = regexFormat.get_battleheer2019_format(amarISM)
	brehmerISM = regexFormat.get_battleheer2019_format(brehmerISM)
	gotzZhouISM = regexFormat.get_battleheer2019_format(gotzZhouISM)
	yiISM = regexFormat.get_battleheer2019_format(yiISM)

	ism_sequence(amarISM, countISMAmar, "amar2005", "battleheer2019")
	ism_sequence(brehmerISM, countISMBrehmer, "brehmermunzner2013", "battleheer2019")
	ism_sequence(gotzZhouISM, countISMGotzZhou, "gotzzhou2009", "battleheer2019")
	ism_sequence(yiISM, countISMYi, "yi2007", "battleheer2019")


	amarGuo = regexFormat.get_battleheer2019_format(amarGuo)
	brehmerGuo = regexFormat.get_battleheer2019_format(brehmerGuo)
	gotzZhouGuo = regexFormat.get_battleheer2019_format(gotzZhouGuo)
	yiGuo = regexFormat.get_battleheer2019_format(yiGuo)

	guo_sequence(amarGuo, countGuoAmar, "amar2005", "battleheer2019")
	guo_sequence(brehmerGuo, countGuoBrehmer, "brehmermunzner2013", "battleheer2019")
	guo_sequence(gotzZhouGuo, countGuoGotzZhou, "gotzzhou2009", "battleheer2019")
	guo_sequence(yiGuo, countGuoYi, "yi2007", "battleheer2019")

	gotzwenData = []

	for i in range(0, len(data)):
		temp = {}
		temp['amar2005'] = interaction_coverage_labels["battleheer2019-amar2005-mapping"][data[i]['interactionTypeRaw']]["mapping"]
		temp['brehmermunzner2013'] = interaction_coverage_labels["battleheer2019-brehmermunzner2013-mapping"][data[i]['interactionTypeRaw']]["mapping"]
		temp['gotzzhou2009'] = interaction_coverage_labels["battleheer2019-gotzzhou2009-mapping"][data[i]['interactionTypeRaw']]["mapping"]
		temp['yi2007'] = interaction_coverage_labels["battleheer2019-yi2007-mapping"][data[i]['interactionTypeRaw']]["mapping"]
		temp['interactionTypeRaw'] = data[i]['interactionTypeRaw']
		temp['state'] = data[i]['state']
		temp['seqId'] = data[i]['seqId']

		gotzwenData.append(temp)

	amarGotzWen = get_gotzwen_sequence_battleheer2019(gotzwenData, "amar2005")
	brehmerGotzWen = get_gotzwen_sequence_battleheer2019(gotzwenData, "brehmermunzner2013")
	gotzZhouGotzWen = get_gotzwen_sequence_battleheer2019(gotzwenData, "gotzzhou2009")
	yiGotzWen = get_gotzwen_sequence_battleheer2019(gotzwenData, "yi2007")

	amarGotzWen = regexFormat.get_battleheer2019_format(amarGotzWen)
	brehmerGotzWen = regexFormat.get_battleheer2019_format(brehmerGotzWen)
	gotzZhouGotzWen = regexFormat.get_battleheer2019_format(gotzZhouGotzWen)
	yiGotzWen = regexFormat.get_battleheer2019_format(yiGotzWen)

	gotzwen_sequence(amarGotzWen, countGotzWenAmar, "amar2005", "battleheer2019")
	gotzwen_sequence(brehmerGotzWen, countGotzWenBrehmer, "brehmermunzner2013", "battleheer2019")
	gotzwen_sequence(gotzZhouGotzWen, countGotzWenGotzZhou, "gotzzhou2009", "battleheer2019")
	gotzwen_sequence(yiGotzWen, countGotzWenYi, "yi2007", "battleheer2019")

# Get all sequence embeddings for the Liu and Heer interaction log dataset
def get_liuheer2014_sequence(data):
	amarClassification = []
	brehmerClassification = []
	gotzZhouClassification = []
	yiClassification = []

	interaction_coverage_labels = json.load(open("../Mappings/interaction_level.json"))
	for i in range(0, len(data)):
		amarClassification.append(interaction_coverage_labels["liuheer2014-amar2005-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		brehmerClassification.append(interaction_coverage_labels["liuheer2014-brehmermunzner2013-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		gotzZhouClassification.append(interaction_coverage_labels["liuheer2014-gotzzhou2009-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		yiClassification.append(interaction_coverage_labels["liuheer2014-yi2007-mapping"][data[i]['interactionTypeRaw']]["mapping"])

	amarClassification = removeRepetitions(amarClassification)
	brehmerClassification = removeRepetitions(brehmerClassification)
	gotzZhouClassification = removeRepetitions(gotzZhouClassification)
	yiClassification = removeRepetitions(yiClassification)
	
	amar = regexFormat.get_liuheer2014_wall2020_format(amarClassification)
	brehmer = regexFormat.get_liuheer2014_wall2020_format(brehmerClassification)
	gotzZhou = regexFormat.get_liuheer2014_wall2020_format(gotzZhouClassification)
	yi = regexFormat.get_liuheer2014_wall2020_format(yiClassification)

	ism_sequence(amar, countISMAmar, "amar2005", "liuheer2014")
	ism_sequence(brehmer, countISMBrehmer, "brehmermunzner2013", "liuheer2014")
	ism_sequence(gotzZhou, countISMGotzZhou, "gotzzhou2009", "liuheer2014")
	ism_sequence(yi, countISMYi, "yi2007", "liuheer2014")

	guo_sequence(amar, countGuoAmar, "amar2005", "liuheer2014")
	guo_sequence(brehmer, countGuoBrehmer, "brehmermunzner2013", "liuheer2014")
	guo_sequence(gotzZhou, countGuoGotzZhou, "gotzzhou2009", "liuheer2014")
	guo_sequence(yi, countGuoYi, "yi2007", "liuheer2014")

	amarGotzWen = get_gotzwen_sequence_liuheer2014(data, "amar2005")
	brehmerGotzWen = get_gotzwen_sequence_liuheer2014(data, "brehmermunzner2013")
	gotzZhouGotzWen = get_gotzwen_sequence_liuheer2014(data, "gotzzhou2009")
	yiGotzWen = get_gotzwen_sequence_liuheer2014(data, "yi2007")

	amarGotzWen = regexFormat.get_liuheer2014_wall2020_format(amarGotzWen)
	brehmerGotzWen = regexFormat.get_liuheer2014_wall2020_format(brehmerGotzWen)
	gotzZhouGotzWen = regexFormat.get_liuheer2014_wall2020_format(gotzZhouGotzWen)
	yiGotzWen = regexFormat.get_liuheer2014_wall2020_format(yiGotzWen)

	gotzwen_sequence(amarGotzWen, countGotzWenAmar, "amar2005", "liuheer2014")
	gotzwen_sequence(brehmerGotzWen, countGotzWenBrehmer, "brehmermunzner2013", "liuheer2014")
	gotzwen_sequence(gotzZhouGotzWen, countGotzWenGotzZhou, "gotzzhou2009", "liuheer2014")
	gotzwen_sequence(yiGotzWen, countGotzWenYi, "yi2007", "liuheer2014")



# Get all sequences for the Wall provenance log dataset
def get_wall_sequence(data):
	amarClassification = []
	brehmerClassification = []
	gotzZhouClassification = []
	yiClassification = []

	interaction_coverage_labels = json.load(open("../Mappings/interaction_level.json"))
	for i in range(0, len(data)):
		amarClassification.append(interaction_coverage_labels["wall2020-amar2005-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		brehmerClassification.append(interaction_coverage_labels["wall2020-brehmermunzner2013-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		gotzZhouClassification.append(interaction_coverage_labels["wall2020-gotzzhou2009-mapping"][data[i]['interactionTypeRaw']]["mapping"])
		yiClassification.append(interaction_coverage_labels["wall2020-yi2007-mapping"][data[i]['interactionTypeRaw']]["mapping"])
	
	amar = regexFormat.get_liuheer2014_wall2020_format(amarClassification)
	brehmer = regexFormat.get_liuheer2014_wall2020_format(brehmerClassification)
	gotzZhou = regexFormat.get_liuheer2014_wall2020_format(gotzZhouClassification)
	yi = regexFormat.get_liuheer2014_wall2020_format(yiClassification)

	ism_sequence(amar, countISMAmar, "amar2005", "liuheer2014")
	ism_sequence(brehmer, countISMBrehmer, "brehmermunzner2013", "liuheer2014")
	ism_sequence(gotzZhou, countISMGotzZhou, "gotzzhou2009", "liuheer2014")
	ism_sequence(yi, countISMYi, "yi2007", "liuheer2014")

	guo_sequence(amar, countGuoAmar, "amar2005", "liuheer2014")
	guo_sequence(brehmer, countGuoBrehmer, "brehmermunzner2013", "liuheer2014")
	guo_sequence(gotzZhou, countGuoGotzZhou, "gotzzhou2009", "liuheer2014")
	guo_sequence(yi, countGuoYi, "yi2007", "liuheer2014")

	amarGotzWen = wall_to_gotzzhou2009_sequence(data, "amar2005")
	brehmerGotzWen = wall_to_gotzzhou2009_sequence(data, "brehmermunzner2013")
	gotzZhouGotzWen = wall_to_gotzzhou2009_sequence(data, "gotzzhou2009")
	yiGotzWen = wall_to_gotzzhou2009_sequence(data, "yi2007")

	amarGotzWen = regexFormat.get_liuheer2014_wall2020_format(amarGotzWen)
	brehmerGotzWen = regexFormat.get_liuheer2014_wall2020_format(brehmerGotzWen)
	gotzZhouGotzWen = regexFormat.get_liuheer2014_wall2020_format(gotzZhouGotzWen)
	yiGotzWen = regexFormat.get_liuheer2014_wall2020_format(yiGotzWen)

	gotzwen_sequence(amarGotzWen, countGotzWenAmar, "amar2005", "liuheer2014")
	gotzwen_sequence(brehmerGotzWen, countGotzWenBrehmer, "brehmermunzner2013", "liuheer2014")
	gotzwen_sequence(gotzZhouGotzWen, countGotzWenGotzZhou, "gotzzhou2009", "liuheer2014")
	gotzwen_sequence(yiGotzWen, countGotzWenYi, "yi2007", "liuheer2014")


################# READING THE DATA FROM PROVENANCE LOGS #################

# Read the Battle and Heer provenance log data
def read_battleheer2019_data():
	global countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi
	countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi = initialize()

	path = '../Provenance Datasets/Battle and Heer/master_file.json'
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

			get_battleheer2019_sequence(logDataset)

# Read the Liu and Heer provenance log dataset
def read_liuheer2014_data():
	global countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi
	countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi = initialize()

	path = "../Provenance Datasets/Liu and Heer/triggered-evt-logs"
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
			dictionary[i] = allLogs
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
				            temp['timestamp'] = line.split(',')[1]
				            temp['interactionTypeRaw'] = line.split(',')[4]
				            temp['dimension'] = line.split(',')[5]
				            allLogs.append(temp)
				    else:
				        for line in lines:
				            temp = {}
				            temp['timestamp'] = line.split(',')[1]
				            temp['interactionTypeRaw'] = line.split(',')[2]
				            temp['dimension'] = line.split(',')[3]
				            allLogs.append(temp)
			sortedAllLogs = sorted(allLogs, key = lambda p: (p['timestamp']))
			dictionary[i] = allLogs

	for i in participants:
		data = dictionary[i]
		send = []
		for d in data:
			send.append(d)
		get_liuheer2014_sequence(send)

# Read the Wall provenance log dataset
def read_wall2020_data():
	global countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi
	countISMAmar, countISMBrehmer, countISMGotzZhou, countISMYi, countGotzWenAmar, countGotzWenBrehmer, countGotzWenGotzZhou, countGotzWenYi, countGuoAmar, countGuoBrehmer, countGuoGotzZhou, countGuoYi = initialize()

	path = "../Provenance Datasets/Wall"
	all_files = [f for f in os.listdir(path) if not f.startswith('.')]

	all_files = sorted(all_files)

	for i in range(0, len(all_files)):
		pathdir = '../Provenance Datasets/Wall/' + all_files[i]
		li = os.listdir(pathdir)
		path = '../Provenance Datasets/Wall/' + all_files[i] +'/' + li[0]
		temp = []
		with open(path) as f:
			lis = [line.split('\t') for line in f]
			for p in range(1, len(lis)):
				dictt = {}
				dictt['interactionTypeRaw'] = lis[p][5]
				dictt['processed_at'] = lis[p][8]
				dictt['input_type'] = lis[p][4]
				temp.append(dictt)
		sortedAllLogs = sorted(temp, key = lambda ii: (ii['processed_at']))
		get_wall_sequence(sortedAllLogs)

# Main program
def main():
	'''
	Sequence coverage for Battle and Heer provenance log dataset
	'''
	print("\033[1mBattle and Heer\033[0m")
	read_battleheer2019_data()
	print("\033[1mInformation Seeking Mantra sequence using Amar et al. interaction level taxonomy:\033[0m {}".format(countISMAmar))
	print("\033[1mInformation Seeking Mantra sequence using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countISMBrehmer))
	print("\033[1mInformation Seeking Mantra sequence using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countISMGotzZhou))
	print("\033[1mInformation Seeking Mantra sequence using Yi et al. interaction level taxonomy:\033[0m {}".format(countISMYi))
	print("")

	print("\033[1mGuo et al. sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGuoAmar))
	print("\033[1mGuo et al. sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGuoBrehmer))
	print("\033[1mGuo et al. sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGuoGotzZhou))
	print("\033[1mGuo et al. sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGuoYi))
	print("")

	print("\033[1mGotz and Wen sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGotzWenAmar))
	print("\033[1mGotz and Wen sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGotzWenBrehmer))
	print("\033[1mGotz and Wen sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGotzWenGotzZhou))
	print("\033[1mGotz and Wen sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGotzWenYi))
	print("")
	print("------------------------------------")
	print("")

	'''
	Sequence coverage for Liu and Heer provenance log dataset
	'''
	print("\033[1mLiu and Heer\033[0m")
	read_liuheer2014_data()
	print("\033[1mInformation Seeking Mantra sequence using Amar et al. interaction level taxonomy:\033[0m {}".format(countISMAmar))
	print("\033[1mInformation Seeking Mantra sequence using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countISMBrehmer))
	print("\033[1mInformation Seeking Mantra sequence using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countISMGotzZhou))
	print("\033[1mInformation Seeking Mantra sequence using Yi et al. interaction level taxonomy:\033[0m {}".format(countISMYi))
	print("")

	print("\033[1mGuo et al. sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGuoAmar))
	print("\033[1mGuo et al. sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGuoBrehmer))
	print("\033[1mGuo et al. sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGuoGotzZhou))
	print("\033[1mGuo et al. sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGuoYi))
	print("")

	print("\033[1mGotz and Wen sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGotzWenAmar))
	print("\033[1mGotz and Wen sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGotzWenBrehmer))
	print("\033[1mGotz and Wen sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGotzWenGotzZhou))
	print("\033[1mGotz and Wen sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGotzWenYi))
	print("")
	print("------------------------------------")
	print("")

	'''
	Sequence coverage for Wall provenance log dataset
	'''
	print("\033[1mWall\033[0m")
	read_wall2020_data()
	print("\033[1mInformation Seeking Mantra sequence using Amar et al. interaction level taxonomy:\033[0m {}".format(countISMAmar))
	print("\033[1mInformation Seeking Mantra sequence using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countISMBrehmer))
	print("\033[1mInformation Seeking Mantra sequence using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countISMGotzZhou))
	print("\033[1mInformation Seeking Mantra sequence using Yi et al. interaction level taxonomy:\033[0m {}".format(countISMYi))
	print("")

	print("\033[1mGuo et al. sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGuoAmar))
	print("\033[1mGuo et al. sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGuoBrehmer))
	print("\033[1mGuo et al. sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGuoGotzZhou))
	print("\033[1mGuo et al. sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGuoYi))
	print("")

	print("\033[1mGotz and Wen sequences using Amar et al. interaction level taxonomy:\033[0m {}".format(countGotzWenAmar))
	print("\033[1mGotz and Wen sequences using Brehmer and Munzner interaction level taxonomy:\033[0m {}".format(countGotzWenBrehmer))
	print("\033[1mGotz and Wen sequences using Gotz and Zhou interaction level taxonomy:\033[0m {}".format(countGotzWenGotzZhou))
	print("\033[1mGotz and Wen sequences using Yi et al. interaction level taxonomy:\033[0m {}".format(countGotzWenYi))
	print("")
	print("------------------------------------")
	print("")


if __name__ == "__main__":
    main()
# %%
