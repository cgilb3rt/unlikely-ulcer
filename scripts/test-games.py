from lib import games

game = {'visitor-id': 'macalester', 'home-id': 'saint-marys-mn', 'date': '20010701', 'site-id': 'WINON001', 'number': 1}

games.add_record(game)
games.write_data()

data = {}
games.read_data(data)
print data['id-lookup']
