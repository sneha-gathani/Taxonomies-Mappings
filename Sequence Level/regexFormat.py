import re

# Gets the count of sequences for the Battle and Heer provenance log dataset
def get_count_battleheer2019(data, expression):
	counts = []
	for i in data:
		count = len(re.findall(expression, i))
		counts.append(count)
	return sum(counts)

# Gets the count of sequences for the Liu and Heer and Wall provenance log dataset
def get_count_liuheer2014_wall2020(data, expression):
	return len(re.findall(expression, data))

# Gets the single concatenation of string of programmatic mappings for the Battle and Heer provenance log dataset
def get_battleheer2019_format(data):
	regstring_array = []
	for i in range(0, len(data)):
		regstring = ""
		for d in data[i]:
			if(d != "null"):
				regstring += d
		regstring_array.append(regstring)
	return regstring_array

# Gets the single concatenation of string of programmatic mappings for the Liu and Heer and Wall provenance log dataset
def get_liuheer2014_wall2020_format(data):
	regstring = ""
	for i in range(0, len(data)):
		if(data[i] != "null"):
			regstring += data[i]
	return regstring