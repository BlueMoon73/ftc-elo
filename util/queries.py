from string import Template

teamEventListTemplate = Template("""
{
    teamByNumber(number: $teamNumber){
      matches (season: 2024){
        eventCode
      }
  }
} """)

eventMatchesTemplate = Template(""" {
  eventByCode(season:2024, code:"$code"){
    matches { 
      teams {teamNumber}
      scores {
        ... on MatchScores2024	{ 
          red {totalPointsNp}
          blue {totalPointsNp}
        }
      }
    }
  }
}""")

eventDateTemplate = Template(""" 
{
  eventByCode(season:2024, code:"$code"){
    end
  }
}
""")

teamNameTemplate = Template ("""{ 
 teamByNumber(number: $teamNum) {name}
}
""")

worldRecordRegion = """ {
    tradWorldRecord(season:2024){
    eventCode
  }
}"""

numMatchesPlayed = """ {
    matchesPlayedCount(season:2024)
} """