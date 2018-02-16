import csv, os, re

FILE = "data/players/%s/%s.csv"

HEADER = "player-id,game-id,lineup-pos,start,pos,ab,r,h,rbi,bb,so,2b,3b,hr,sb,cs,sh,sf,hbp,po,a,e,pb,p-ip,p-h,p-r,p-er,p-bb,p-so,p-ab,p-bf,p-wp,p-hbp,p-bk,p-w,p-l,p-s".split(",")

def get_file(team_id, player_id):
	return FILE % (team_id, player_id)

def read_header():
	return HEADER

def read_data(data, team_id, player_id):
	data = {}
	file = get_file(team_id, player_id)
	if os.path.exists(file):
		with open (file, 'r') as f:
			reader = csv.DictReader(f)
			for row in reader:
				add_record(team_id, row)


def write_data(team_id, player_id):
	if team_id not in data or player_id not in data[team_id]:
		return
	fieldnames = read_header()
	file = get_file(team_id, player_id)
	dir = os.path.dirname(file)
	if not os.path.exists(dir):
		os.makedirs(dir)
	if os.path.exists(file):
		os.rename(file, file + '.backup')
	with open (file, 'w') as f:
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(data[team_id][player_id])

def construct_rec(id, game_id, batter, pitcher):
	ret = {'player-id': id, 'game-id': game_id}
	for field in read_header():
		if batter is not None and field in batter:
			ret[field] = batter[field]
		if pitcher is not None:
			p_field = field[2:]
			#print " ** DEBUG : %s | %s" % (p_field, pitcher)
			if p_field in pitcher:
				ret[field] = pitcher[p_field]
			if 'start' in pitcher and 'start' not in ret:
				ret['start'] = pitcher['start']
	return ret

def add_record(team_id, row):
	if team_id not in data:
		data[team_id] = {}
	id = row['player-id']
	if id not in data[team_id]:
		data[team_id][id] = []
	data[team_id][id].append(row)

def lookup_id(team_id, player_id):
	if team_id in data and id in data[team_id]:
		return data[team_id][id]
	return None

data = {}
