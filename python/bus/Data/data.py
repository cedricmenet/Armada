from Travel import *
from time import *

##############################################
#####      GENERATION TRAVELS LINKS     ######
##############################################


# generate all the travels with dist and time
def generateTravels(links):
	file = open('Data/horaires.csv', 'r')
	data = file.readlines()
	travels = []
	currentLine = None
	lastLine = None
	
	currentTerminus = []
	currentDist = None
	for line in data:
		line = line[:-1]
		if "ligne" in line:
			if len(currentTerminus) >0:
				if currentLine == lastLine:
					lineType = 'r'
				else:
					lineType = 'a'
				travelsLine = generateTravelsOfLine(currentLine,currentTerminus,currentDist,lineType)
				for geneIndex in range(len(travelsLine)):
					travels.append(travelsLine[geneIndex])
				lastLine = currentLine
			currentTerminus = []
			currentDist = None
			# print "New line:" + str(currentLine)
			currentLine = line.split(' ')[1]
		elif "T" in line:
			currentTerminus.append(line)
		else:
			currentDist = line

	if currentLine == lastLine:
		lineType = 'r'
	else:
		lineType = 'a'
	travelsLine = generateTravelsOfLine(currentLine,currentTerminus,currentDist,lineType)
	for geneIndex in range(len(travelsLine)):
		travels.append(travelsLine[geneIndex])

	# Init travels to have before and after travels
	generateLinksTravels(travels,links)
	return travels

# intern function contruct travels of current line
def generateTravelsOfLine(nameline,terminus,dist,lineType):
	travels = []
	travelCount = 0;
	terminusDecoded = []
	distDecoded = dist.split(',')

	for i in range(len(terminus)):
		#save split terminus
		terminusDecoded.append(terminus[i].split(','))
		#save max travel
		if len(terminusDecoded[len(terminusDecoded)-1]) > travelCount :
			travelCount = len(terminusDecoded[len(terminusDecoded)-1])
	travelCount -= 1

	for i in range(travelCount):
		terminusIndexStart=0
		terminusIndexEnd=len(terminusDecoded)-1
		#Find terminus index of start
		while i+1 >= len(terminusDecoded[terminusIndexStart]) or terminusDecoded[terminusIndexStart][i+1] is "": 
			terminusIndexStart += 1
		#Find terminus index of end
		while i+1 >= len(terminusDecoded[terminusIndexEnd]) or terminusDecoded[terminusIndexEnd][i+1] is "": 
			terminusIndexEnd -= 1

		startPoint = TravelPoint( terminusDecoded[terminusIndexStart][0], TravelTime(terminusDecoded[terminusIndexStart][i+1].split(':')) )
		endPoint = TravelPoint( terminusDecoded[terminusIndexEnd][0], TravelTime(terminusDecoded[terminusIndexEnd][i+1].split(':'))  )
		travels.append(Travel(nameline, lineType, i+1, startPoint,endPoint,distDecoded[i+1]))
	return travels

def generateLinksTravels(travels,links):
	for travel in travels:
		for travelTMP in travels:
			if not travel == travelTMP:
				travel.isTravelCompatible(travelTMP,True,links)

#base function open file for parsing
def generateLiaisons():
	file = open('Data/terminus.csv', 'r')
	fileDist = open('Data/dist_terminus.csv', 'r')
	data = file.readlines()
	dataDist = fileDist.readlines()
	terminusName = []
	links = {}
	for i in range(len(data)):
		if not data[i] == "":
			if i==0:
				terminusName = data[i][:-1].split(',')
			else:
				line = data[i][:-1].split(',')
				lineDist = dataDist[i][:-1].split(',')
				for j in range(len(line)-1):
					links[str(terminusName[j+1]+':'+line[0])] = TravelLink(lineDist[j+1],line[j+1])
	return links

def saveIndividu (nbBus,messageLines):
	file = open('Data/Save/' + str(nbBus) + '_individu_' + str(time()) +'.csv', 'w')
	for l in messageLines:
		file.write(l)
		file.write("\n")


def exportIndividu(nbBus,individu,travels):
	total = 0
	lines = []
	for j in range(nbBus+1):
		nbTrajetbus = 0
		strtraj = ''
		for i in range(len(individu.adn)):
			if individu.adn[i] == j:
				strtraj += ',l'+str(travels[i].lineName)+':'+travels[i].lineType+':v'+str(travels[i].lineNumber)
				nbTrajetbus += 1
		total += nbTrajetbus
		lines.append('bus' + str(j)+strtraj)

	lines.insert(0,str(nbBus)+','+str(individu.scoreTime)+','+str(individu.scoreDist))
	lines.insert(0,'#Bentoumi Feth-Allah, Bosch I Sais Jordi, Casol Nicolas, Jouet Jeremie, Leger Olivier, Menet Cedric')

	file = open('Data/Save/' + str(nbBus) + '_equipe2_' + str(time()) +'.csv', 'w')
	for l in lines:
		file.write(l)
		file.write("\n")

def exportIndividu2(nbBus,individu,travels):
	lines = []
	buslistTravels = [[] for i in range(len(travels))]

	for i in range(len(individu.adn)):
		buslistTravels[individu.adn[i]].append(travels[i])

	indexBus = 0
	for busTravels in buslistTravels:
		busTravels.sort(key=lambda x: x.startPoint.time.inMin(), reverse=False)
		if len(busTravels) > 0:
			strtraj = 'bus' + str(indexBus)
			for travel in busTravels:
				strtraj += ',l'+str(travel.lineName)+':'+travel.lineType+':v'+str(travel.lineNumber)
			indexBus += 1
			lines.append(strtraj)
			

	lines.insert(0,str(nbBus)+','+str(individu.scoreTime)+','+str(individu.scoreDist))
	lines.insert(0,'#Bentoumi Feth-Allah, Bosch I Sais Jordi, Casol Nicolas, Jouet Jeremie, Leger Olivier, Menet Cedric')

	file = open('Data/Save/' + str(nbBus) + '_equipe2_' + str(time()) +'.csv', 'w')
	for l in lines:
		file.write(l)
		file.write("\n")