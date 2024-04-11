# import table create statements

CREATE TABLE `game_play_by_play_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `eventId` int NOT NULL,
  `period` int DEFAULT NULL,
  `periodType` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timeInPeriod` time DEFAULT '00:00:00',
  `timeRemaining` time DEFAULT '00:00:00',
  `situationCode` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `typeCode` int DEFAULT NULL,
  `typeDescKey` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sortOrder` int DEFAULT NULL,
  `eventOwnerTeamId` int DEFAULT NULL,
  `losingPlayerId` int DEFAULT NULL,
  `winningPlayerId` int DEFAULT NULL,
  `xCoord` decimal(9,8) DEFAULT NULL,
  `yCoord` decimal(9,8) DEFAULT NULL,
  `zoneCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reason` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hittingPlayerId` int DEFAULT NULL,
  `hitteePlayerId` int DEFAULT NULL,
  `shotType` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shootingPlayerId` int DEFAULT NULL,
  `goalieInNetId` int DEFAULT NULL,
  `awaySOG` int DEFAULT NULL,
  `homeSOG` int DEFAULT NULL,
  `playerId` int DEFAULT NULL,
  `blockingPlayerId` int DEFAULT NULL,
  `secondaryReason` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `detailTypeCode` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `detailDescKey` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `detailDuration` int DEFAULT NULL,
  `detailCommittedByPlayerId` int DEFAULT NULL,
  `detailDrawnByPlayerId` int DEFAULT NULL,
  `scoringPlayerId` int DEFAULT NULL,
  `scoringPlayerTotal` int DEFAULT NULL,
  `assist1PlayerId` int DEFAULT NULL,
  `assist1PlayerTotal` int DEFAULT NULL,
  `assist2PlayerId` int DEFAULT NULL,
  `assist2PlayerTotal` int DEFAULT NULL,
  `awayScore` int DEFAULT NULL,
  `homeScore` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gameId_index` (`gameId`),
  KEY `eventId` (`eventId`),
  KEY `typeCode` (`typeCode`),
  KEY `typeCode_index` (`typeCode`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `game_rosters_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `teamId` int NOT NULL,
  `playerId` int NOT NULL,
  `sweaterNumber` int DEFAULT NULL,
  `positionCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `firstName.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastName.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gameId_index` (`gameId`),
  KEY `teamId_index` (`teamId`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `games_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameType` int NOT NULL,
  `gameDate` date DEFAULT NULL,
  `venue` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `neutralSite` tinyint DEFAULT NULL,
  `startTimeUTC` datetime DEFAULT NULL,
  `venueUTCOffset` time DEFAULT '00:00:00',
  `venueTimezone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameState` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameScheduleState` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayTeam` int NOT NULL,
  `awayTeamSplitSquad` tinyint DEFAULT NULL,
  `awayTeamScore` int DEFAULT NULL,
  `homeTeam` int NOT NULL,
  `homeTeamSplitSquad` tinyint DEFAULT NULL,
  `homeTeamScore` int DEFAULT NULL,
  `periodType` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameOutcome` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `datePBPChecked` date DEFAULT NULL,
  `PBPCheckSuccess` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `seasonId_index` (`seasonId`),
  KEY `gameDate_index` (`gameDate`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `goalie_career_totals_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `regularSeason.gamesPlayed` int DEFAULT '0',
  `regularSeason.goals` int DEFAULT '0',
  `regularSeason.assists` int DEFAULT '0',
  `regularSeason.pim` int DEFAULT '0',
  `regularSeason.gamesStarted` int DEFAULT '0',
  `regularSeason.points` int DEFAULT '0',
  `regularSeason.wins` int DEFAULT '0',
  `regularSeason.losses` int DEFAULT '0',
  `regularSeason.otLosses` int DEFAULT '0',
  `regularSeason.shotsAgainst` int DEFAULT '0',
  `regularSeason.goalsAgainst` int DEFAULT '0',
  `regularSeason.goalsAgainstAvg` decimal(10,8) DEFAULT '0.00000000',
  `regularSeason.savePctg` decimal(10,8) DEFAULT '0.00000000',
  `regularSeason.shutouts` int DEFAULT '0',
  `regularSeason.timeOnIce` time DEFAULT '00:00:00',
  `playoffs.gamesPlayed` int DEFAULT '0',
  `playoffs.goals` int DEFAULT '0',
  `playoffs.assists` int DEFAULT '0',
  `playoffs.pim` int DEFAULT '0',
  `playoffs.gamesStarted` int DEFAULT '0',
  `playoffs.points` int DEFAULT '0',
  `playoffs.wins` int DEFAULT '0',
  `playoffs.losses` int DEFAULT '0',
  `playoffs.otLosses` int DEFAULT '0',
  `playoffs.shotsAgainst` int DEFAULT '0',
  `playoffs.goalsAgainst` int DEFAULT '0',
  `playoffs.goalsAgainstAvg` decimal(10,8) DEFAULT '0.00000000',
  `playoffs.savePctg` decimal(10,8) DEFAULT '0.00000000',
  `playoffs.shutouts` int DEFAULT '0',
  `playoffs.timeOnIce` time DEFAULT '00:00:00',
  `regularSeason.timeOnIceSeconds` int DEFAULT NULL,
  `playoffs.timeOnIceSeconds` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `goalie_season_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `gameTypeId` int DEFAULT NULL,
  `gamesPlayed` int DEFAULT NULL,
  `goalsAgainst` int DEFAULT NULL,
  `goalsAgainstAvg` decimal(11,8) DEFAULT '0.00000000',
  `leagueAbbrev` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `losses` int DEFAULT NULL,
  `season` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sequence` int DEFAULT NULL,
  `shutouts` int DEFAULT NULL,
  `ties` int DEFAULT NULL,
  `timeOnIce` time DEFAULT '00:00:00',
  `wins` int DEFAULT NULL,
  `teamName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `savePctg` decimal(10,8) DEFAULT '0.00000000',
  `shotsAgainst` int DEFAULT NULL,
  `otLosses` int DEFAULT NULL,
  `assists` int DEFAULT NULL,
  `gamesStarted` int DEFAULT NULL,
  `goals` int DEFAULT NULL,
  `pim` int DEFAULT NULL,
  `timeOnIceSeconds` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_award_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trophy.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_bios_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `isActive` tinyint DEFAULT NULL,
  `currentTeamId` int DEFAULT NULL,
  `currentTeamAbbrev` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sweaterNumber` int DEFAULT NULL,
  `position` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `heightInInches` int DEFAULT NULL,
  `heightInCentimeters` int DEFAULT NULL,
  `weightInPounds` int DEFAULT NULL,
  `weightInKilograms` int DEFAULT NULL,
  `birthDate` date DEFAULT NULL,
  `birthCountry` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shootsCatches` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `inTop100AllTime` tinyint DEFAULT NULL,
  `inHHOF` tinyint DEFAULT NULL,
  `firstName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthCity.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birthStateProvince.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `draftDetails.year` int DEFAULT NULL,
  `draftDetails.teamAbbrev` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `draftDetails.round` int DEFAULT NULL,
  `draftDetails.pickInRound` int DEFAULT NULL,
  `draftDetails.overallPick` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`),
  KEY `teamId_index` (`currentTeamId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_career_totals_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `regularSeason.gamesPlayed` int DEFAULT NULL,
  `regularSeason.goals` int DEFAULT NULL,
  `regularSeason.assists` int DEFAULT NULL,
  `regularSeason.pim` int DEFAULT NULL,
  `regularSeason.points` int DEFAULT NULL,
  `regularSeason.plusMinus` int DEFAULT NULL,
  `regularSeason.powerPlayGoals` int DEFAULT NULL,
  `regularSeason.powerPlayPoints` int DEFAULT NULL,
  `regularSeason.shorthandedPoints` int DEFAULT NULL,
  `regularSeason.gameWinningGoals` int DEFAULT NULL,
  `regularSeason.otGoals` int DEFAULT NULL,
  `regularSeason.shots` int DEFAULT NULL,
  `regularSeason.shootingPctg` decimal(10,8) DEFAULT '0.00000000',
  `regularSeason.faceoffWinningPctg` decimal(10,8) DEFAULT '0.00000000',
  `regularSeason.avgToi` time DEFAULT '00:00:00',
  `regularSeason.shorthandedGoals` int DEFAULT NULL,
  `playoffs.gamesPlayed` int DEFAULT NULL,
  `playoffs.goals` int DEFAULT NULL,
  `playoffs.assists` int DEFAULT NULL,
  `playoffs.pim` int DEFAULT NULL,
  `playoffs.points` int DEFAULT NULL,
  `playoffs.plusMinus` int DEFAULT NULL,
  `playoffs.powerPlayGoals` int DEFAULT NULL,
  `playoffs.powerPlayPoints` int DEFAULT NULL,
  `playoffs.shorthandedPoints` int DEFAULT NULL,
  `playoffs.gameWinningGoals` int DEFAULT NULL,
  `playoffs.otGoals` int DEFAULT NULL,
  `playoffs.shots` int DEFAULT NULL,
  `playoffs.shootingPctg` decimal(10,8) DEFAULT '0.00000000',
  `playoffs.faceoffWinningPctg` decimal(10,8) DEFAULT '0.00000000',
  `playoffs.avgToi` time DEFAULT '00:00:00',
  `playoffs.shorthandedGoals` int DEFAULT NULL,
  `regularSeason.avgToiSeconds` int DEFAULT NULL,
  `playoffs.avgToiSeconds` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `logDate` datetime DEFAULT NULL,
  `playerBio` tinyint DEFAULT NULL,
  `career` tinyint DEFAULT NULL,
  `season` tinyint DEFAULT NULL,
  `awards` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_season_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `assists` int DEFAULT '0',
  `gameTypeId` int DEFAULT '0',
  `gamesPlayed` int DEFAULT '0',
  `goals` int DEFAULT '0',
  `leagueAbbrev` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pim` int DEFAULT '0',
  `points` int DEFAULT '0',
  `season` int DEFAULT NULL,
  `sequence` int DEFAULT NULL,
  `teamName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameWinningGoals` int DEFAULT '0',
  `plusMinus` int DEFAULT '0',
  `powerPlayGoals` int DEFAULT '0',
  `shorthandedGoals` int DEFAULT '0',
  `shots` int DEFAULT '0',
  `faceoffWinningPctg` decimal(9,8) DEFAULT '0.00000000',
  `avgToi` time DEFAULT '00:00:00',
  `otGoals` int DEFAULT '0',
  `powerPlayPoints` int DEFAULT '0',
  `shootingPctg` decimal(9,8) DEFAULT '0.00000000',
  `shorthandedPoints` int DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`),
  KEY `seasonId_index` (`season`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `rosters_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `playerId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId` (`seasonId`),
  KEY `playerId` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `shiftcharts_import` (
	`id` int NOT NULL,
    `detailCode` int default NULL,
    `duration` time DEFAULT NULL,
    `endTime` time DEFAULT NULL,
    `eventDescription` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `eventDetails` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `eventNumber` int default NULL,
    `firstName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `gameId` int default NULL,
    `hexValue` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `lastName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
	`period` int default NULL,
    `playerId` int default NULL,
    `shiftNumber` int default NULL,
    `startTime` time DEFAULT NULL,
    `teamAbbrev` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `teamId` int default NULL,
    `teamName` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `typeCode` int default NULL,
    primary key (`id`),
    key `gameId_index` (`gameId`),
    key `playerId_index` (`playerId`),
    key `teamId_index` (`teamId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `team_seasons_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId_index` (`seasonId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `teams_import` (
  `teamId` int NOT NULL,
  `franchiseId` int NOT NULL,
  `fullName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `leagueId` int NOT NULL,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`teamId`),
  KEY `franchiseId_index` (`franchiseId`),
  KEY `triCode_index` (`triCode`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

