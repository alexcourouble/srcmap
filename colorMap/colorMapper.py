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