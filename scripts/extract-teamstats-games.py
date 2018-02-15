import csv, datetime, os, re, sys
from lib import games, linescores, sites, teams

updated_games = set()

def process_lines(date, site, lines, number):

	v = {'name': re.sub('\.+$', '', lines[2][:27].strip())}
	h = {'name': re.sub('\.+$', '', lines[3][:27].strip())}

	v = teams.lookup_name(v)
	h = teams.lookup_name(h)
	v_id = v['id']
	h_id = h['id']
	if v_id is None:
		sys.exit("** no visitor ID found: ", v['name'])
	if h_id is None:
		sys.exit("** no home ID found: ", h['name'])

	m1 = re.search(r"([0-9 ]+) - +([0-9]+) +([0-9]+) +([0-9]+)", lines[2][20:])
	m2 = re.search(r"([0-9 X\(\)]+) - +([0-9]+) +([0-9]+) +([0-9]+)", lines[3][20:])

	game = {'visitor-id': v_id, 'home-id': h_id, 'date': date, 'site-id': site['id'], 'number': number}
	games.add_record(game)

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
				if prev_date is None or prev_date <> date:
					number = 2
				else:
					number = 1
				if date is not None and site['id'] == 'ORANG001':
						process_lines(date, site, lines, number)
						prev_date = date
				lines = []
				date = datetime.datetime.strptime(m.group(1), '%b %d, %Y').strftime('%Y%m%d')
				site = {'name': m.group(2)}
				sites.add_record(site)
	if date is not None and site['id'] == 'ORANG001':
		process_lines(date, site, lines, number)

	games.write_data()
	for game_id in updated_games:
		linescores.write_data(game_id)

main()
