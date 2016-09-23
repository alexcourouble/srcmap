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






import sqlite3, operator, random,sys
from collections import defaultdict
"""
Argument:
'pre-git' : will replace any author name before git by pre-git. This feature is only working for mingin the linux repo!!

"""

"""
TODO:

- Get data from new DB schema for speed

"""
DBPATH = "blame.db"
OUTPUTFILENAME = "outputTest.csv"
ARGS = sys.argv
"""
Commit object
a Commit object is created for each row in the DB created by the perl script
"""
class commit(object):
    def __init__(self, commitID, author, authorTime, fileName, fileName2):
        self.commitID = commitID
        self.author = author
        self.authorTime = authorTime
        self.fileName = fileName
        self.fileName2 = fileName2

"""
File object
A file object is created from all the commit objecvts refering to that file
"""
class file(object):
    def __init__(self, fileName, linesOfCode, color,
                 firstCommit,
                 lastCommit,
                 authors,
                 loc,
                 blameLink):

        self.fileName = fileName
        self.linesOfCode = linesOfCode
        self.color = color
        self.firstCommit = firstCommit
        self.lastCommit = lastCommit
        self.authors = authors
        self.loc = loc
        self.blameLink = blameLink

"""
Takes the list of commit and extract all the diferent files 
All the relevant info is extracted as well
"""
def commitToFile(commitList):
    print "creating files from commits"
    files = []
    filesAuth = {}
    filesAuthTimes = {}
    for i in commitList:
        # need to create author "pre-git" to account for pregit commits
        # assinging author
        if "pre-git" in ARGS:
            if i.authorTime == 1113690036:
                authorName = "pre-git"
            else:
                authorName = i.author
        else:
            authorName = i.author

        # putting author in list
        fName = "linux/" + i.fileName
        if fName not in files:
            # creating a new file in the dict in order to add the author
            filesAuth[fName] = [authorName]
            filesAuthTimes[fName] = [i.authorTime]
            files.append(fName)
        else:
            # file already exists, so we just add the athor to the list of authors
            filesAuth[fName].append(authorName)            
            filesAuthTimes[fName].append(i.authorTime)
    print "Compiled a list of ", len(files), " files out of ", len(commitList), " commits"
    filesAuthLOC = authLOCCount(filesAuth)
    # creating the file objects
    tree = dirTree(files)
    dirFilesAuthLOC = {}
    dirFilesAuthTime = {}
    for i in tree:
        for j in filesAuthLOC:
            path = "/" + j
            if i in path:
                if i not in dirFilesAuthLOC.keys():
                    dirFilesAuthLOC[i] = filesAuthLOC[j]
                else:
                    dirFilesAuthLOC[i] = dictSum(dirFilesAuthLOC[i],filesAuthLOC[j])
                if i not in dirFilesAuthTime.keys():
                    dirFilesAuthTime[i] = filesAuthTimes[j]
                else:
                    dirFilesAuthTime[i] = dirFilesAuthTime[i] + filesAuthTimes[j]
    # Assigning colors
    colors = getColors(dirFilesAuthLOC)
    fileObjects = []
    for i in dirFilesAuthLOC:
        # print i
        authors = []
        loc = []
        totalLOC = sum(dirFilesAuthLOC[i].values())
        for j in range(20):
            if len(dirFilesAuthLOC[i]) > 0:
                tmp = max(dirFilesAuthLOC[i].iteritems(), key=operator.itemgetter(1))[0]    
                authors.append(tmp)
                loc.append(dirFilesAuthLOC[i][tmp])
                del dirFilesAuthLOC[i][tmp]
                if "," in authors[j]:
                    authors[j] = authors[j].replace(",","")
                if '"' in authors[j]:
                    authors[j] = authors[j].replace('"','')
            else:
                authors.append("")
                loc.append(0)
        if i in colors.keys():
            col = colors[i]
        else:
            col = "-100"
        f = file(i, #fileName
                totalLOC, 
                col,
                min(dirFilesAuthTime[i]),
                max(dirFilesAuthTime[i]),
                authors,
                loc,
                "https://github.com/torvalds/linux/blame/master" + i
                )
        fileObjects.append(f)
    return fileObjects

"""
this function will assign colors to each file
"""
def getColors(dirFilesAuthLOC):
    filesColor = {}
    authorsColor = {}
    for i in dirFilesAuthLOC:
        authors = dict(sorted(dirFilesAuthLOC[i].iteritems(), key=operator.itemgetter(1), reverse=True)[:20])
        # print authors
        for j in dirFilesAuthLOC:
            if i in j and i != j:
                topGuy = max(dirFilesAuthLOC[j].iteritems(), key=operator.itemgetter(1))[0] 
                if topGuy in authors.keys():
                    if topGuy not in authorsColor.keys():
                        authorsColor[topGuy] = random.randint(0,10000)
                    filesColor[j] = authorsColor[topGuy]
    return filesColor


"""
This function will sum the two dictionaries
"""
def dictSum(*dicts):
    ret = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            ret[k] += v
    return dict(ret)


"""
this will return a list of all folder and file paths at any depth of the dir tree
"""
def dirTree(files):
    print "Creating tree"
    tree = []
    for i in files:
        splt = i.split("/")
        path = ""
        for j in splt:
            path += ("/" + j)
            if path not in tree:
                tree.append(path)
    return tree
"""
this will return a dict of each file pointing to a dict of the files authors along their numb of LOC
"""
def authLOCCount(filePerson):
    print "Reading contributors"
    fileAndContributor = {}
    for i in filePerson:
        contributors = {}
        for j in filePerson[i]:
            if j not in contributors.keys():
                contributors[j] = 1
            else:
                contributors[j] += 1
        # threeContributors = dict(sorted(contributors.iteritems(), key=operator.itemgetter(1), reverse=True)[:3])
        # fileAndContributor[i] = threeContributors
        fileAndContributor[i] = contributors
    return fileAndContributor

"""
Opening, reading the blame db.
Will return a list of the commits found in the DB
"""
def readDB(path):
	print "reading DB at:	", path
	connection =sqlite3.connect(path)
	connection.text_factory = str
	cursor = connection.cursor()
	commitList = []
	for row in cursor.execute("SELECT cid,author,authortime,filename,filename2 FROM blame"):
		# c will contain a commit object
		c = commit(row[0], row[1], row[2], row[3], row[4])
		# we add c to our commit list
		commitList.append(c)
	print "Extracted ", len(commitList), " commits from the DB"
	return commitList

def rootNode(files):
    locTot = 0
    first = []
    last = []
    for i in files:
        if len(i.fileName.split('/')) < 3:
            locTot += i.linesOfCode
            first.append(i.firstCommit)
            last.append(i.lastCommit)
    return "linux,,"+ str(locTot) + ",0,,,,,,,,,,,,,,,,,,,,,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,https://github.com/torvalds/linux,"+ str(min(first))+"," + str(max(last)) + "\n"



"""
prints to the csv file all the file info
"""
def printToFile(files):
    print "printing to file:    ", OUTPUTFILENAME
    outputFile = open(OUTPUTFILENAME, "w")
    outputFile.write("'File Name', 'Parent', 'LOC', 'Color', 'author1', 'author2', 'author3', 'author4', 'author5', 'author6', 'author7', 'author8', 'author9', 'author10', 'author11' , 'author12', 'author13', 'author14', 'author15', 'author16', 'author17', 'author18', 'author19', 'author20', 'author1LOC', 'author2LOC', 'author3LOC', 'author4LOC', 'author5LOC', 'author6LOC', 'author7LOC', 'author8LOC', 'author9LOC', 'author10LOC', 'author11LOC', 'author12LOC', 'author13LOC', 'author14LOC', 'author15LOC', 'author16LOC', 'author17LOC', 'author18LOC', 'author19LOC', 'author20LOC','blameLink','firstCommit','lastCommit'\n")
    # outputFile.write(rootNode(files))
    for i in files:
        split = i.fileName.split('/')
        if len(split) < 3:
            parent = "/linux"
        else:
            parent = ""
            for j in range(len(split)-1):
                if split[j] != "":
                    parent += ("/" + split[j])
        fName = i.fileName.replace(",","")
        if fName == parent:
            parent = ""
        outputFile.write(fName +
            "," + parent + 
            "," + str(i.linesOfCode) + 
            "," + str(i.color) + "," 
            + i.authors[0] + "," + i.authors[1] + "," + i.authors[2] + "," + i.authors[3] + "," + i.authors[4] + "," + i.authors[5] + "," + i.authors[6] + "," + i.authors[7] + "," + i.authors[8] + "," + i.authors[9] + "," + i.authors[10] + "," + i.authors[11] + "," + i.authors[12] + "," +i.authors[13] + "," + i.authors[14] + "," + i.authors[15] + "," + i.authors[16] + "," + i.authors[17] + "," + i.authors[18] + "," + i.authors[19] + "," + 
            str(i.loc[0]) + "," + str(i.loc[1]) + "," + str(i.loc[2]) + "," + str(i.loc[3]) + "," + str(i.loc[4]) + "," + str(i.loc[5]) + "," + str(i.loc[6]) + "," + str(i.loc[7]) + "," + str(i.loc[8]) + "," + str(i.loc[9]) + "," +str(i.loc[10]) + "," + str(i.loc[11]) + "," + str(i.loc[12]) + "," + str(i.loc[13]) + "," + str(i.loc[14]) + "," + str(i.loc[15]) + "," + str(i.loc[16]) + "," + str(i.loc[17]) + "," + str(i.loc[18]) + "," + str(i.loc[19]) + "," + 
            i.blameLink.replace(",","") + "," + str(i.firstCommit) + "," + str(i.lastCommit) + "\n")
    outputFile.close()

if __name__ == "__main__":
	# Query db and create list of commits
    commitList = readDB(DBPATH)
    files = commitToFile(commitList)
    printToFile(files)

