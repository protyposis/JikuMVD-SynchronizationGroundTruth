import os
import xml.etree.ElementTree as ET

# gathers all location accuracy values and prints them out

indir = './metadata/'
accuracyList = []

for root, dirs, filenames in os.walk(indir):
	for filename in filenames:
		if filename.endswith('.xml'):
			f = root + filename
			xmlLocationAcc = ET.parse(f).find('.//location/accuracy');
			if xmlLocationAcc is not None:
				accuracyList.append(float(xmlLocationAcc.text))

accuracyList.sort()
print(accuracyList)
print('min: ' + str(min(accuracyList)))
print('max: ' + str(max(accuracyList)))