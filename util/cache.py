# calc all
# cache all in postgres

# if new event happens
# calc teams from event

# update the list

import csv
import main
import time
import os
import queries


fields = ['teamNumber', 'elo']
fileName = "teamElos.csv"
eloRange = [1, 26000]

def createDictFromVars(teamNum, teamEloNum):
    f = lambda s: f"dict({','.join(f'{k}={k}' for k in s.split(','))})"
    teamNumber = teamNum
    elo = teamEloNum
    dictExpression = f('teamNumber,elo')
    return (eval(dictExpression))

def initCSV():
    if (os.path.exists(fileName) and os.path.isfile(fileName)):
        os.remove(fileName)
        print("file deleted")
    else:
        print("file not found")

    with open(fileName, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        csvfile.close()

def appendRowToCSV(teamNumber, teamElo):
    teamInfo = [createDictFromVars(teamNumber, round(teamElo, 1))]

    with open(fileName, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        # writing data rows
        writer.writerows(teamInfo)
        csvfile.close()

def printCSV(name):
    with open(name, mode='r') as file:
        csvFile = csv.reader(file)
        print("==========================")
        print(name)
        print("CSV Content: ")
        for lines in csvFile:
            print(lines)
        print("==========================")
def calcAll():
    eloList = list()
    teamList = list()
    print(eloRange)
    for i in range(eloRange[0], eloRange[1]):
        eloRating = main.getElo(i)
        if eloRating is not False:
            eloList.append(eloRating)
            teamList.append(i)
    return teamList, eloList

def cacheAll():
    teamList, eloList = calcAll()
    for i in range(len(eloList)):
        print(teamList[i], eloList[i])
        appendRowToCSV(teamList[i], eloList[i])

def initNumMatchesCSV():
    fields = ["numMatches"]
    numMatches = main.fetchAPI(queries.numMatchesPlayed)['data']['matchesPlayedCount']
    fileName = "numMatches.csv"

    if (os.path.exists(fileName) and os.path.isfile(fileName)):
        os.remove(fileName)
        print("file deleted")
    else:
        print("file not found")

    with open(fileName, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()
        writer.writerows([dict([('numMatches', numMatches)])])

        csvfile.close()

def checkNumMatchesCSV():
    fileName = "numMatches.csv"
    newNumMatches = main.fetchAPI(queries.numMatchesPlayed)['data']['matchesPlayedCount']

    with open(fileName, mode='r') as csvFile:
        csvReader = csv.reader(csvFile)
        oldNumMatches = int(list(csvReader)[1][0])
        csvFile.close()

    if newNumMatches > oldNumMatches:
        return True
    else:
        return False

def createCSVFromList(fileName, list):
    fields = list[0]
    del list[0]

    with open(fileName, 'w') as csvfile:
        # creating a csv dict writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(list)


initNumMatchesCSV()
print(checkNumMatchesCSV())
printCSV("sortedTeamElos.csv")

# return if()

# add event listener and keep updating list based on that
# def checkForEvent

# def checkIfEventDone

# def


# def import if else elif for and or in as not from with del try except return pass while  continue pass



