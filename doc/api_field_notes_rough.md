# rough notes on api fields to be captured for each table

table `teams`
	`teamId` 		data/ [index] /id
	`franchiseId` 	data/ [index] /franchiseId
	`fullName` 		data/ [index] /fullName
	`leagueId` 		data/ [index] /leagueId
	`triCode` 		data/ [index] /triCode


table `team_seasons`
	`id` 			AUTO GENERATE INDEX COLUMN
	`triCode` 		INSERT
	`seasonId` 		[index]


table `games`
	`gameId` 			games/ [index] /id
	`seasonId` 			games/ [index] /season
	`gameType` 			games/ [index] /gameType
	`gameDate` 			games/ [index] /gameDate
	`venue` 			games/ [index] /venue/default
	`neutralSite` 		games/ [index] /neutralSite
	`startTimeUTC` 		games/ [index] /startTimeUTC
	`venueUTCOffset`	games/ [index] /venueUTCOffset
	`venueTimezone` 	games/ [index] /venueTimezone
	`gameState` 		games/ [index] /gameState
	`gameScheduleState` games/ [index] /gameScheduleState
	`awayTeam` 			games/ [index] /awayTeam/id
	`awayTeamSplitSquad`games/ [index] /awayTeam/awaySplitSquad
	`awayTeamScore` 	games/ [index] /awayTeam/score
	`homeTeam` 			games/ [index] /homeTeam/id
	`homeTeamSplitSquad`games/ [index] /homeTeam/homeSplitSquad
	`homeTeamScore` 	games/ [index] /homeTeam/score
	`periodType` 		games/ [index] /periodDescriptor/periodType
	`gameOutcome` 		games/ [index] /gameOutcome/lastPeriodType


`game_play_by_play`
	`id` 			AUTO GENERATE INDEX COLUMN
	`gameId` 		INSERT
	`eventId` 		plays/ [index] /eventId
	`period` 		plays/ [index] /periodDescriptor/number
	`periodType` 	plays/ [index] /periodDescriptor/periodType
	`timeInPeriod` 	plays/ [index] /timeInPeriod
	`timeRemaining` plays/ [index] /timeRemaining
	`situationCode` plays/ [index] /situationCode
	`typeCode` 		plays/ [index] /typeCode
	`typeDescKey` 	plays/ [index] /typeDescKey
	`sortOrder` 	plays/ [index] /sortOrder


table `game_rosters`
	`id` 			AUTO GENERATE INDEX COLUMN
	`gameId` 		INSERT
	`teamId` 		rosterSpots/ [index] /teamId
	`playerId` 		rosterSpots/ [index] /playerId
	`sweaterNumber` rosterSpots/ [index] /sweaterNumber
	`positionCode` 	rosterSpots/ [index] /positionCode


table `rosters`
	`id` 			AUTO GENERATE INDEX COLUMN
	`triCode` 		INSERT
	`seasonId` 		INSERT
	`playerId`
					forwards/ [index] /id
					defensemen/ [index] /id
					goalies/ [index] /id


table `player_bios`
	`playerId` 				playerId
	`isActive` 				isActive
	`currentTeamId` 		currentTeamId
	`firstName` 			firstName/default
	`lastName` 				lastName/default
	`sweaterNumber` 		sweaterNumber
	`positionCode` 			positionCode
	`heightInInches` 		heightInInches
	`heightInCentimeters` 	heightInCentimeters
	`weightInPounds` 		weightInPounds
	`weightInKilograms` 	weightInKilograms
	`birthDate` 			birthDate
	`birthCity` 			birthCity/default
	`birthStateProvince` 	birthStateProvince/default
	`birthCountry` 			birthCountry
	`shootsCatches` 		shootsCatches


table `player_career_totals`
	`playerId` 					playerId
	`gamesPlayedReg` 			careerTotals/regularSeason/gamesPlayed
	`goalsReg` 					careerTotals/regularSeason/goals
	`assistsReg` 				careerTotals/regularSeason/assists
	`pimReg` 					careerTotals/regularSeason/pim
	`pointsReg` 				careerTotals/regularSeason/points
	`plusMinusReg` 				careerTotals/regularSeason/plusMinus
	`powerPlayGoalsReg` 		careerTotals/regularSeason/powerPlayGoals
	`powerPlayPointsReg` 		careerTotals/regularSeason/powerPlayPoints
	`shortHandedGoalsReg` 		careerTotals/regularSeason/shortHandedGoals
	`shortHandedPointsReg` 		careerTotals/regularSeason/shortHandedPoints
	`gameWinningGoalsReg` 		careerTotals/regularSeason/gameWinningGoals
	`otGoalsReg` 				careerTotals/regularSeason/otGoals
	`shotsReg` 					careerTotals/regularSeason/shots
	`shootingPctgReg` 			careerTotals/regularSeason/shootingPctg
	`faceoffWinningPctgReg` 	careerTotals/regularSeason/faceoffWinningPctg
	`avgToiReg` 				careerTotals/regularSeason/avgToi
	`gamesPlayedPlayoff` 		careerTotals/playoffs/gamesPlayed
	`goalsPlayoff` 				careerTotals/playoffs/goals
	`assistsPlayoff` 			careerTotals/playoffs/assists
	`pimPlayoff` 				careerTotals/playoffs/pim
	`pointsPlayoff` 			careerTotals/playoffs/points
	`plusMinusPlayoff` 			careerTotals/playoffs/plusMinus
	`powerPlayGoalsPlayoff` 	careerTotals/playoffs/powerPlayGoals
	`powerPlayPointsPlayoff` 	careerTotals/playoffs/powerPlayPoints
	`shortHandedGoalsPlayoff` 	careerTotals/playoffs/shortHandedGoals
	`shortHandedPointsPlayoff` 	careerTotals/playoffs/shortHandedPoints
	`gameWinningGoalsPlayoff` 	careerTotals/playoffs/gameWinningGoals
	`otGoalsPlayoff` 			careerTotals/playoffs/otGoals
	`shotsPlayoff` 				careerTotals/playoffs/shots
	`shootingPctgPlayoff` 		careerTotals/playoffs/shootingPctg
	`faceoffWinningPctgPlayoff` careerTotals/playoffs/faceoffWinningPctg
	`avgToiPlayoff` 			careerTotals/playoffs/avgToi
	

table `player_season_totals`
	`id` 					AUTO GENERATE INDEX COLUMN
	`playerId` 				playerId
	`seasonId` 				seasonTotals/ [index] /season
	`assists` 				seasonTotals/ [index] /assists
	`avgToiPlayoff` 		seasonTotals/ [index] /avgToi
	`faceoffWinningPctg`  	seasonTotals/ [index] /faceoffWinningPctg
	`gameTypeId` 			seasonTotals/ [index] /gameTypeId
	`gameWinningGoals` 		seasonTotals/ [index] /gameWinningGoals
	`gamesPlayed` 			seasonTotals/ [index] /gamesPlayed
	`goals` 				seasonTotals/ [index] /goals
	`leagueAbbrev` 			seasonTotals/ [index] /leagueAbbrev
	`otGoals` 				seasonTotals/ [index] /otGoals
	`pim` 					seasonTotals/ [index] /pim
	`plusMinus` 			seasonTotals/ [index] /plusMinus
	`points` 				seasonTotals/ [index] /points
	`powerPlayGoals` 		seasonTotals/ [index] /powerPlayGoals
	`powerPlayPoints` 		seasonTotals/ [index] /powerPlayPoints
	`sequence` 				seasonTotals/ [index] /sequence
	`shootingPctg`  		seasonTotals/ [index] /shootingPctg
	`shorthandedGoals` 		seasonTotals/ [index] /shorthandedGoals
	`shorthandedPoints` 	seasonTotals/ [index] /shorthandedPoints
	`shots` 				seasonTotals/ [index] /shots
	`teamName` 				seasonTotals/ [index] /teamName/default


table `player_awards`
	`id` 			AUTO GENERATE INDEX COLUMN
	`playerId` 		playerId
	`trophyName` 	awards/ [index] /trophy/default
	`seasonId` 		awards/ [index] /seasons/ [index] /seasonId
