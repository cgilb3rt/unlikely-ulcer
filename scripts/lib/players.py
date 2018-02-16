import csv, os, re
from collections import OrderedDict

FILE = "data/players.csv"

HEADER = "id,last,first,team,years,extra".split(",")

def read_data(data):
	data['id-lookup'] = {}
	data['name-lookup'] = {}
	if os.path.exists(FILE):
		with open (FILE, 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				add_record(row)

def read_header():
	return HEADER

def write_data():
	fieldnames = read_header()
	if os.path.exists(FILE):
		os.rename(FILE, FILE +'.backup')
	with open (FILE, 'w') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(data['id-lookup'].values())

def create_rec(first, last, year, team):
	return {'first': first, 'last': last, 'years': year, 'team': team}

def add_record(row):
	if 'id' not in row:
		row = lookup_name(row)
	id = row['id']
	name = compute_name(row)
	team = row['team']
	data['id-lookup'][id] = row
	if team not in data['name-lookup']:
		data['name-lookup'][team] = {}
	data['name-lookup'][team][name] = id
	if 'extra' in row and row['extra'] is not None and row['extra'] != '':
		for extra in split_packed(row['extra']):
			data['name-lookup'][team][extra] = id

def compute_id(row):
	if 'last' not in row or row['last'] is None:
		last = ''
	else:
		last = re.sub(r"\W", "", row['last'])
	last = last.ljust(4, '-').lower()
	if 'first' not in row or row['first'] is None:
		first = ''
	else:
		first = re.sub(r"\W", "", row['first'])
	first = first.ljust(1, '-').lower()
	prefix = "%s%s" % (last[:4], first[:1])
	return "%s%s" % (prefix, lookup_id_seq(prefix))

def lookup_id_seq(prefix):
	for candidate in range(1,999):
		id = "%s%03d" % (prefix, candidate)
		if id in data['id-lookup']:
			name = compute_name(data['id-lookup'][id])
			if name not in data['name-lookup'].keys():
				return "%03d" % candidate
		else:
			return "%03d" % candidate
	return None

def compute_name(row):
	first = row['first']
	last = row['last']
	if first is None:
		return last
	ret = "%s %s" % (first, last)
	return ret.strip()

def lookup_id(id):
	if id in data['id-lookup']:
		return data['id-lookup']
	return None

def lookup_name(row):
	team = row['team']
	name = compute_name(row)
	if team not in data['name-lookup']:
		data['name-lookup'][team] = {}
	if name in data['name-lookup'][team]:
		id = data['name-lookup'][team][name]
		row['id'] = id
		# this usage may ask us to extend the years list
		rec = data['id-lookup'][id]
		if 'years' in row and row['years'] is not None and row['years'] != rec['years']:
			years = split_packed(rec['years'])
			for yr in split_packed(row['years']):
				if yr not in years:
					years.append(yr)
			years.sort()
			data['id-lookup'][id]['years'] = join_packed(years)
	else:
		id = compute_id(row)
		row['id'] = id
		data['id-lookup'][id] = row
		data['name-lookup'][team][name] = id
	return data['id-lookup'][id]

def split_packed(field):
	return field.split("|")

def join_packed(list):
	return "|".join(list)

def get_data():
	return data;

data = {}
read_data(data)
