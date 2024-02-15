# imports
import requests
import json
from string import Template
from util import elo
from datetime import datetime


print(elo.ratingDiff)

url = "https://api.ftcscout.org/graphql"

teamEventListTemplate = Template("""
{
    teamByNumber(number: $teamNumber){
      matches (season: 2023){
        eventCode
      }
  }
} """)

eventMatchesTemplate = Template(""" {
  eventByCode(season:2023, code:"$code"){
    matches { 
      teams {teamNumber}
      scores {
        ... on MatchScores2023	{ 
          red {totalPointsNp}
          blue {totalPointsNp}
        }
      }
    }
  }
}""")

eventDateTemplate = Template(""" 
{
  eventByCode(season:2023, code:"$code"){
    end
  }
}
"""
                             )

teamNumber = 22012

eventList = teamEventListTemplate.safe_substitute(teamNum=22012)


def fetchAPI(body):
    response = requests.post(url=url, json={"query": body})
    if response.status_code == 200:
        jsonResponse = json.loads(response.content)
    else:
        jsonResponse = "null"
    return jsonResponse


def getEvents(teamNum):
    body = teamEventListTemplate.safe_substitute(teamNumber=teamNum)
    jsonResponse = fetchAPI(body)
    numMatches = len(jsonResponse["data"]["teamByNumber"]["matches"])
    eventSet = set()
    for i in range(numMatches):
        eventSet.add(jsonResponse["data"]["teamByNumber"]["matches"][i]['eventCode'])
    return (eventSet)


def getAllTeamsFromEvent(eventCode):
    body = eventMatchesTemplate.safe_substitute(code=eventCode)
    jsonResponse = fetchAPI(body)
    numMatches = len(jsonResponse["data"]["eventByCode"]["matches"])
    teamSet = set()
    for i in range(numMatches):
        for j in range(4):
            teamSet.add(jsonResponse["data"]["eventByCode"]["matches"][i]["teams"][j]["teamNumber"])
    return jsonResponse, teamSet


def getAllTeamsFromEvents(eventList):
    teamSet = set()
    jsonResponseList = list()
    for event in eventList:
        body = eventMatchesTemplate.safe_substitute(code=event)
        jsonResponse = fetchAPI(body)
        numMatches = len(jsonResponse["data"]["eventByCode"]["matches"])
        jsonResponseList.append(jsonResponse)
        for i in range(numMatches):
            for j in range(4):
                teamSet.add(jsonResponse["data"]["eventByCode"]["matches"][i]["teams"][j]["teamNumber"])
    return jsonResponseList, teamSet


def getEventDate(eventCode):
    eventDateRequest = eventDateTemplate.safe_substitute(code=eventCode)

    dateStr = fetchAPI(eventDateRequest)["data"]["eventByCode"]["end"]
    dateFormat = "%Y-%m-%d"
    dateObj = datetime.strptime(dateStr, dateFormat)
    return dateStr


def sortEvents(eventList):
    dateObjList = list()
    for event in eventList:
        # print(event)
        dateObjList.append(getEventDate(event))

    eventDict = dict(zip(eventList, dateObjList))
    #   print(eventDict)
    #   for item in eventDict.items():
    # print(item[1], item[0])
    #   print("====")/
    #   rankedTeamDict = dict(sorted(teamDict.items(), key=lambda item: item[1], reverse=True))
    sortedEventDict = dict(sorted(eventDict.items(), key=lambda x: x[1]), reverse=True)
    #   for item in sortedEventDict.items():
    # print(item[1], item[0])
    #   print(list(sortedEventDict.keys()))
    return list(sortedEventDict.keys())


def initialRatings(teamSet):
    playerList = list()
    for team in teamSet:
        playerList.append(elo.player(team))
    return playerList


def findMatches(matchList):
    numMatches = len(matchList["data"]["eventByCode"]["matches"])
    matchArray = list()
    for i in range(numMatches):
        currentMatch = list()
        for j in range(4):
            currentMatch.append(matchList["data"]["eventByCode"]["matches"][i]["teams"][j]["teamNumber"])
        matchArray.append(currentMatch)
    return matchArray


def getPlayerIndex(teamList, teamNum):
    for team in teamList:
        if (team.teamNumber == teamNum):
            return teamList.index(team)


def simulateMatches(teamsInMatches, teamList, matchStats):
    # print(teamsInMatches)
    for match in teamsInMatches:
        try:
            elo.matchup(
                teamList[getPlayerIndex(teamList, match[0])],
                teamList[getPlayerIndex(teamList, match[1])],
                teamList[getPlayerIndex(teamList, match[2])],
                teamList[getPlayerIndex(teamList, match[3])],
                matchStats["data"]["eventByCode"]["matches"][teamsInMatches.index(match)]["scores"]["red"][
                    "totalPointsNp"],
                matchStats["data"]["eventByCode"]["matches"][teamsInMatches.index(match)]["scores"]["blue"][
                    "totalPointsNp"]
            )
        except TypeError:
            pass


def getAllElos(teamList):
    for team in teamList:
        print(str(team.teamNumber) + ": " + str(team.eloRating))


def calcEloFromAllEvents(teamNum):
    eventList = getEvents(teamNum)
    print("Events Competed At:", eventList)
    sortedEventList = sortEvents(eventList)
    #
    matchStatsList, teamSet = getAllTeamsFromEvents(eventList)

    teamList = initialRatings(teamSet)

    for matchStats in matchStatsList:
        teamsInMatches = findMatches(matchStats)
        simulateMatches(teamsInMatches, teamList, matchStats)
        # print(matchStatsList.index(matchStats), teamRanking(teamNum, teamList, True))
    return teamList


def teamRanking(teamName, teamList, shouldPrint):
    teamNumList = list()
    teamEloList = list()
    for team in teamList:
        teamNumList.append(team.teamNumber)
        teamEloList.append(team.eloRating)

    teamDict = dict(zip(teamNumList, teamEloList))
    print("rankings")

    rankedTeamDict = dict(sorted(teamDict.items(), key=lambda item: item[1], reverse=True))
    if shouldPrint:
        print(teamName, ":", teamEloList[teamNumList.index(teamName)])
    return teamEloList[teamNumList.index(teamName)], rankedTeamDict


def printDict(dict):
    place = 1
    for key, value in dict.items():
        print(place, "-", key, ':', value)
        place = place + 1


def predictMatch (team1, team2, team3, team4):
    team1List = calcEloFromAllEvents(team1)
    team2List = calcEloFromAllEvents(team2)
    team3List = calcEloFromAllEvents(team3)
    team4List = calcEloFromAllEvents(team4)
    # Creating a copy
    teamList = list(team1List)
    print(len(teamList))

    # Using extend() method
    teamNumbers = [t.teamNumber for t in teamList]
    for y in team2List:
        if y.teamNumber not in teamNumbers:
            teamList.extend([y])
            teamNumbers.append(y.teamNumber)

    for y in team3List:
        if y.teamNumber not in teamNumbers:
            teamList.extend([y])
            teamNumbers.append(y.teamNumber)

    for y in team4List:
        if y.teamNumber not in teamNumbers:
            teamList.extend([y])
            teamNumbers.append(y.teamNumber)

    print(elo.predictMatch(
              teamList[getPlayerIndex(teamList, team1)],
              teamList[getPlayerIndex(teamList, team2)],
              teamList[getPlayerIndex(teamList, team3)],
              teamList[getPlayerIndex(teamList, team4)]))




def getAvgElo(teamNum, iterations=1):
  avgElo = 0;
  for i in range(iterations):
    updatedTeamSet = calcEloFromAllEvents(teamNum)
    teamElo, rankedTeamDict = teamRanking(teamNum, updatedTeamSet, False)
    avgElo += teamElo
  avgElo /= iterations

  return avgElo


