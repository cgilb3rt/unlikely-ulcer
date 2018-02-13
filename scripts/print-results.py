import argparse, sys
from lib import games, teams

def main():
	if len(sys.argv) <= 2:
		sys.exit("You must supply a team ID and year")
	a_team = sys.argv[1]
	a_year = sys.argv[2]

	# collect data
	data = []
	for game in games.get_data()['id-lookup'].values():
		if (game['visitor-id'] == a_team or game['home-id'] == a_team) and game['date'][:4] == a_year:
			data.append(game)
		
	# print
	for row in sorted(data, key=lambda game: game['id']):
		if row['visitor-id'] == a_team:
			team = teams.lookup_id(row['home-id'])
			join = 'at'
		else:
			team = teams.lookup_id(row['visitor-id'])
			join = 'vs'
		print "%s %s %s" % (row['date'], join, team['name'])
			

main()
