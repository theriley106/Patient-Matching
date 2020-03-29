import re
import json
import Levenshtein as lev

STATES = json.load(open("states.json"))


COLUMN_PRIORITY = {
    "PATIENT_ACCT_#": 1.00,
	"First": .930,
    "CURRENT_ZIP_CODE": .555,
    "CURRENT_STATE": .511,
    "CURRENT_STREET_1": .509,
    "DATE_OF_BIRTH": .503,
    "LAST_NAME": .491,
    "FIRST_NAME": .400,
    "MI": .310,
    "CURRENT_CITY": .303,
    "SEX": .100,
    "CURRENT_STREET_2": .100,
    "PREVIOUS_FIRST_NAME": .100,
    "PREVIOUS_MI": .100,
    "PREVIOUS_LAST_NAME": .100,
    "PREVIOUS_STREET_1": .100,
    "PREVIOUS_STREET_2": .100,
    "PREVIOUS_CITY": .100,
    "PREVIOUS_STATE": .100,
    "PREVIOUS_ZIP_CODE": .100,
}

def score_address_diff(string):
	if len(numericalAddress) == 0:
		return

	return string.lower()




def default_clean(string):
	x = string.decode("utf8").upper()
	if len(x) == 0:
		return
	return x

def address(string):
	return string.lower()

def address2(string):
	digits = re.findall("\d+", string)
	if len(digits) == 0:
		return
	return digits[0]


def states(state):
	if STATES.get(state) != None:
		return STATES.get(state)
	return state

def initial(mi):
	if len(mi) > 0:
		return mi[0]
	return mi

def calc_distance(val1, val2):
	val1 = val1.split(" ")
	val2 = val2.split(" ")
	score = 0
	for i in xrange(min(len(val1), len(val2))):
		score += lev.distance(val1[i], val2[i])
	return score

def dob(dob):
	return 

def calc_similarity(row1, row2):
	score = 0.0
	count = 0
	# print row1
	# print row2
	for i in xrange(len(row1)):
		# This will be the same length
		column1, value1 = row1[i]
		column2, value2 = row2[i]
		if str(value1) == "" and str(value2) == "":
			pass
		elif str(value1) == "" or str(value2) == "":
			pass
		elif column1 not in COLUMN_PRIORITY:
			pass
		else:

			count += 1
			r = min(len(value1), len(value2))
			if r == 0:
				pass
			else:
				if float(calc_distance(str(value1), str(value2))) / float(r) < .2:
					score += COLUMN_PRIORITY[column1]
			
	# print score
	if score == 0:
		return 0, count
	return score, count

distance_map = {
	"CURRENT_STREET_2": address2,
	"PREVIOUS_STREET_1": address,
	"PREVIOUS_STREET_2": address2,
	"PREVIOUS_STATE": states,
	"CURRENT_STATE": states,
	"MI": initial,
}

data_map = {
	"CURRENT_STREET_1": address,
	"CURRENT_STREET_2": address2,
	"PREVIOUS_STREET_1": address,
	"PREVIOUS_STREET_2": address2,
	"PREVIOUS_STATE": states,
	"CURRENT_STATE": states,
	"MI": initial,
}

def parse(text, column=None):
	if column == None:
		x = default_clean(text)
		if x == None:
			return ""
		return x
	clean_function = data_map.get(column, default_clean)
	returnedValue = clean_function(text)
	if returnedValue != None and len(returnedValue) == 0:
		return ""
	if returnedValue == None:
		return ""
	return returnedValue