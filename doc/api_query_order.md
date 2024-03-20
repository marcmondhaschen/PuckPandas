# a rough guide to api queries to be run, their order, and the fields to be captured from each

1. Run https://api.nhle.com/stats/rest/en/team
	- Build [TEAM TRI-CODE] list
	
2. Run https://api-web.nhle.com/v1/roster-season/ [TEAM TRI-CODE]
	- Loop for each [TEAM TRI-CODE] 
	- Build [TEAM TRI-CODE] , [SEASON ID] list

3. Run https://api-web.nhle.com/v1/club-schedule-season/ [TEAM TRI-CODE]/ [SEASON ID]
	- Loop for each [TEAM TRI-CODE], [SEASON ID]
	- Build [GAME ID] summary details as below
		games/ [index] /id
		games/ [index] /season
		games/ [index] /gameType
		games/ [index] /gameDate
		games/ [index] /venue/default
		games/ [index] /neutralSite
		games/ [index] /startTimeUTC
		games/ [index] /venueUTCOffset
		games/ [index] /venueTimezone
		games/ [index] /gameState
		games/ [index] /gameScheduleState
		games/ [index] /tvBroadcasts
		games/ [index] /awayTeam/id
		games/ [index] /awayTeam/awaySplitSquad
		games/ [index] /awayTeam/score
		games/ [index] /homeTeam/id
		games/ [index] /homeTeam/homeSplitSquad
		games/ [index] /homeTeam/score
		games/ [index] /periodDescriptor/periodType
		games/ [index] /gameOutcome/lastPeriodType
	- Filter for duplicates! This should pull each game twice, as it will appear on both teams' schedules.

4. Run https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/play-by-play
	- Loop for each [GAME ID]
	- For each game, append to tables below
		- play by play
			plays/ [index] /eventId
			plays/ [index] /period
			plays/ [index] /periodDescriptor/number
			plays/ [index] /periodDescriptor/periodType
			plays/ [index] /timeInPeriod
			plays/ [index] /timeRemaining
			plays/ [index] /situationCode
			plays/ [index] /typeCode
			plays/ [index] /typeDescKey
			plays/ [index] /sortOrder
			plays/ [index] /details/eventOwnerTeamId
			plays/ [index] /details/losingPlayerId
			plays/ [index] /details/winningPlayerId
			plays/ [index] /details/xCoord
			plays/ [index] /details/yCoord
			plays/ [index] /details/zoneCode
			plays/ [index] /details/reason
			plays/ [index] /details/hittingPlayerId
			plays/ [index] /details/hitteePlayerId
			plays/ [index] /details/shotType
			plays/ [index] /details/shootingPlayerId
			plays/ [index] /details/goalieInNetId
			plays/ [index] /details/awaySOG
			plays/ [index] /details/homeSOG
			plays/ [index] /details/playerId
			plays/ [index] /details/blockingPlayerId
			plays/ [index] /details/secondaryReason
			plays/ [index] /details/detailTypeCode
			plays/ [index] /details/detailDescKey
			plays/ [index] /details/detailDuration
			plays/ [index] /details/detailCommittedByPlayerId
			plays/ [index] /details/scoringPlayerId
			plays/ [index] /details/scoringPlayerTotal
			plays/ [index] /details/assist1PlayerId
			plays/ [index] /details/assist1PlayerTotal
			plays/ [index] /details/assist2PlayerId
			plays/ [index] /details/assist2PlayerTotal
			plays/ [index] /details/awayScore
			plays/ [index] /details/homeScore
			
		- rosters
			rosterSpots/ [index] /teamId
			rosterSpots/ [index] /playerId
			rosterSpots/ [index] /sweaterNumber
			rosterSpots/ [index] /positionCode

5. Run https://api-web.nhle.com/v1/roster/ [TEAM TRI-CODE]/ [SEASON ID]
	- Loop for each [TEAM TRI-CODE], [SEASON ID]
	- Build [PLAYER ID] list
		append together from three queries:
			forwards/ [index] /id
			defensemen/ [index] /id
			goalies/ [index] /id

6. Run https://api-web.nhle.com/v1/player/ [PLAYER ID]/landing
	- Loop for each [PLAYER ID]
	- For each player, append to tables below
		player header info
			playerId
			isActive
			currentTeamId
			firstName/default
			lastName/default
			sweaterNumber
			positionCode
			heightInInches
			heightInCentimeters
			weightInPounds
			weightInKilograms
			birthDate
			birthCity/default
			birthStateProvince/default
			birthCountry
			shootsCatches
		career totals
			careerTotals/regularSeason/gamesPlayed
			careerTotals/regularSeason/goals
			careerTotals/regularSeason/assists
			careerTotals/regularSeason/pim
			careerTotals/regularSeason/points
			careerTotals/regularSeason/plusMinus
			careerTotals/regularSeason/powerPlayGoals
			careerTotals/regularSeason/powerPlayPoints
			careerTotals/regularSeason/shortHandedPoints
			careerTotals/regularSeason/gameWinningGoals
			careerTotals/regularSeason/otGoals
			careerTotals/regularSeason/shots
			careerTotals/regularSeason/shootingPctg
			careerTotals/regularSeason/faceoffWinningPctg
			careerTotals/regularSeason/avgToi
			careerTotals/regularSeason/shorthandedGoals
			careerTotals/playoffs/gamesPlayed
			careerTotals/playoffs/goals
			careerTotals/playoffs/assists
			careerTotals/playoffs/pim
			careerTotals/playoffs/points
			careerTotals/playoffs/plusMinus
			careerTotals/playoffs/powerPlayGoals
			careerTotals/playoffs/powerPlayPoints
			careerTotals/playoffs/shortHandedGoals
			careerTotals/playoffs/shortHandedPoints
			careerTotals/playoffs/gameWinningGoals
			careerTotals/playoffs/otGoals
			careerTotals/playoffs/shots
			careerTotals/playoffs/shootingPctg
			careerTotals/playoffs/faceoffWinningPctg
			careerTotals/playoffs/avgToi
			careerTotals/playoffs/shorthandedGoals
		season totals
			seasonTotals/ [index] /assists
			seasonTotals/ [index] /avgToi
			seasonTotals/ [index] /faceoffWinningPctg
			seasonTotals/ [index] /gameTypeId
			seasonTotals/ [index] /gameWinningGoals
			seasonTotals/ [index] /gamesPlayed
			seasonTotals/ [index] /goals
			seasonTotals/ [index] /leagueAbbrev
			seasonTotals/ [index] /otGoals
			seasonTotals/ [index] /pim
			seasonTotals/ [index] /plusMinus
			seasonTotals/ [index] /points
			seasonTotals/ [index] /powerPlayGoals
			seasonTotals/ [index] /powerPlayPoints
			seasonTotals/ [index] /season
			seasonTotals/ [index] /sequence
			seasonTotals/ [index] /shootingPctg
			seasonTotals/ [index] /shorthandedGoals
			seasonTotals/ [index] /shorthandedPoints
			seasonTotals/ [index] /shots
			seasonTotals/ [index] /teamName/default
		awards
			awards/ [index] /trophy/default
			awards/ [index] /seasons/ [index] /seasonId
