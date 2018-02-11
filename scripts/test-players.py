from lib import players

data = players.get_data()

print "Header-----------------"
print players.read_header()

print "Name lookup keys-----------------"
print data['name-lookup'].keys()
print "Name lookup sample details-----------------"
print data['name-lookup']['macalester']


print "Name lookup-----------------"
row = {'team':'macalester', 'first':'Cristin', 'last':'Beach'}
players.lookup_name(row)
print row

print "Write-----------------"
players.write_data()


#print "Compute ID-----------------"
#row={'id':'gilbc001','first':'Chris','last':'Gilbert','years':'2001,2002','team':None,'extra':None}
#print players.compute_id(row)
#row={'first':'','last':'qw'}
#print players.compute_id(row)
#row={'first':'zx','last':''}
#print players.compute_id(row)

#print "Lookup ID prefix-----------------"
#print players.lookup_id_seq('gilbc')

#print "Write-----------------"
#row={'first':'Chris','last':'Gilbert','years':'2001,2002'}
#players.add_record(row)
#print " ---- after insert, computed id = ", row['id']
#players.write_data()

