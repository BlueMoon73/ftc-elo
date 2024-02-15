import math 
ratingDiff = 500; 

def calcPointFactor(teamScore, opposingTeamScore):
# 0 (abs(1 + teamScore/2 - opposingTeamScore/2) ),2))

    pointFactor = math.pow(math.log10 (1 + abs(teamScore/2 - opposingTeamScore/2) ),2)
    return pointFactor

def calcExpectedPlayerScore(playerRating, opposingTeam1Rating, opposingTeam2Rating):  
    opposingTeam1Score = 1 / (1+math.pow(10,(opposingTeam1Rating- playerRating)/ratingDiff))
    opposingTeam2Score = 1 / (1+math.pow(10,(opposingTeam2Rating- playerRating)/ratingDiff))

    return (opposingTeam1Score + opposingTeam2Score) / 2


def calcExpectedTeamScore (expectedPlayer1Score, expectedPlayer2Score):
    return (expectedPlayer1Score + expectedPlayer2Score) / 2
    
class player: 
    numGames = 0
    k = 50
    gameCutoff = 20 
    eloRating = 400
    # teamNumber = int()

    def __init__(self, number,  rating=400): 
       self.teamNumber = number
      # print(number)
       self.eloRating = rating

    def calcK (self): 
        self.k = 30 / (1 + (self.numGames / self.gameCutoff)) 

    def calcNewRating (self, oldRating, actualScore, expectedTeamScore, pointFactor):
        newRating = oldRating + (self.k * pointFactor) * (actualScore - expectedTeamScore) 
        self.eloRating = newRating
def predictMatch(player1, player2, player3, player4):
    p1Expected =  calcExpectedPlayerScore(player1.eloRating, player3.eloRating, player4.eloRating)
    p2Expected =  calcExpectedPlayerScore(player2.eloRating, player3.eloRating, player4.eloRating)
    p3Expected = calcExpectedPlayerScore(player3.eloRating, player1.eloRating, player2.eloRating)
    p4Expected = calcExpectedPlayerScore(player4.eloRating, player1.eloRating, player2.eloRating)

    # expected team scores
    t1Expected = calcExpectedTeamScore(p1Expected, p2Expected)
    t2Expected = calcExpectedTeamScore(p3Expected, p4Expected)
def matchup(player1, player2, player3, player4, team1Score, team2Score): 
    player1.numGames = player1.numGames + 1; 
    player1.calcK()

    player2.numGames = player2.numGames + 1; 
    player2.calcK()

    player3.numGames = player3.numGames + 1; 
    player3.calcK()

    player4.numGames = player4.numGames + 1; 
    player4.calcK()

    # expected scores
    p1Expected =  calcExpectedPlayerScore(player1.eloRating, player3.eloRating, player4.eloRating)
    p2Expected =  calcExpectedPlayerScore(player2.eloRating, player3.eloRating, player4.eloRating)
    p3Expected = calcExpectedPlayerScore(player3.eloRating, player1.eloRating, player2.eloRating)
    p4Expected = calcExpectedPlayerScore(player4.eloRating, player1.eloRating, player2.eloRating)

    # expected team scores
    t1Expected = calcExpectedTeamScore(p1Expected, p2Expected)
    t2Expected = calcExpectedTeamScore(p3Expected, p4Expected)

    # print(t1Expected)
    # print(t2Expected)

    pFactor = calcPointFactor(team1Score, team2Score)
    # print("p fac" + str(pFactor))
    # print("k fac" + str(player1.k))

    if (team1Score > team2Score): 
        player1.calcNewRating(player1.eloRating, 1, t1Expected, pFactor)
        player2.calcNewRating(player2.eloRating, 1, t1Expected, pFactor)
        
        player3.calcNewRating(player3.eloRating, 0, t2Expected, pFactor)
        player4.calcNewRating(player4.eloRating, 0, t2Expected, pFactor)

    else: 
        player1.calcNewRating(player1.eloRating, 0, t1Expected, pFactor)
        player2.calcNewRating(player2.eloRating, 0, t1Expected, pFactor)
        
        player3.calcNewRating(player3.eloRating, 1, t2Expected, pFactor)
        player4.calcNewRating(player4.eloRating, 1, t2Expected, pFactor)        

# matchup(ls, sc, rb, abi, 200, 198)
ls = player(600)
sc = player(200)
rb = player(400)
abi = player(300)

matchup(ls, sc, rb, abi, 87, 43)
matchup(rb, sc, ls, abi, 32, 93)
matchup(ls, rb, abi, sc, 123, 24)

# print(ls.eloRating)
# print(sc.eloRating)
# print(rb.eloRating)
# print(abi.eloRating)