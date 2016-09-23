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

