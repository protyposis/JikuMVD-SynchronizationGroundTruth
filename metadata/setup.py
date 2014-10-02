import os
import sys
import subprocess

# This script downloads and prepares the Jiku metadata for the graphical map. It
# only need to be run for the first time, all further data preparation is done
# in the extractgeo.py script.

def is_tool(name):
	try:
		devnull = open(os.devnull)
		subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			return False
	return True

extension = None

errorDlScriptMissing = """
Jiku download file missing, please:
 - visit http://liubei.ddns.comp.nus.edu.sg/jiku/dataset/download/
 - select the desired videos (preferably all)
 - download the download script archive
 - extract the archive to this script's directory
 - restart this script
"""

errorWgetMissing = """
wget is missing, but required for downloading
please download wget
 - for windows (wget AND dependencies): http://gnuwin32.sourceforge.net/packages/wget.htm
 - for linux: through your distribution's package manager
"""

print("checking for supported OS...")
if os.name is 'nt':
	extension = '.bat'
elif os.name is 'posix':
	extension = '.sh'
else:
	print("unsupported OS: " + os.name)
	sys.exit(1)

print("checking for download script...")
if not os.path.isfile('download'+extension):
	print(errorDlScriptMissing)
	sys.exit(2)

print("checking for wget...")
if not is_tool("wget"):
	print(errorWgetMissing)
	sys.exit(3)

print("extracting metadata XML files from download script...")
with open("download"+extension, "r") as dlin, \
		open("download-xml"+extension, "w") as dlxmlout:
	for line in dlin:
		if line.strip().endswith(".xml"):
			line = line.replace('-N', '-N -P ./metadata/')
			dlxmlout.write(line)

print("downloading XML metadata files to 'metadata' subdirectory...")
subprocess.call("download-xml"+extension)

print("downloading finished!")
print("preparing geo data...")
execfile("extractgeo.py")
print("finished! You can now open the map.html in the 'map' subdirectory.")