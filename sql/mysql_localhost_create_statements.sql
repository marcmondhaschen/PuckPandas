# create prod schema
create schema if not exists `puckpandas`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# create prod analysis user
create user `puckpandas`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select on `puckpandas`.* to `puckpandas`@`localhost`;


# create prod transform user
create user `puckpandas_tx`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select, insert, update, delete on `puckpandas`.* to `puckpandas_tx`@`localhost`;
grant select on `puckpandas_import`.* to `puckpandas_tx`@`localhost`;

# create import schema
create schema if not exists `puckpandas_import`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;


# create import user
create user `puckpandas_import`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select, insert, update, delete on `puckpandas_import`.* to `puckpandas_import`@`localhost`;


# create import tables
create table `puckpandas_import`.`game_center_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `season` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameType` int DEFAULT NULL,
  `limitedScoring` tinyint DEFAULT NULL,
  `gameDate` date DEFAULT NULL,
  `venue.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `venueLocation.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `startTimeUTC` datetime DEFAULT NULL,
  `easternUTCOffset` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `venueUTCOffset` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameState` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameScheduleState` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `periodDescriptor.number` int DEFAULT NULL,
  `periodDescriptor.periodType` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `periodDescriptor.maxRegulationPeriods` int DEFAULT NULL,
  `awayTeam.id` int DEFAULT NULL,
  `awayTeam.commonName.default` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayTeam.abbrev` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayTeam.score` int DEFAULT NULL,
  `awayTeam.sog` int DEFAULT NULL,
  `awayTeam.logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayTeam.placeName.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayTeam.placeNameWithPreposition.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeam.id` int DEFAULT NULL,
  `homeTeam.commonName.default` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeam.abbrev` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeam.score` int DEFAULT NULL,
  `homeTeam.sog` int DEFAULT NULL,
  `homeTeam.logo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeam.placeName.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeam.placeNameWithPreposition.default` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `shootoutInUse` tinyint DEFAULT NULL,
  `otInUse` tinyint DEFAULT NULL,
  `clock.timeRemaining` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `clock.secondsRemaining` int DEFAULT NULL,
  `clock.running` tinyint DEFAULT NULL,
  `clock.inIntermission` tinyint DEFAULT NULL,
  `displayPeriod` int DEFAULT NULL,
  `maxPeriods` int DEFAULT NULL,
  `gameOutcome.lastPeriodType` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `regPeriods` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`),
  KEY `season` (`season`),
  KEY `gameType` (`gameType`),
  KEY `gameDate` (`gameDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`game_center_right_rail_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `seasonSeriesWins.awayTeamWins` int DEFAULT NULL,
  `seasonSeriesWins.homeTeamWins` int DEFAULT NULL,
  `seasonSeriesWins.neededToWin` int DEFAULT NULL,
  `gameInfo.awayTeam.headCoach.default` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameInfo.homeTeam.headCoach.default` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gameVideo.threeMinRecap` bigint DEFAULT NULL,
  `linescore.totals.away` int DEFAULT NULL,
  `linescore.totals.home` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`games_import` (
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
  `seriesStatus.round` int DEFAULT NULL,
  `seriesStatus.seriesAbbrev` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seriesStatus.seriesTitle` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seriesStatus.seriesLetter` varchar(3) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seriesStatus.neededToWin` int DEFAULT NULL,
  `seriesStatus.topSeedWins` int DEFAULT NULL,
  `seriesStatus.bottomSeedWins` int DEFAULT NULL,
  `seriesStatus.gameNumberOfSeries` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `seasonId_index` (`seasonId`),
  KEY `gameDate_index` (`gameDate`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`games_import_log` (
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
  `refereesFound` tinyint DEFAULT NULL,
  `linesmenFound` tinyint DEFAULT NULL,
  `scratchesFound` tinyint DEFAULT NULL,
  `shiftsFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `gameId_UNIQUE` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`goalie_career_totals_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`goalie_season_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`linesmen_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `default` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`player_award_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trophy.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `playerId_index` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`player_bios_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`player_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `lastDateUpdated` datetime DEFAULT NULL,
  `playerFound` tinyint DEFAULT NULL,
  `careerTotalsFound` tinyint DEFAULT NULL,
  `seasonTotalsFound` tinyint DEFAULT NULL,
  `awardsFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `playerId_UNIQUE` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`plays_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `eventId` int NOT NULL,
  `periodDescriptor.number` int DEFAULT NULL,
  `periodDescriptor.periodType` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `periodDescriptor.maxRegulationPeriods` int DEFAULT NULL,
  `timeInPeriod` time DEFAULT '00:00:00',
  `timeRemaining` time DEFAULT '00:00:00',
  `situationCode` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeTeamDefendingSide` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `typeCode` int DEFAULT NULL,
  `typeDescKey` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sortOrder` int DEFAULT NULL,
  `details.eventOwnerTeamId` int DEFAULT NULL,
  `details.losingPlayerId` int DEFAULT NULL,
  `details.winningPlayerId` int DEFAULT NULL,
  `details.xCoord` int DEFAULT NULL,
  `details.yCoord` int DEFAULT NULL,
  `details.zoneCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.reason` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.hittingPlayerId` int DEFAULT NULL,
  `details.hitteePlayerId` int DEFAULT NULL,
  `details.shotType` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.shootingPlayerId` int DEFAULT NULL,
  `details.goalieInNetId` int DEFAULT NULL,
  `details.awaySOG` int DEFAULT NULL,
  `details.homeSOG` int DEFAULT NULL,
  `details.playerId` int DEFAULT NULL,
  `details.blockingPlayerId` int DEFAULT NULL,
  `details.secondaryReason` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.typeCode` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.descKey` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `details.duration` int DEFAULT NULL,
  `details.committedByPlayerId` int DEFAULT NULL,
  `details.drawnByPlayerId` int DEFAULT NULL,
  `details.scoringPlayerId` int DEFAULT NULL,
  `details.scoringPlayerTotal` int DEFAULT NULL,
  `details.assist1PlayerId` int DEFAULT NULL,
  `details.assist1PlayerTotal` int DEFAULT NULL,
  `details.assist2PlayerId` int DEFAULT NULL,
  `details.assist2PlayerTotal` int DEFAULT NULL,
  `details.awayScore` int DEFAULT NULL,
  `details.homeScore` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gameId_index` (`gameId`),
  KEY `eventId` (`eventId`),
  KEY `typeCode_index` (`typeCode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`referees_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `default` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`roster_spots_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `teamId` int NOT NULL,
  `playerId` int NOT NULL,
  `sweaterNumber` int DEFAULT NULL,
  `positionCode` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `headshot` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `firstName` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastName` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameId` (`gameId`),
  KEY `teamId` (`teamId`),
  KEY `playerId` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`rosters_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `playerId` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId` (`seasonId`),
  KEY `playerId` (`playerId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`scratches_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `playerId` int NOT NULL,
  `firstName.default` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `lastName.default` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`season_series_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `seriesNumber` int NOT NULL,
  `refGameId` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`shifts_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`skater_career_totals_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`skater_season_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `playerId` int NOT NULL,
  `assists` int DEFAULT NULL,
  `gameTypeId` int DEFAULT NULL,
  `gamesPlayed` int DEFAULT NULL,
  `goals` int DEFAULT NULL,
  `leagueAbbrev` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pim` int DEFAULT '0',
  `points` int DEFAULT NULL,
  `season` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sequence` int DEFAULT NULL,
  `teamName.default` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `plusMinus` int DEFAULT NULL,
  `avgToi` varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `faceoffWinningPctg` decimal(10,8) DEFAULT NULL,
  `gameWinningGoals` int DEFAULT NULL,
  `otGoals` int DEFAULT NULL,
  `powerPlayGoals` int DEFAULT NULL,
  `shootingPctg` decimal(10,8) DEFAULT NULL,
  `shorthandedGoals` int DEFAULT NULL,
  `shorthandedPoints` int DEFAULT NULL,
  `shots` int DEFAULT NULL,
  `teamCommonName.default` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `teamPlaceNameWithPreposition.default` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `playerId` (`playerId`),
  KEY `gameTypeId` (`gameTypeId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci


CREATE TABLE `puckpandas_import`.`table_update_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tableName` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lastDateUpdated` datetime DEFAULT NULL,
  `updateFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `tableName` (`tableName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


create table `puckpandas_import`.`team_game_stats_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gameId` int NOT NULL,
  `category` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awayValue` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homeValue` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `gameTypeId` (`gameId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`team_seasons_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `seasonId` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `teamId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `triCode_index` (`triCode`),
  KEY `seasonId_index` (`seasonId`),
  KEY `teamId` (`teamId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`team_seasons_import_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teamId` int DEFAULT NULL,
  `seasonId` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `lastDateUpdated` datetime DEFAULT NULL,
  `gamesFound` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `seasonId_idx` (`seasonId`),
  KEY `teamId_idx` (`teamId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`teams_import` (
  `teamId` int NOT NULL,
  `franchiseId` int NOT NULL,
  `fullName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `leagueId` int NOT NULL,
  `triCode` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`teamId`),
  KEY `franchiseId_index` (`franchiseId`),
  KEY `triCode_index` (`triCode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `puckpandas_import`.`tv_broadcasts_import` (
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;