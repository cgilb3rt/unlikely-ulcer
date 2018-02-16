import argparse, csv, datetime, os, re, sys
from collections import OrderedDict
from lib import games, linescores, players, player_games, sites, teams

updated_players = {}
updated_games = set()

def read_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('year')
	parser.add_argument('files', nargs='+')
	parser.add_argument('--silent', action='store_true')
	return parser.parse_args()

def read_at(line):
	m = re.search('(.+) +[a-z]{2} +(.+)', line)
	if not m is None:
		return (m.group(1).strip(), m.group(2).strip())
	sys.exit("Unable to parse line: %s" % line)

def read_score(line):
	return line.strip().split(' ')[1]

def read_batter(line, lineup_pos):
	m = re.search('([\w\'\.\* ]+) ([a-z1-9/]+)\.+ ([0-9 ]+)', line)
	if m is None:
		# handle the case where there is no '.' after positions
		m = re.search('([\w\'\.\* ]+) ([a-z1-9/]+) ([0-9 ]+)', line)
		if m is None:
			sys.exit(" -- UNABLE TO PARSE : %s" % line)
	ret = {"start": (line[0] != ' '), "pos": m.group(2)}

	if ret['start']:
		lineup_pos = lineup_pos +1
	ret['lineup-pos'] = lineup_pos

	(ret['first'], ret['last']) = parse_name(m.group(1).strip())

	#print "BATTER: %s %s | %s" % (ret['first'], ret['last'], line)
	
	stats = m.group(3).split()
	i = 0
	for key in ['ab','r','h','rbi','bb','so','po','a']:
		ret[key] = stats[i]
		i = i+1
		
	return ret

def read_pitcher(line, order):
	#m = re.search('([\w\'\.\* ]+)\.+ ([0-9\. ]+)', line[)
	#if m is None:
	#	sys.exit(" -- UNABLE TO PARSE : %s" % line)
	ret = {"start": (order == 0)}

	(ret['first'], ret['last']) = parse_name(line[:20])
	# strip off trailing dots
	ret['last'] = re.sub(r"\.+$", "", ret['last'])

	#print "PITCHER: %s %s | %s" % (ret['first'], ret['last'], line)

	stats = line[20:].split()
	i = 0
	#print " ++ read_pitcher: %s | %s" % (stats, line)
	for key in ['ip','h','r','er','bb','so','ab','bf']:
		if len(stats) > i:
			ret[key] = stats[i]
			i = i+1
		
	return ret

def read_extras(line):
	ret = {}
	m3 = re.search(r"Win - (.*)\. +Loss - (.*)\. +Save - (.*)\.", line)
	if m3 is not None:
		ret['W'] = m3.group(1)
		ret['L'] = m3.group(2)
		ret['S'] = m3.group(3)
	else:
		for m in re.finditer(r"(\S+) - ([^-].*)\.", line):
			if m is not None:
				key = m.group(1)
				value = m.group(2)
				if key != 'HBP':
					ret[key] = value
				# special handling for HBP since it has two names
				else:
					m2 = re.search(r"by (.+) \((.+)\)", value)
					if m2 is None:
						print "WARNING: Unable to parse HBP line: ", value
					else:
						ret['P-HBP'] = m2.group(1)
						ret['HBP'] = m2.group(2)
	return ret

def parse_name(name):
	if ' ' in name:
		parts = name.split(' ')
		return (parts[0], parts[1])
	else:
		# try to identify first initial 'R.Zahn'
		m = re.search(r"([A-Z])\.(.*)", name)
		if m is not None:
			return (m.group(1), m.group(2))
		else:
			return (None, name)
	
def read_boxscore(lines):
	m1 = re.compile(r"<h3>Box Score<\/h3>")
	m2 = re.compile(r"The Automated ScoreBook")
	m3 = re.compile(r"^[^\D]+ \D+ ")
	m4 = re.compile(r"^Name \(Pos\)") # boxscore top
	m5 = re.compile(r"^Totals") # boxscore bottom
	m6 = re.compile(r"^-+") # linescore separator
	m7 = re.compile(r"\S+ - .*\.") # extras
	m8 = re.compile(r"^.+  +IP") # pitching header
	m9 = re.compile(r"<hr></pre>") # end

	status = None
	ret = {'visitor-batting': [], 'visitor-pitching': [],
		 'home-batting': [], 'home-pitching': [],
		 'extras': {}, 'notes': []}

	v_lineup_pos = 0
	h_lineup_pos = 0
	v_pitcher_order = 0
	h_pitcher_order = 0
	for line in lines:
		if m1.search(line) is not None:
			status = "start"
		elif status == "start" and m2.search(line) is not None:
			status = "teams"
		elif status == "teams":
			(v, h) = read_at(line)
			ret['visitor'] = teams.lookup_name({'name': v})
			if ret['visitor'] is None or 'id' not in ret['visitor'] or ret['visitor']['id'] is None:
				sys.exit("No team ID found for visitor team: %s" % v)
			ret['home'] = teams.lookup_name({'name': h})
			if ret['home'] is None or 'id' not in ret['home'] or ret['home']['id'] is None:
				sys.exit("No team ID found for home team: %s" % h)
			status = "date"
		elif status == "date":
			(date, site) = read_at(line)
			try:
				dt = datetime.datetime.strptime(date, '%b %d, %Y')
			except ValueError:
				dt = datetime.datetime.strptime(date, '%m/%d/%y')
			ret['date'] = dt.strftime('%Y%m%d')
			ret['site'] = {'name': site}
			sites.add_record(ret['site'])
			status = "visitor"

		elif status == "visitor" and m3.search(line) is not None:
			ret['visitor-score'] = read_score(line)
		elif status == "visitor" and m4.search(line) is not None:
			status = "visitor-batting"
		elif status == "visitor-batting" and m5.search(line) is not None:
			ret['visitor-totals'] = line
			status = "home"
		elif status == "visitor-batting" and m5.search(line) is None:
			v_player = read_batter(line, v_lineup_pos)
			v_lineup_pos = v_player['lineup-pos']
			ret['visitor-batting'].append(v_player)

		elif status == "home" and m3.search(line) is not None:
			ret['home-score'] = read_score(line)
		elif status == "home" and m4.search(line) is not None:
			status = "home-batting"
		elif status == "home-batting" and m5.search(line) is not None:
			ret['home-totals'] = line
			status = "linescore"
		elif status == "home-batting" and m5.search(line) is None:
			h_player = read_batter(line, h_lineup_pos)
			h_lineup_pos = h_player['lineup-pos']
			ret['home-batting'].append(h_player)

		elif status == "linescore" and m6.search(line) is not None:
			#print " ++ (switch to visitor-linescore): ", line
			status = "visitor-linescore"
		elif status == "visitor-linescore":
			#print " ++ (switch to home-linescore): ", line
			ret['visitor-linescore'] = line
			status = "home-linescore"
		elif status == "home-linescore":
			#print " ++ (switch to notes): ", line
			ret['home-linescore'] = line
			status = "notes"
			
		elif m9.search(line) is not None:
			break
		elif status == "notes" and m8.search(line) is not None:
			#print " ++ (switch to visitor-pitching): ", line
			status = "visitor-pitching"
		elif status == "visitor-pitching" and m8.search(line) is not None:
			#print " ++ (switch to home-pitching): ", line
			status = "home-pitching"
		elif status == "home-pitching" and not line:
			#print " ++ (switch to notes): ", line
			status = "notes"
		elif status == "visitor-pitching":
			if line.strip() != '':
				ret['visitor-pitching'].append(read_pitcher(line, v_pitcher_order))
				v_pitcher_order = v_pitcher_order +1
		elif status == "home-pitching":
			if line.strip() != '':
				ret['home-pitching'].append(read_pitcher(line, h_pitcher_order))
				h_pitcher_order = h_pitcher_order +1
		elif status == "notes" and line and m6.search(line) is None:
			if m7.search(line) is None:
				ret['notes'].append(line)
			else:
				ret['extras'].update(read_extras(line))

	return ret

def construct_game(boxscore, year):
	ret = {}
	ret['info'] = construct_game_info(boxscore, year)

	# look up player IDs
	visitor_id = ret['info']['visitor-id']
	home_id = ret['info']['home-id']
	game_id = ret['info']['id']

	ret['visitor-roster'] = construct_roster(year, visitor_id, game_id, boxscore['visitor-batting'], boxscore['visitor-pitching'], boxscore['extras'])
	ret['home-roster'] = construct_roster(year, home_id, game_id, boxscore['home-batting'], boxscore['home-pitching'], boxscore['extras'])

	ret['linescore'] = construct_linescore(game_id, boxscore)

	return ret

def construct_game_info(boxscore, year):
	""" populate a game record (see data/games.csv) """
	ret = {}

	ret['visitor-id'] = boxscore['visitor']['id']
	ret['home-id'] = boxscore['home']['id']

	ret['date'] = boxscore['date']
	ret['site-id'] = boxscore['site']['id']

	for note in boxscore['notes']:
		## check for doubleheader
		m1 = re.search('Game ([0-9]) of doubleheader.', note)
		m2 = re.search('Start: ([0-9: apm]+?) Time: ([0-9:]+?) Attendance: ([0-9]+)', note)
		if not m1 is None:
			ret['number'] = m1.group(1)
		elif not m2 is None:
			ret['timeofgame'] = m2.group(2)

	ret['conf'] = is_conf_game(boxscore)

	games.add_record(ret)
	return ret

def is_conf_game(boxscore):
	if 'conf' in boxscore['visitor'] and 'conf' in boxscore['home']:
		v_conf = boxscore['visitor']['conf']
		h_conf = boxscore['home']['conf']
		if v_conf is not None and h_conf is not None and v_conf == h_conf:
			return 1
	return 0

def construct_roster(year, team, game_id, batting, pitching, extras):
	ret = []
	batters = {}
	pitchers = {}
	for batter in batting:
		rec = players.create_rec(batter['first'], batter['last'], year, team)
		#print " ++ batter : ", rec
		players.add_record(rec)
		id = rec['id']
		ret.append(id)
		batters[id] = batter
	for pitcher in pitching:
		rec = players.create_rec(pitcher['first'], pitcher['last'], year, team)
		#print " ++ pitcher : ", rec
		players.add_record(rec)
		id = rec['id']
		if id not in ret:
			ret.append(id)
		pitchers[id] = pitcher
		
	for key in extras.keys():
		for entry in extras[key].split(","):
			number = 1
			name = entry.strip()
			m = re.match(r"(.*) ([0-9\-]+)", name)
			if m is not None:
				name = m.group(1)
				number = m.group(2)

			# look up name
			player_id = None
			if name is not 'None':
				for id in batters.keys():
					if batters[id]['last'] == name:
						player_id = id
						break
					elif players.compute_name(batters[id]) == name:
						player_id = id
						break

			if player_id is not None:
				#print " ++ (%s) EXTRA: %s = %s [%s] x%s" % (team, key, name, player_id, number)
				if key in ['E','2B','3B','HR','SB','CS','SH','HBP']:
					batters[player_id][key.lower()] = number
				elif key in ['WP','P-HBP','W','L','S']:
					if key == 'P-HBP': 
						key = "hbp"
					else:
						key = key[:1].lower()
					pitchers[player_id][key] = number

	for id in ret:
		batter = None
		pitcher = None
		if id in batters:
			batter = batters[id]
		if id in pitchers:
			pitcher = pitchers[id]
		player_games.add_record(team, player_games.construct_rec(id, game_id, batter, pitcher))
		if team not in updated_players:
			updated_players[team] = set()
		updated_players[team].add(id)
	return ret

def construct_linescore(game_id, boxscore):
	ls = []
	ls.append(linescores.construct_rec('V', 'team-id', boxscore['visitor']['id']))
	ls.append(linescores.construct_rec('H', 'team-id', boxscore['home']['id']))

	m1 = re.search(r"([0-9 \-\(\)]+) +- +([0-9]+) +([0-9]+) +([0-9]+)", boxscore['visitor-linescore'])
	m2 = re.search(r"([0-9 \-\(\)]+) +- +([0-9]+) +([0-9]+) +([0-9]+)", boxscore['home-linescore'])

	if m1 is not None:
		ls.append(linescores.construct_rec('V', 'R', m1.group(2)))
		ls.append(linescores.construct_rec('V', 'H', m1.group(3)))
		ls.append(linescores.construct_rec('V', 'E', m1.group(4)))

		ls.append(linescores.construct_rec('V', 'innings', linescores.parse_innings(m1.group(1))))
	else:
		print " WARNING : could not parse visitor linescore from ", boxscore['visitor-linescore']
	if m2 is not None:
		ls.append(linescores.construct_rec('H', 'R', m2.group(2)))
		ls.append(linescores.construct_rec('H', 'H', m2.group(3)))
		ls.append(linescores.construct_rec('H', 'E', m2.group(4)))

		ls.append(linescores.construct_rec('H', 'innings', linescores.parse_innings(m2.group(1))))
	else:
		print " WARNING : could not parse home linescore from ", boxscore['home-linescore']

	linescores.add_records(game_id, ls)
	updated_games.add(game_id)

	return ls

def add_player(first, last, team, year):
	rec = {'last': last, 'first': first, 'team': team, 'years': year, 'extra': None}
	rec['id'] = players.compute_id(rec)
	if rec['id'] is None:
		sys.exit("No id computed for new player: %s" % rec)
	players.write_rows([rec])
	return rec
	
def main():
	args = read_args()

	for file in args.files:
		with open(file) as f:
			print "Processing file: ", file
			boxscore = read_boxscore([line.strip('\n') for line in f])
			game = construct_game(boxscore, args.year)
			print "...processed as id: ", game['info']['id']

	if args.silent:
		print " ** SILENT MODE **"
		for key in game:
			print "%s | %s" % (key, game[key])
		return

	games.write_data()
	sites.write_data()
	players.write_data()
	for team_id in updated_players:
		for id in updated_players[team_id]:
			player_games.write_data(team_id, id)

	for game_id in updated_games:
		linescores.write_data(game_id)

main()
