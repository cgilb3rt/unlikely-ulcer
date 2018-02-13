from lib import linescores

id = '200104071saint-marys-mn'

linescores.add_record(id, linescores.construct_rec('V', 'team-id', 'macalester'))
linescores.add_record(id, linescores.construct_rec('H', 'team-id', 'saint-marys-mn'))

linescores.add_record(id, linescores.construct_rec('V', 'runs', 0))
linescores.add_record(id, linescores.construct_rec('V', 'hits', 0))
linescores.add_record(id, linescores.construct_rec('V', 'errors', 2))

linescores.add_record(id, linescores.construct_rec('H', 'runs', 8))
linescores.add_record(id, linescores.construct_rec('H', 'hits', 12))
linescores.add_record(id, linescores.construct_rec('H', 'errors', 0))

linescores.write_data(id)
