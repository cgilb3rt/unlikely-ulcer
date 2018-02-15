from lib import games

game = {'visitor-id': 'macalester', 'home-id': 'saint-marys-mn', 'date': '20010701', 'site-id': 'WINON001', 'number': 1}

games.add_record(game)
#games.write_data()

print 'for game: ', game
print 'found game id: ', game['id']
print 'lookup via id: ', games.lookup_id(game['id'])
