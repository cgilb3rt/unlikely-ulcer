from lib import sites

print "Header-----------------"
print sites.read_header()

row={'name':'Winona Minn. (SMU Field)'}
sites.add_record(row)
sites.write_data()

