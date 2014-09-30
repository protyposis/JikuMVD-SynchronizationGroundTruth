import os
import xml.etree.ElementTree as ET
import csv
import json
import re

# Parses the Jiku XML metadata files and creates CSV and JSON files 
# for all videos with geolocation and compass data

def localizeDE(infile, outfile):
	fin = open(infile)
	fout = open(outfile, "w")
	for line in fin:
	    fout.write( line.replace(',', ';').replace('.',',').replace(',xml','.xml') )
	fin.close()
	fout.close()

def jsonToJs(intfile, outfile, variableName):
	f = open(intfile,'r')
	newf = open(outfile,'w')
	lines = f.readlines()
	newf.write(variableName + ' = ')
	for line in lines:
		newf.write(line)
	newf.write(';')
	newf.close()
	f.close()

indir = './metadata/'
T = []
M = {}

for root, dirs, filenames in os.walk(indir):
	filenames.sort()
	for filename in filenames:
		if filename.endswith('.xml'):
			f = root + filename
			xml = ET.parse(f)
			startTimestamp = int(xml.find('./start').text)
			xmlLocation = xml.find('.//location');
			# print(f)
			if list(xmlLocation): # check if xmlLocation is a list of subproperties; if not, it is a 'location missing' placeholder text
				lat = float(xmlLocation.find('latitude').text) # samplemeanlatitude
				lon = float(xmlLocation.find('longitude').text) # samplemeanlongitude
				acc = float(xmlLocation.find('accuracy').text)
				location = (lat, lon)
				direction = float(xml.find('.//orientation/direction').text)
				if lat != 0:
					T.append((filename,startTimestamp) + (location) + (direction,))
					M[filename] = { 'location':{ 'lat':lat, 'lon':lon, 'acc':acc }, 'dir':direction, 'start':startTimestamp }
			# else:
			# 	print(xmlLocation.text)

# write the CSV data file
with open("_locations.csv", "w",newline='') as outfile:
	writer = csv.writer(outfile, dialect = 'excel')
	writer.writerows(T)

# convert the CSV to a German localized format for easier handling in German Excel
localizeDE('_locations.csv', '_locations-de.csv')

# group the JSON data by the events
M2 = {}
for entry in M:
	event = re.search('([A-Z]+_[0-9]+)', entry).group(1)
	# print(event)
	if event not in M2:
		M2[event] = {}
	M2[event][entry.replace('.xml','')] = M[entry]

# write the JSON data to a file
with open("_locations.json", "w") as outfile:
    # json.dump({'numbers':1, 'strings':'bla', 'x':3, 'y':4}, outfile, indent=4)
    json.dump(M2, outfile, indent=4)

# convert the JSON file to an HTML-includable JS file containing the JSON data 
# due to browser security, JSON files cannot be loaded from a local path -> a 
# local webserver would be needed which is too much of a hassle for this simple task
jsonToJs("_locations.json", "_locations.js", 'locations')
