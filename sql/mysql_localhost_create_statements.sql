# create prod schema
create schema if not exists `puckpandas`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# create import schema
create schema if not exists `puckpandas_import`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# create import user
create user `puckpandas_import`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select, insert, update, delete on `puckpandas_import`.* to `puckpandas_import`@`localhost`;

# create prod transform user
create user `puckpandas_tx`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select, insert, update, delete on `puckpandas`.* to `puckpandas_tx`@`localhost`;
grant select on `puckpandas_import`.* to `puckpandas_tx`@`localhost`;

# create prod analysis user
create user `puckpandas`@`localhost` identified by "YOURPASSWORDGOESHERE";
grant select on `puckpandas`.* to `puckpandas`@`localhost`;

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
  KEY `gameIdeventId` (`gameId`, `eventId`),
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
  `faceoffWinningPctg` decimal(10,8) DEFAULT '0.00000000',
  `gameWinningGoals` int DEFAULT NULL,
  `otGoals` int DEFAULT NULL,
  `powerPlayGoals` int DEFAULT NULL,
  `powerPlayPoints` int DEFAULT NULL,
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
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


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

### COACHES ###
create table `puckpandas`.`coaches` (
	`coachId` int not null auto_increment,
    `coachName` varchar(255) not null,
    primary key (`coachId`),
    unique key `coachId` (`coachId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### LEAGUES ###
create table `puckpandas`.`leagues` (
	`leagueId` int not null auto_increment,
    `leagueAbbrev` varchar(25) not null,
    primary key (`leagueId`),
    unique key `leagueId` (`leagueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### LINESMEN ###
create table `puckpandas`.`linesmen` (
	`linesmanId` int not null auto_increment,
    `linesmanName` varchar(100),
    primary key (`linesmanId`),
    unique key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;


### PLAY TYPE CODES ###
create table `puckpandas`.`play_type_codes` (
	`typeCode` int not null,
    `typeDescKey` varchar(100),
    primary key (`typeCode`),
    unique key `typeCode` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;


### REFEREES ###
create table `puckpandas`.`referees` (
	`refereeId` int not null auto_increment,
    `refereeName` varchar(100),
    primary key (`refereeId`),
    unique key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;


### TEAM LOGOS ###
create table `puckpandas`.`team_logos` (
	`logoId` int not null auto_increment,
	teamLogo varchar(255),
    teamId	int not null,
    away tinyint not null,
    home tinyint not null,
    primary key (`logoId`),
    unique key `logoId` (`logoId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### TROPHIES ###
create table `puckpandas`.`trophies` (
	`trophyId` int not null auto_increment,
    `trophyName` varchar(100) not null,
    primary key (`trophyId`),
    unique key `trophyId` (`trophyId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;


### VENUES ###
create table `puckpandas`.`venues` (
	`venueId` int not null auto_increment,
    `venue` varchar(255) not null,
    primary key (`venueId`),
    unique key `venueId` (`venueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### TEAMS ###
create table `puckpandas`.`teams` (
	`teamId` int not null,
    `triCode` varchar(5) default null,
    `fullName` varchar(100) default null,
    `commonName` varchar(50) default null,
    `placeName` varchar(50) default null,
    primary key (`teamId`),
    unique key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAMES ###
create table `puckpandas`.`games` (
	`gameId` bigint not null,
    `seasonId` int not null,
    `gameType` int not null,
    `gameDate` date not null,
    `venueId` int default 0,
    `startTimeUTC` datetime not null,
    `startTimeVenue` datetime not null,
    `awayTeam` int not null,
    `homeTeam` int not null,
    primary key (`gameId`),
    unique key `gameId` (`gameId`),
    key `seasonId` (`seasonId`),
    key `gameDate` (`gameDate`),
    key `awayTeam` (`awayTeam`),
    key `homeTeam` (`homeTeam`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME COACHES ###
create table `puckpandas`.`game_coaches` (
	`gameCoachId` int not null auto_increment,
	`gameId` bigint not null,
	`teamId` int not null,
    `coachId` int not null,
    `home` tinyint not null,
    `away` tinyint not null,
    primary key (`gameCoachId`),
    unique key `gameCoachId` (`gameCoachId`),
    key `gameId` (`gameId`),
    key `teamId` (`teamId`),
    key `coachId` (`coachId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME LINESMEN ###
create table `puckpandas`.`game_linesmen` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `linesmanId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME REFEREES
create table `puckpandas`.`game_referees` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `refereeId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME RULES ###
create table `puckpandas`.`game_rules` (
	`gameId` int not null,
    `neutralSite` tinyInt default 0,
    `awayTeamSplitSquad` tinyInt default 0,
    `homeTeamSplitSquad` tinyInt default 0,
    `maxRegulationPeriods` int default 0,
    `maxPeriods` int default 0,
    `regPeriods` int default 3,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME SERIES ###
create table `puckpandas`.`game_series` (
    `gameId` int not null,
    `seriesLetter` varchar(3) default null,
    `neededToWin` int default 0,
    `topSeedWins` int default 0,
    `bottomSeedWins` int default 0,
    `gameNumberOfSeries` int default 0,
    `awayTeam` int not null,
    `awayTeamWins` int default 0,
    `homeTeam` int not null,
    `homeTeamWins` int default 0,
    key `gameId` (`gameId`),
    key `awayTeam` (`awayTeam`),
    key `homeTeam` (`homeTeam`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME SERIES GROUPS ###
create table `puckpandas`.`game_series_groups` (
	`gameId` int not null,
    `seriesNumber` int not null,
    `refGameId` int not null,
    key `gameId` (`gameId`),
    key `refGameId` (`refGameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME TV BROADCASTS ###
create table `puckpandas`.`game_tv_broadcasts` (
	`gameBroadcastId` int not null auto_increment,
    `gameId` int not null,
    `broadcastId` int not null,
    `sequenceNumber` int not null,
    `market` varchar(3) default null,
    `countryCode` varchar(5) default null,
    `network` varchar(12) default null,
    primary key (`gameBroadcastId`),
    unique key `gameBroadcastId` (`gameBroadcastId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME VIDEOS ###
create table `puckpandas`.`game_videos` (
	`gameId` int not null,
    `threeMinRecap` varchar(25) default null,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME PROGRESS ###
create table `puckpandas`.`game_progress` (
	`gameId` int not null,
    `gameState` varchar(8) default null,
    `gameScheduleState` varchar(8) default null,
    `periodNumber` int default 0,
    `periodType` varchar(8) default null,
    `secondsRemaining` int default 0,
    `clockRunning` tinyint default 0,
    `inIntermission` tinyint default 0,
    `maxPeriods` int default 0,
    `lastPeriodType` varchar(8) default null,
    `regPeriods` int default 0,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME SCORES ###
create table `puckpandas`.`game_scores` (
  `gameId` int not null,
  `periodType` varchar(8) default null,
  `gameOutcome` varchar(8) default null,
  `awayTeam` int not null,
  `awayScore` int default null,
  `awayLineScore` int default null,
  `awaySOG` int default null,
  `homeTeam` int not null,
  `homeScore` int default null,
  `homeLineScore` int default null,
  `homeSOG` int default null,
  primary key (`gameId`),
  unique key `gameId` (`gameId`),
  key `awayTeam` (`awayTeam`),
  key `homeTeam` (`homeTeam`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME TEAM STATS ###
create table `puckpandas`.`game_team_stats` (
	`gameId` int not null,
    `teamId` int not null,
    `sog` int default 0,
    `faceoffWinningPctg` decimal(10,8) default 0,
    `powerPlay` varchar(12) default null,
    `powerPlayPctg` decimal(10,8) default 0,
    `pim` int default 0,
    `hits` int default 0,
    `blockedShots` int default 0,
    `giveaways` int default 0,
    `takeaways` int default 0,
    key `gameId` (`gameId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME ROSTER SPOTS ###
create table `puckpandas`.`game_roster_spots` (
    `id` int not null auto_increment,
	`gameId` int not null,
    `teamId` int not null,
    `playerId` int not null,
    `sweaterNumber` int default null,
    `positionCode` varchar(3) default null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `teamId` (`teamId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME SCRATCHES ###
create table `puckpandas`.`game_scratches` (
	`id` int not null auto_increment,
    `gameId` int not null,
    `playerId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYS ###
create table `puckpandas`.`plays` (
	`playId` int not null auto_increment,
    `gameId` int not null,
	`eventId` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameIdeventId` (`gameId`, `eventId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME PLAYS ###
create table `puckpandas`.`game_plays` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
	`sortOrder` int not null,
	`teamId` int not null,
	`typeCode` int not null,
	`situationCode`  varchar(8) default null,
	`homeTeamDefendingSide` varchar (8) default null,
	`xCoord` int default null,
	`yCoord` int default null,
	`zoneCode` varchar(3) default null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`),
    key `teamId` (`teamId`),
    key `typeCode` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME PLAY TIMINGS ###
create table `puckpandas`.`game_play_timings` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `periodNumber` int default null,
    `periodType` varchar(8) default null,
    `maxRegulationPeriods` int default null,
    `secondsInPeriod` int default 0,
    `secondsRemaining` int default 0,
    `sortOrder` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME FACEOFFS ###
create table `puckpandas`.`game_faceoffs` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `losingPlayerId` int default null,
    `winningPlayerId` int default null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME GIVEAWAY TAKEAWAY ###
create table `puckpandas`.`game_giveaway_takeaway` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `playerId` int default null,
    `typeCode` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME GOALS ###
create table `puckpandas`.`game_goals` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `reason` varchar(25) default null,
    `shotType` varchar(25) default null,
    `goalieInNetId` int default null,
    `scoringPlayerId` int not null,
    `scoringPlayerTotal` int not null,
    `assist1PlayerId` int default null,
    `assist1PlayerTotal` int default null,
    `assist2PlayerId` int default null,
    `assist2PlayerTotal` int default null,
    `awayScore` int default null,
    `homeScore` int default null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME HITS ###
create table `puckpandas`.`game_hits` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `hittingPlayerId` int default null,
    `hitteePlayerId` int default null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME PENALTIES ###
create table `puckpandas`.`game_penalties` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `typeCode` int not null,
    `penaltyTypeCode` varchar(5) default null,
    `penaltyDescKey` varchar(50) default null,
    `penaltyDuration` int default null,
    `committedByPlayerId` int default null,
    `drawnByPlayerId` int default null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`),
    key `typeCode` (`typeCode`),
    key `penaltyTypeCode` (`penaltyTypeCode`),
    key `committedByPlayerId` (`committedByPlayerId`),
    key `drawnByPlayerId` (`drawnByPlayerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME SHOTS ###
create table `puckpandas`.`game_shots` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `typeCode` int not null,
    `reason` varchar(25) default null,
    `shotType` varchar(25) default null,
    `shootingPlayerId` int default null,
    `blockingPlayerId` int default null,
    `goalieInNetId` int default null,
    `awaySOG` int default 0,
    `homeSOG` int default 0,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME STOPPAGES ###
create table `puckpandas`.`game_stoppages` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `typeCode` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### SHIFTS ###
create table `puckpandas`.`shifts` (
	`id` int not null auto_increment,
    `gameId` int not null,
    `teamId` int not null,
    `eventNumber` int default null,
    `detailCode` int default null,
    `playerId` int not null,
    `shiftNumber` int default null,
    `period` int not null,
    `startTimeSeconds` int default 0,
    `endTimeSeconds` int default 0,
    `durationSeconds` int default 0,
    `typeCode` int default null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### SHIFT GOALS ###
create table `puckpandas`.`shift_goals` (
	`id` int not null auto_increment,
    `gameId` int not null,
    `eventNumber` int not null,
    `detailCode` int default null,
    `teamId` int not null,
    `playerId` int not null,
    `period` int not null,
    `goalTimeSeconds` int default 0,
    `eventDescription` varchar(255) default '',
    `eventDetails` varchar(50) default '',
    `typeCode` int not null,
	primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `teamId` (`teamId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYER BIOS ###
create table `puckpandas`.`player_bios` (
	`playerId` int not null,
    `firstName` varchar(50) default null,
    `lastName` varchar(50) default null,
    `birthDate` date default null,
    `birthCountry` varchar(50) default null,
    `birthState` varchar(50) default null,
    `birthCity` varchar(50) default null,
    `shootsCatches` varchar(5) default null,
    `heightInInches` int default null,
    `heightInCentimeters` int default null,
    `weightInPounds` int default null,
    `weightInKilograms` int default null,
    primary key (`playerId`),
    unique key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYER STATUSES ###
create table `puckpandas`.`player_statuses` (
	`playerId` int not null,
	`isActive` tinyint default 0,
    `currentTeamId` int default null,
    `currentTeamAbbrev` varchar(8) default null,
    `sweaterNumber` int default null,
    `position` varchar(5) default null,
    `inTop100AllTime` tinyint default 0,
    `inHHOF` tinyint default 0,
    primary key (`playerId`),
    unique key `playerId` (`playerId`),
    key `position` (`position`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYER AWARDS ###
create table `puckpandas`.`player_awards` (
	`id` int not null auto_increment,
	`playerId` int not null,
    `seasonId` int not null,
    `trophyId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `playerId` (`playerId`),
    key `seasonId` (`seasonId`),
    key `trophyId` (`trophyId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYER DRAFTS ###
create table `puckpandas`.`player_drafts` (
	`playerId` int not null,
    `draftYear` int default null,
    `teamId` int not null,
    `draftRound` int default null,
    `pickInRound` int default null,
    `overallPick` int default null,
	primary key (`playerId`),
    unique key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### PLAYER HEADSHOTS ###
create table `puckpandas`.`player_headshots` (
	`headshotId` int not null auto_increment,
    `playerId` int not null,
    `headshot` varchar(100) default null,
	primary key (`headshotId`),
    unique key `headshotId` (`headshotId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GOALIE CAREER TOTALS ###
create table `puckpandas`.`goalie_career_totals` (
	`playerId` int not null,
    `gameType` int not null,
    `GP` int not null,
    `G` int not null,
    `A` int not null,
    `PIM` int not null,
    `GS` int not null,
    `PTS` int not null,
    `W` int not null,
    `L` int not null,
    `OTL` int not null,
    `SA` int not null,
    `GA` int not null,
    `GAA` decimal(10,8) not null,
    `SPCT` decimal(10,8) not null,
    `SO` int not null,
    `TOISEC` int not null,
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GOALIE SEASONS ###
create table `puckpandas`.`goalie_seasons` (
	`id` int not null auto_increment,
	`playerId` int not null,
    `seasonId` int default null,
    `leagueAbbrev` varchar(12) default null,
    `teamName` varchar(50) default null,
    `teamId` int default null,
    `sequence` int not null,
    `gameType` int default null,
    `GP` int default null,
    `GS` int default null,
    `G` int default null,
    `A` int default null,
    `PIM` int default null,
    `W` int default null,
    `L` int default null,
    `OTL` int default null,
    `ties` int default null,
    `SA` int default null,
    `GA` int default null,
    `GAA` decimal(11,8) not null,
    `SPCT` decimal(10,8) not null,
    `SO` int default null,
    `TOISEC` int default null,
    primary key (`id`),
    unique key `id` (`id`),
    key `playerId` (`playerId`),
    key `seasonId` (`seasonId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### SKATER CAREER TOTALS ###
create table `puckpandas`.`skater_career_totals` (
	`playerId` int not null,
    `gameType` int not null,
    `GP` int not null,
    `G` int not null,
    `A` int not null,
    `P` int not null,
    `PM` int not null,
    `PIM` int not null,
    `PPG` int not null,
    `PPP` int not null,
    `SHG` int not null,
    `SHP` int not null,
    `TOIGSEC` int not null,
    `GWG` int not null,
    `OTG` int not null,
    `S` int not null,
    `SPCT` decimal(10,8) default 0.0,
    `FOPCT` decimal(10,8) default 0.0,
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### SKATER SEASONS ###
create table `puckpandas`.`skater_seasons` (
	`id` int not null auto_increment,
	`playerId` int not null,
    `seasonId` int default null,
    `leagueId` int default null,
    `teamName` varchar(50) default null,
    `teamId` int default null,
    `sequence` int not null,
    `gameType` int default null,
    `GP` int not null,
    `G` int not null,
    `A` int not null,
    `P` int not null,
    `PM` int not null,
    `PIM` int not null,
    `PPG` int not null,
    `PPP` int not null,
    `SHG` int not null,
    `SHP` int not null,
    `TOIGSEC` int not null,
    `GWG` int not null,
    `OTG` int not null,
    `S` int not null,
    `SPCT` decimal(10,8) default 0.0,
    `FOPCT` decimal(10,8) default 0.0,
    primary key (`id`),
    unique key `id` (`id`),
    key `playerId` (`playerId`),
    key `seasonId` (`seasonId`),
    key `leagueId` (`leagueId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### TEAM ROSTERS ###
create table `puckpandas`.`team_rosters` (
	`id` int not null auto_increment,
    `teamId` int not null,
    `seasonId` int not null,
    `playerId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `teamId` (`teamId`),
    key `seasonId` (`seasonId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### TEAMS SEASONS ###
create table `puckpandas`.`team_seasons` (
	`id` int not null auto_increment,
    `teamId` int not null,
    `seasonId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `teamId` (`teamId`),
    key `seasonId` (`seasonId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


### GAME RESULTS ###
create table `game_results` (
    `resultId` varchar(22) character set utf8mb4 collate utf8mb4_0900_ai_ci not null default '',
    `gameId` bigint not null,
    `teamId` int not null,
    `seasonId` int not null,
    `teamWin` int not null default '0',
    `awayGame` int not null default '0',
    `homeGame` int not null default '0',
    `awayWin` int not null default '0',
    `homeWin` int not null default '0',
    `tie` int not null default '0',
    `overtime` int not null default '0',
    `awayScore` int default null,
    `homeScore` int default null,
    `standingPoints` int not null default '0',
    unique key `resultId` (`resultId`),
    key `teamId` (`teamId`),
    key `seasonId` (`seasonId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;