import argparse, sys
from lib import games, linescores, teams

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

	team_obj = teams.lookup_id(a_team)
		
	# print
	overall_record = {'W': 0, 'L': 0, 'T': 0}
	conf_record = {'W': 0, 'L': 0, 'T': 0}
	for row in sorted(data, key=lambda game: game['id']):
		if row['visitor-id'] == a_team:
			join = 'at'
			opponent_id = row['home-id']
			opponent_key = 'H'
			team_key = 'V'
		else:
			join = 'vs'
			opponent_id = row['visitor-id']
			opponent_key = 'V'
			team_key = 'H'
		opp_obj = teams.lookup_id(opponent_id)

		linescore = linescores.read_data(row['id'])
		our_score = int(linescores.find_item(linescore, team_key, 'R'))
		their_score = int(linescores.find_item(linescore, opponent_key, 'R'))
		score = "%s-%s" % (our_score, their_score)
		if our_score < their_score:
			outcome = 'L'
		elif our_score > their_score:
			outcome = 'W'
		else:
			outcome = 'T'

		overall_record[outcome] = overall_record[outcome] +1
		if opp_obj['conf'] == team_obj['conf']:
			conf_record[outcome] = conf_record[outcome] +1


		innings = linescores.find_item(linescore, 'V', 'innings')
		#print " +++ DEBUG: %d | %s" % (len(innings), innings)

		overall_str = "%2d-%d-%d" % (overall_record['W'], overall_record['L'], overall_record['T'])
		conf_str = "%d-%d-%d" % (conf_record['W'], conf_record['L'], conf_record['T'])
	
		print "%s %s %22s %s %2s-%-2s %d  %-8s (%s)" % (
			row['date'], join, opp_obj['name'],
			outcome, our_score, their_score, len(innings),
			overall_str, conf_str)
			

main()
