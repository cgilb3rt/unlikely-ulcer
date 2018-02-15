import csv, json, os, re

FILE = "data/games/linescores/%s/%s.csv"

HEADER = "homevisitor,stat,value".split(",")

def get_file(game_id):
	year = game_id[:4]
	return FILE % (year, game_id)

def read_header():
	return HEADER

def read_data(game_id):
	if game_id not in data:
		file = get_file(game_id)
		if os.path.exists(file):
			with open (file, 'r') as f:
				reader = csv.DictReader(f)
				for row in reader:
					if row['stat'] == 'innings':
						row['value'] = json.loads(row['value'])
					add_record(game_id, row)
	return data[game_id]

def add_records(game_id, rows):
	for row in rows:
		add_record(game_id, row)

def add_record(game_id, row):
	if game_id not in data:
		data[game_id] = []
	data[game_id].append(row)

def write_data(game_id):
	if game_id not in data:
		return
	fieldnames = read_header()
	file = get_file(game_id)
	dir = os.path.dirname(file)
	if not os.path.exists(dir):
		os.makedirs(dir)
	if os.path.exists(file):
		os.rename(file, file + '.backup')
	with open (file, 'w') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for row in data[game_id]:
			r = row
			if r['stat'] == 'innings':
				r['value'] = json.dumps(row['value'])
			writer.writerow(r)

def construct_rec(homevisitor, stat, value):
	return {'homevisitor': homevisitor, 'stat': stat, 'value': value}

def parse_innings(input):
	innings = []
	group = False
	cur = None
	for char in input.strip().replace(' ', ''):
		if char == '(':
			group = True
			cur = ''
		elif char == ')':
			innings.append(cur)
			group = False
		elif group:
			cur = cur + char
		elif char != 'X':
			innings.append(char)

	print " ** parse_innings (%s) => %s" % (input, innings)
	return innings

def find_item(lines, homevisitor, stat):
	for line in lines:
		if line['homevisitor'] == homevisitor and line['stat'] == stat:
			return line['value']
	return None

data = {}
