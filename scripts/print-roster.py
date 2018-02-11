import argparse, sys
from lib import players
from collections import OrderedDict

def main():
	a_team = None
	if len(sys.argv) > 1:
		a_team = sys.argv[1]

	data = players.get_data()

	teams = data['name-lookup'].keys()
	teams.sort()
	for team in teams:
		if a_team is None or team == a_team:
			out = []
			ids = list(OrderedDict.fromkeys(data['name-lookup'][team].values()))
			for id in ids:
				player = data['id-lookup'][id]
				years = ""
				if player['years'] is not None:
					years = ",".join(player['years'].split("|"))
				out.append("%s | %s [%s]" % (
					player['id'],
					players.compute_name(player),
					years))
			out.sort()
			print "-------------", team
			for row in out:
				print row

main()
