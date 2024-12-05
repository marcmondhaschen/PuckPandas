--import table create statements


create table `nhl_pandas_import`.`game_center_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `season` varchar(8) DEFAULT NULL,
  `gameType` int DEFAULT NULL,
  `limitedScoring` tinyInt DEFAULT NULL,
  `gameDate` date DEFAULT NULL,
  `venue.default` varchar(50) DEFAULT NULL,
  `venueLocation.default` varchar(50) DEFAULT NULL,
  `startTimeUTC` datetime DEFAULT NULL,
  `easternUTCOffset` varchar(10) DEFAULT NULL,
  `venueUTCOffset` varchar(10) DEFAULT NULL,
  `gameState` varchar(5) DEFAULT NULL,
  `gameScheduleState` varchar(5) DEFAULT NULL,
  `periodDescriptor.number` int DEFAULT NULL,
  `periodDescriptor.periodType` varchar(5) DEFAULT NULL,
  `periodDescriptor.maxRegulationPeriods` int DEFAULT NULL,
  `awayTeam.id` int DEFAULT NULL,
  `awayTeam.name.default` varchar(20) DEFAULT NULL,
  `awayTeam.abbrev` varchar(5) DEFAULT NULL,
  `awayTeam.score` int DEFAULT NULL,
  `awayTeam.sog` int DEFAULT NULL,
  `awayTeam.logo` varchar(100) DEFAULT NULL,
  `awayTeam.placename.default` varchar(50) DEFAULT NULL,
  `awayTeam.placenameWithPreposition.default` varchar(50) DEFAULT NULL,
  `homeTeam.id` int DEFAULT NULL,
  `homeTeam.name.default` varchar(20) DEFAULT NULL,
  `homeTeam.abbrev` varchar(5) DEFAULT NULL,
  `homeTeam.score` int DEFAULT NULL,
  `homeTeam.sog` int DEFAULT NULL,
  `homeTeam.logo` varchar(100) DEFAULT NULL,
  `homeTeam.placename.default` varchar(50) DEFAULT NULL,
  `homeTeam.placenameWithPreposition.default` varchar(50) DEFAULT NULL,
  `shootoutInuse` tinyint DEFAULT NULL,
  `otInUse` tinyint DEFAULT NULL,
  `clock.timeRemaining` varchar(10) DEFAULT NULL,
  `clock.secondsRemaining` int DEFAULT NULL,
  `clock.running` tinyint DEFAULT NULL,
  `clock.inIntermission` tinyint DEFAULT NULL,
  `displayPeriod` int DEFAULT NULL,
  `gameOutcome.lastPeriodType` varchar(5) DEFAULT NULL,
  `gameVideo.threeMinRecap` bigint default null,
  `regPeriods` int DEFAULT NULL,
  `summary.seasonSeriesWins.awayTeamWins` int DEFAULT NULL,
  `summary.seasonSeriesWins.homeTeamWins` int DEFAULT NULL,
  `summary.seasonSeriesWins.neededToWin` int DEFAULT NULL,
  `summary.linescore.totals.away` int DEFAULT NULL,
  `summary.linescore.totals.home` int DEFAULT NULL,
  `summary.gameReports.gameSummary` varchar(100) DEFAULT NULL,
  `summary.gameReports.eventSummary` varchar(100) DEFAULT NULL,
  `summary.gameReports.playByPlay` varchar(100) DEFAULT NULL,
  `summary.gameReports.faceoffSummary` varchar(100) DEFAULT NULL,
  `summary.gameReports.faceoffComparison` varchar(100) DEFAULT NULL,
  `summary.gameReports.rosters` varchar(100) DEFAULT NULL,
  `summary.gameReports.shotSummary` varchar(100) DEFAULT NULL,
  `summary.gameReports.shiftChart` varchar(100) DEFAULT NULL,
  `summary.gameReports.toiAway` varchar(100) DEFAULT NULL,
  `summary.gameReports.toiHome` varchar(100) DEFAULT NULL,
  `summary.awayTeam.gameInfo.headCoach.default` varchar(100) DEFAULT NULL,
  `summary.homeTeam.gameInfo.headCoach.default` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`),
  KEY `season` (`season`),
  KEY `gameType` (`gameType`),
  KEY `gameDate` (`gameDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`game_center_right_rail_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `seasonSeriesWins.awayTeamWins` int DEFAULT NULL,
  `seasonSeriesWins.homeTeamWins` int DEFAULT NULL,
  `seasonSeriesWins.neededToWin` int DEFAULT NULL,
  `gameInfo.awayTeam.headCoach.default` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameInfo.homeTeam.headCoach.default` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameVideo.threeMinRecap` bigint DEFAULT NULL,
  `linescore.totals.away` int default NULL,
  `linescore.totals.home` int default NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`games_import` (
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `seasonId_index` (`seasonId`),
  KEY `gameDate_index` (`gameDate`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`games_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `lastDateUpdated` datetime DEFAULT NULL,
  `gameFound` tinyint DEFAULT NULL,
  `gameCenterFound` tinyint DEFAULT NULL,
  `tvBroadcastsFound` tinyint DEFAULT NULL,
  `playsFound` tinyint DEFAULT NULL,
  `rosterSpotsFound` tinyint DEFAULT NULL,
  `teamGameStatsFound` tinyint DEFAULT NULL,
  `seasonSeriesFound` tinyint DEFAULT NULL,
  `linescoreByPeriodFound` tinyint DEFAULT NULL,
  `refereesFound` tinyint DEFAULT NULL,
  `linesmenFound` tinyint DEFAULT NULL,
  `scratchesFound` tinyint DEFAULT NULL,
  `shiftsFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `gameId_UNIQUE` (`gameId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`goalie_career_totals_import` (
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
  `regularSeason.timeOnIceMinutes` int DEFAULT '0',
  `regularSeason.timeOnIceSeconds` int DEFAULT NULL,
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
  `playoffs.timeOnIceMinutes` int DEFAULT '0',
  `playoffs.timeOnIceSeconds` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`goalie_season_import` (
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
  `timeOnIceMinutes` int DEFAULT '0',
  `timeOnIceSeconds` int DEFAULT NULL,
  `wins` int DEFAULT NULL,
  `teamName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `savePctg` decimal(10,8) DEFAULT '0.00000000',
  `shotsAgainst` int DEFAULT NULL,
  `otLosses` int DEFAULT NULL,
  `assists` int DEFAULT NULL,
  `gamesStarted` int DEFAULT NULL,
  `goals` int DEFAULT NULL,
  `pim` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`linesmen_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `default` varchar(100) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`player_award_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trophy.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`player_bios_import` (
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
  `draftDetails.teamAbbrev` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `draftDetails.round` int DEFAULT NULL,
  `draftDetails.pickInRound` int DEFAULT NULL,
  `draftDetails.overallPick` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`),
  KEY `teamId_index` (`currentTeamId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`plays_import` (
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
  KEY `typeCode_index` (`typeCode`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `player_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `lastDateUpdated` datetime DEFAULT NULL,
  `playerFound` tinyint DEFAULT NULL,
  `playerBioFound` tinyint DEFAULT NULL,
  `careerTotalsFound` tinyint DEFAULT NULL,
  `seasonTotalsFound` tinyint DEFAULT NULL,
  `awardsFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `playerId_UNIQUE` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci


create table `nhl_pandas_import`.`referees_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `default` varchar(100) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`roster_spots_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `teamId` int NOT NULL,
  `playerId` int NOT NULL,
  `sweaterNumber` int DEFAULT NULL,
  `positionCode` varchar(5) DEFAULT NULL,
  `headshot` varchar(100) DEFAULT NULL,
  `firstName` varchar(75) DEFAULT NULL,
  `lastName` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `teamId` (`teamId`),
  KEY `playerId` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`rosters_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `playerId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId` (`seasonId`),
  KEY `playerId` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`scratches_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `playerId` int NOT NULL,
  `firstName.default` varchar(75) DEFAULT '',
  `lastName.default` varchar(75) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`season_series_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `seriesNumber` int NOT NULL,
  `refGameId` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`shift_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `logDate` datetime DEFAULT NULL,
  `checked` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gameId_index` (`gameId`),
  KEY `logDate_index` (`logDate`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`shifts_import` (
  `id` int NOT NULL,
  `detailCode` int DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `endTime` time DEFAULT NULL,
  `eventDescription` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `eventDetails` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `eventNumber` int DEFAULT NULL,
  `firstName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameId` int DEFAULT NULL,
  `hexValue` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `period` int DEFAULT NULL,
  `playerId` int DEFAULT NULL,
  `shiftNumber` int DEFAULT NULL,
  `startTime` time DEFAULT NULL,
  `teamAbbrev` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `teamId` int DEFAULT NULL,
  `teamName` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `typeCode` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gameId_index` (`gameId`),
  KEY `playerId_index` (`playerId`),
  KEY `teamId_index` (`teamId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`shots_by_period_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `period` int NOT NULL,
  `periodDescriptor.number` int DEFAULT NULL,
  `periodDescriptor.periodType` int DEFAULT NULL,
  `periodDescriptor.maxRegulationPeriods` int DEFAULT NULL,
  `away` int DEFAULT NULL,
  `home` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`skater_career_totals_import` (
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
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`skater_season_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `assists` int DEFAULT NULL,
  `gameTypeId` int DEFAULT NULL,
  `gamesPlayed` int DEFAULT NULL,
  `goals` int DEFAULT NULL,
  `leagueAbbrev` varchar(12) DEFAULT NULL,
  `pim` int DEFAULT '0',
  `points` int DEFAULT NULL,
  `season` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` int DEFAULT NULL,
  `teamName.default` varchar(50) DEFAULT NULL,
  `gameWinningGoals` int DEFAULT NULL,
  `plusMinus` int DEFAULT NULL,
  `powerPlayGoals` int DEFAULT NULL,
  `shorthandedGoals` int DEFAULT NULL,
  `shots` int DEFAULT NULL,
  `faceoffWinningPctg` decimal(10,8) DEFAULT '0.00000000',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `playerId` (`playerId`),
  KEY `gameTypeId` (`gameTypeId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`table_update_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tableName` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastDateUpdated` datetime DEFAULT NULL,
  `updateFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `tableName` (`tableName`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `nhl_pandas_import`.`team_game_stats_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `category` varchar(20) DEFAULT NULL,
  `awayValue` varchar(20) DEFAULT NULL,
  `homeValue` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`team_seasons_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId_index` (`seasonId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `nhl_pandas_import`.`teams_import` (
  `teamId` int NOT NULL,
  `franchiseId` int NOT NULL,
  `fullName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `leagueId` int NOT NULL,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`teamId`),
  KEY `franchiseId_index` (`franchiseId`),
  KEY `triCode_index` (`triCode`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `tv_broadcasts_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `broadcastId` int NOT NULL,
  `market` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `countryCode` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `network` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequenceNumber` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `broadcastId` (`broadcastId`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci