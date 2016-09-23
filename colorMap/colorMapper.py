"""
srcmap. Displaying linux source code information in a zoomable treemap

Copyright (C) 2016 Alexandre Courouble

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
"""



import csv

"""
This will create the actual color map readable by the tool. 
"""


# Creating a color and id dict 
# {"ID":"hex"}
colorMap = {}
with open("colorMap.csv","r") as theMap:
	theMap = csv.reader(theMap)
	for row in theMap:
		colorMap[row[0]] = row[1]

# reading the cav file
# we need all the authors and their colorID
# {"author":"colorID"}
authIDMap = {}
with open("/Users/alexandrecourouble/Desktop/public_html/treemap/dataFiles/graftedData.csv","r") as netData:
	netData = csv.reader(netData)
	for row in netData:
		if row[0] != "'File Name'":
			authIDMap[row[4]] = row[3]
print authIDMap
authColorMap = {}
# populating the map
# {"author":"hex"}
for i in authIDMap:
	authColorMap[i] = colorMap[authIDMap[i]]



with open("/Users/alexandrecourouble/Desktop/public_html/treemap/dataFiles/authColorMapGrafted.csv","w") as output:
	output = csv.writer(output)
	for i in authColorMap:
		output.writerow([i,authColorMap[i]])