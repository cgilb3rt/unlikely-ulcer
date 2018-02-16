import csv, datetime, os, re, sys
from lib import games, linescores, sites, teams

updated_games = set()

def process_lines(date, site, lines, number):

	#print " ++ PROCESS LINES: %s | %s" %(lines[2][:27].strip(), lines[3][:27].strip())

	v_name = re.sub('\.+$', '', lines[2][:27].strip())
	h_name = re.sub('\.+$', '', lines[3][:27].strip())

	v = teams.lookup_name({'name':v_name})
	if v is None:
		sys.exit("ERROR: unable to parse Visitor team: %s" % (v_name))
	h = teams.lookup_name({'name':h_name})
	if h is None:
		sys.exit("ERROR: unable to parse Home team: %s" % (h_name))
	v_id = v['id']
	h_id = h['id']
	if v_id is None:
		sys.exit("** no visitor ID found: ", v['name'])
	if h_id is None:
		sys.exit("** no home ID found: ", h['name'])

	m1 = re.search(r"([0-9 ]+) - +([0-9]+) +([0-9]+) +([0-9]+)", lines[2][20:])
	m2 = re.search(r"([0-9 X\(\)]+) - +([0-9]+) +([0-9]+) +([0-9]+)", lines[3][20:])

	ls = []
	ls.append(linescores.construct_rec('V', 'team-id', v_id))
	ls.append(linescores.construct_rec('H', 'team-id', h_id))

	ls.append(linescores.construct_rec('V', 'R', m1.group(2)))
	ls.append(linescores.construct_rec('V', 'H', m1.group(3)))
	ls.append(linescores.construct_rec('V', 'E', m1.group(4)))

	ls.append(linescores.construct_rec('H', 'R', m2.group(2)))
	ls.append(linescores.construct_rec('H', 'H', m2.group(3)))
	ls.append(linescores.construct_rec('H', 'E', m2.group(4)))

	ls.append(linescores.construct_rec('V', 'innings', linescores.parse_innings(m1.group(1))))
	ls.append(linescores.construct_rec('H', 'innings', linescores.parse_innings(m2.group(1))))

	if date == '20020410' and h_id == 'macalester':
		print "V runs: ", m1.group(2)
		if m1.group(2) == '10':
			number = 4
		else:
			number = 3

	game = {'visitor-id': v_id, 'home-id': h_id, 'date': date, 'site-id': site['id'], 'number': number}
	game_id = games.compute_id(game)
	if games.has_id(game_id):
		print " ** SKIPPING ", game_id
		return
	if date in ['20020311','20020323','20020324','20020325','20020327','20020328']:
		print " ** SKIPPING ", game_id
		return

	games.add_record(game)
	linescores.add_records(game['id'], ls)
	updated_games.add(game['id'])
	print " ** processed game ", game['id']

def main():
	if len(sys.argv) <= 1:
		sys.exit("You must supply a path to a raw teamstats.htm file")
	a_file = sys.argv[1]

	if not os.path.exists(a_file):
		sys.exit("File does not exist: ", a_file)
	with open (a_file, 'r') as f:
		date = None
		prev_date = None
		site = None
		lines = []
		for line in f:
			lines.append(line)
			m = re.search(r"<br>\((.*) at (.*)\)<\/h3><\/a>", line)
			if m is not None:
				try :
					dt = datetime.datetime.strptime(m.group(1), '%b %d, %Y')
				except ValueError:
					dt = datetime.datetime.strptime(m.group(1), '%m/%d/%y')
				date = dt.strftime('%Y%m%d')

				if prev_date is None or prev_date <> date:
					number = 2
				else:
					number = 1
				if prev_date is not None:
					process_lines(prev_date, site, lines, number)
				prev_date = date
				lines = []
				site = {'name': m.group(2)}
				sites.add_record(site)
	process_lines(date, site, lines, number)

	sorted(updated_games)
	for game_id in updated_games:
		print "%s | %s" % (game_id, games.lookup_id(game_id)['site-id'])

	games.write_data()
	for game_id in updated_games:
		linescores.write_data(game_id)

main()
