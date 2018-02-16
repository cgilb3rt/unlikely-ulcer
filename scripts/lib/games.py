import csv, os
from collections import OrderedDict
from datetime import datetime

FILE = "data/games.csv"

HEADER = "id,visitor-id,home-id,site-id,date,number,timeofgame,neutral,indoors,postponed-till,makeup-from,conf".split(",")

data = {}

def read_header():
	return HEADER

def read_data():
	data['id-lookup'] = {}
	with open (FILE, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			add_record(row)

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
		row['id'] = compute_id(row)
	id = row['id']
	data['id-lookup'][id] = row

def compute_id(row):
	if 'number' in row:
		number = row['number']
	else:
		number = '0'
	return '%s%s%s' % (row['date'], number, row['home-id'])

def lookup_id(id):
	if id in data['id-lookup']:
		return data['id-lookup'][id]
	return None

def has_id(id):
	return id in data['id-lookup']

def get_data():
	return data;

read_data()
