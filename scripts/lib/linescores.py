import csv, os, re

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
		if os.path.exists(fle):
			with open (file, 'r') as f:
				reader = csv.DictReader(f)
				for row in reader:
					add_record(game_id, row)
	return data[game_id]

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
		writer.writerows(data[game_id])

def construct_rec(homevisitor, stat, value):
	return {'homevisitor': homevisitor, 'stat': stat, 'value': value}

data = {}
