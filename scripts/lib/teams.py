import csv
from collections import OrderedDict

FILE = "data/teams.csv"

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

def add_record(row):
	if 'id' not in row:
		lookup_name(row)
	id = row['id']
	data['id-lookup'][id] = row
	data['name-lookup'][row['name']] = id
	if 'extra' in row and row['extra'] is not None and row['extra'] != '':
		for extra in row['extra'].split('|'):
			data['name-lookup'][extra] = id

def lookup_id(id):
	if id in data['id-lookup']:
		return data['id-lookup'][id]
	return None

def lookup_name(row):
	name = row['name']
	if name in data['name-lookup']:
		row['id'] = data['name-lookup'][name]
	return None

data = {}
read_data(data)
