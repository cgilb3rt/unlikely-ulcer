import csv, os, re
from collections import OrderedDict

FILE = "data/sites.csv"

def read_data(data):
	data['id-lookup'] = {}
	data['name-lookup'] = {}
	with open (FILE, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			add_record(row)

def read_header():
	with open (FILE, 'r') as f:
		for row in csv.reader(f):
			return row

def write_data():
	fieldnames = read_header()
	if os.path.exists(FILE):
		os.rename(FILE, FILE + '.backup')
	with open (FILE, 'w') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(data['id-lookup'].values())

def add_record(row):
	if 'id' not in row:
		row = lookup_name(row)
	id = row['id']
	data['id-lookup'][id] = row
	data['name-lookup'][row['name']] = id
	if 'extra' in row and row['extra'] is not None and row['extra'] != '':
		for extra in row['extra'].split('|'):
			data['name-lookup'][extra] = id


def compute_id(row):
	prefix = re.sub(r"\W", "", row['name'].upper())[:5]
	return '%s%s' % (prefix, lookup_id_seq(prefix))

def lookup_id_seq(prefix):
	for candidate in range(1,999):
		id = "%s%03d" % (prefix, candidate)
		if id in data['id-lookup']:
			name = data['id-lookup'][id]['name']
			if name not in data['name-lookup'].keys():
				return "%03d" % candidate
		else:
			return "%03d" % candidate
	return None

def lookup_id(id):
	if id in data['id-lookup']:
		return data['id-lookup'][id]
	return None

def lookup_name(row):
	name = row['name']
	if name in data['name-lookup']:
		id = data['name-lookup'][name]
		row['id'] = id
	else:
		row['id'] = compute_id(row)
		add_record(row)
	return data['id-lookup'][id]

data = {}
read_data(data)
