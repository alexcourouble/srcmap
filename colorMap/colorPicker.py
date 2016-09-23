import csv

"""
This script will read the html file containing the map with all the colors. 
It will then map the color with their ID.
"""

colorMap = {}
with open("colors.txt","r") as f:
	f = f.read()
	splt = f.split("fill=")
	count = -100
	for i in splt:
		hex = i[0:9]
		if "#000000" not in hex:
			if "<svg" not in hex:
				colorMap[count] = hex
				count += 1


with open("colorMap.csv","w") as m:
	m.write("ID,Hex\n")
	for i in colorMap:
		m.write(str(i) +","+ colorMap[i] + "\n")

