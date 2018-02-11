import csv, os
from collections import OrderedDict

data_dir = 'data/'
data_sources = {
	"teams" : "teams.csv",
	"players" : "players.csv"
}

def read_data():
	"""read CSV files"""
	ret = {}
	for name in data_sources:
		file = data_dir + data_sources[name]
		if os.path.isfile(file):
			with open(file) as f:
				ret[name] = OrderedDict((row[0],row) for row in csv.reader(f))
	construct_team_lookup(ret)
	construct_players_lookup(ret)
	return ret

def construct_team_lookup(data):
	ret = {}
	for key in data['teams']:
		t = data['teams'][key]
		ret[t[2]] = t[0]
		if len(t) > 4:
			for item in t[4].split("|"):
				ret[item] = t[0]
	data['teams-lookup'] = ret

def construct_players_lookup(data):
	ret = {}
	for key in data['players']:
		t = data['players'][key]
		name = "%s %s" % (t[1], t[2])
		ret[name] = t[0]
		if len(t) > 4:
			for item in t[4].split("|"):
				ret[item] = t[0]
	data['players-lookup'] = ret
