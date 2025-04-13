### create schemas ###

# import
create schema `puckpandas_import`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# prod
create schema `puckpandas`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# analysis
create schema `puckpandas_ana`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# test import
create schema `puckpandas_imp_test`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;

# test prod
create schema `puckpandas_test`
  default character set = utf8mb4
  default collate = utf8mb4_unicode_ci;


### create users ###

# import
create user `puckpandas_import`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas_import`.* to `puckpandas_import`@`"YOURDBHOSTNAMEGOESHERE"`;

# import transform
create user `puckpandas_tx`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas`.* to `puckpandas_tx`@`"YOURDBHOSTNAMEGOESHERE"`;
grant select on `puckpandas_import`.* to `puckpandas_tx`@`"YOURDBHOSTNAMEGOESHERE"`;

# prod
create user `puckpandas`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select insert, update, delete on `puckpandas`.* to `puckpandas`@`"YOURDBHOSTNAMEGOESHERE"`;

# analysis
create user `puckpandas_ana`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas_ana`.* to `puckpandas_ana`@`"YOURDBHOSTNAMEGOESHERE"`;
grant select on `puckpandas`.* to `puckpandas_ana`@`"YOURDBHOSTNAMEGOESHERE"`;

# import test
create user `puckpandas_imp_test`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas_imp_test`.* to `puckpandas_imp_test`@`"YOURDBHOSTNAMEGOESHERE"`;

# import transform test
create user `puckpandas_tx_test`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas_test`.* to `puckpandas_tx_test`@`"YOURDBHOSTNAMEGOESHERE"`;
grant select on `puckpandas_imp_test`.* to `puckpandas_tx_test`@`"YOURDBHOSTNAMEGOESHERE"`;

# prod test
create user `puckpandas_test`@`"YOURDBHOSTNAMEGOESHERE"` identified by `"YOURPASSWORDGOESHERE"`;
grant select, insert, update, delete on `puckpandas_test`.* to `puckpandas_test`@`"YOURDBHOSTNAMEGOESHERE"`;


### create tables ###

# import tables
create table `puckpandas_import`.`game_center_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `season` varchar(8) collate utf8mb4_unicode_ci default null,
  `gameType` int default null,
  `limitedScoring` tinyint default null,
  `gameDate` date default null,
  `venue.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `venueLocation.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `startTimeUTC` datetime default null,
  `easternUTCOffset` varchar(10) collate utf8mb4_unicode_ci default null,
  `venueUTCOffset` varchar(10) collate utf8mb4_unicode_ci default null,
  `gameState` varchar(5) collate utf8mb4_unicode_ci default null,
  `gameScheduleState` varchar(5) collate utf8mb4_unicode_ci default null,
  `periodDescriptor.number` int default null,
  `periodDescriptor.periodType` varchar(5) collate utf8mb4_unicode_ci default null,
  `periodDescriptor.maxRegulationPeriods` int default null,
  `awayTeam.id` int default null,
  `awayTeam.commonName.default` varchar(20) collate utf8mb4_unicode_ci default null,
  `awayTeam.abbrev` varchar(5) collate utf8mb4_unicode_ci default null,
  `awayTeam.score` int default null,
  `awayTeam.sog` int default null,
  `awayTeam.logo` varchar(100) collate utf8mb4_unicode_ci default null,
  `awayTeam.placeName.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `awayTeam.placeNameWithPreposition.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `homeTeam.id` int default null,
  `homeTeam.commonName.default` varchar(20) collate utf8mb4_unicode_ci default null,
  `homeTeam.abbrev` varchar(5) collate utf8mb4_unicode_ci default null,
  `homeTeam.score` int default null,
  `homeTeam.sog` int default null,
  `homeTeam.logo` varchar(100) collate utf8mb4_unicode_ci default null,
  `homeTeam.placeName.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `homeTeam.placeNameWithPreposition.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `shootoutInUse` tinyint default null,
  `otInUse` tinyint default null,
  `clock.timeRemaining` varchar(10) collate utf8mb4_unicode_ci default null,
  `clock.secondsRemaining` int default null,
  `clock.running` tinyint default null,
  `clock.inIntermission` tinyint default null,
  `displayPeriod` int default null,
  `maxPeriods` int default null,
  `gameOutcome.lastPeriodType` varchar(5) collate utf8mb4_unicode_ci default null,
  `regPeriods` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`),
  key `season` (`season`),
  key `gameType` (`gameType`),
  key `gameDate` (`gameDate`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`game_center_right_rail_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seasonSeriesWins.awayTeamWins` int default null,
  `seasonSeriesWins.homeTeamWins` int default null,
  `seasonSeriesWins.neededToWin` int default null,
  `gameInfo.awayTeam.headCoach.default` varchar(250) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameInfo.homeTeam.headCoach.default` varchar(250) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameVideo.threeMinRecap` bigint default null,
  `linescore.totals.away` int default null,
  `linescore.totals.home` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`games_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameType` int not null,
  `gameDate` date default null,
  `venue` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `neutralSite` tinyint default null,
  `startTimeUTC` datetime default null,
  `venueUTCOffset` time default '00:00:00',
  `venueTimezone` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameState` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameScheduleState` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `awayTeam` int not null,
  `awayTeamSplitSquad` tinyint default null,
  `awayTeamScore` int default null,
  `homeTeam` int not null,
  `homeTeamSplitSquad` tinyint default null,
  `homeTeamScore` int default null,
  `periodType` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameOutcome` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `seriesStatus.round` int default null,
  `seriesStatus.seriesAbbrev` varchar(8) collate utf8mb4_unicode_ci default null,
  `seriesStatus.seriesTitle` varchar(25) collate utf8mb4_unicode_ci default null,
  `seriesStatus.seriesLetter` varchar(3) collate utf8mb4_unicode_ci default null,
  `seriesStatus.neededToWin` int default null,
  `seriesStatus.topSeedWins` int default null,
  `seriesStatus.bottomSeedWins` int default null,
  `seriesStatus.gameNumberOfSeries` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `seasonId_index` (`seasonId`),
  key `gameDate_index` (`gameDate`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`games_import_log` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `lastDateUpdated` datetime default null,
  `gameFound` tinyint default null,
  `gameCenterFound` tinyint default null,
  `tvBroadcastsFound` tinyint default null,
  `playsFound` tinyint default null,
  `rosterSpotsFound` tinyint default null,
  `teamGameStatsFound` tinyint default null,
  `seasonSeriesFound` tinyint default null,
  `refereesFound` tinyint default null,
  `linesmenFound` tinyint default null,
  `scratchesFound` tinyint default null,
  `shiftsFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  unique key `gameId_unique` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`goalie_career_totals_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `regularSeason.gamesPlayed` int default '0',
  `regularSeason.goals` int default '0',
  `regularSeason.assists` int default '0',
  `regularSeason.pim` int default '0',
  `regularSeason.gamesStarted` int default '0',
  `regularSeason.points` int default '0',
  `regularSeason.wins` int default '0',
  `regularSeason.losses` int default '0',
  `regularSeason.otLosses` int default '0',
  `regularSeason.shotsAgainst` int default '0',
  `regularSeason.goalsAgainst` int default '0',
  `regularSeason.goalsAgainstAvg` decimal(10,8) default '0.00000000',
  `regularSeason.savePctg` decimal(10,8) default '0.00000000',
  `regularSeason.shutouts` int default '0',
  `regularSeason.timeOnIce` time default '00:00:00',
  `regularSeason.timeOnIceMinutes` int default '0',
  `regularSeason.timeOnIceSeconds` int default null,
  `playoffs.gamesPlayed` int default '0',
  `playoffs.goals` int default '0',
  `playoffs.assists` int default '0',
  `playoffs.pim` int default '0',
  `playoffs.gamesStarted` int default '0',
  `playoffs.points` int default '0',
  `playoffs.wins` int default '0',
  `playoffs.losses` int default '0',
  `playoffs.otLosses` int default '0',
  `playoffs.shotsAgainst` int default '0',
  `playoffs.goalsAgainst` int default '0',
  `playoffs.goalsAgainstAvg` decimal(10,8) default '0.00000000',
  `playoffs.savePctg` decimal(10,8) default '0.00000000',
  `playoffs.shutouts` int default '0',
  `playoffs.timeOnIce` time default '00:00:00',
  `playoffs.timeOnIceMinutes` int default '0',
  `playoffs.timeOnIceSeconds` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`goalie_season_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `gameTypeId` int default null,
  `gamesPlayed` int default null,
  `goalsAgainst` int default null,
  `goalsAgainstAvg` decimal(11,8) default '0.00000000',
  `leagueAbbrev` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `losses` int default null,
  `season` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci not null,
  `sequence` int default null,
  `shutouts` int default null,
  `ties` int default null,
  `timeOnIce` time default '00:00:00',
  `timeOnIceMinutes` int default '0',
  `timeOnIceSeconds` int default null,
  `wins` int default null,
  `teamName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `savePctg` decimal(10,8) default '0.00000000',
  `shotsAgainst` int default null,
  `otLosses` int default null,
  `assists` int default null,
  `gamesStarted` int default null,
  `goals` int default null,
  `pim` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`linesmen_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `default` varchar(100) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`player_award_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `trophy.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`player_bios_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `isActive` tinyint default null,
  `currentTeamId` int default null,
  `currentTeamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sweaterNumber` int default null,
  `position` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `heightInInches` int default null,
  `heightInCentimeters` int default null,
  `weightInPounds` int default null,
  `weightInKilograms` int default null,
  `birthDate` date default null,
  `birthCountry` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `shootsCatches` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `inTop100AllTime` tinyint default null,
  `inHHOF` tinyint default null,
  `firstName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `lastName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `birthCity.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `birthStateProvince.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `draftDetails.year` int default null,
  `draftDetails.teamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `draftDetails.round` int default null,
  `draftDetails.pickInRound` int default null,
  `draftDetails.overallPick` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`),
  key `teamId_index` (`currentTeamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`player_import_log` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `lastDateUpdated` datetime default null,
  `playerFound` tinyint default null,
  `careerTotalsFound` tinyint default null,
  `seasonTotalsFound` tinyint default null,
  `awardsFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  unique key `playerId_unique` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`plays_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `eventId` int not null,
  `periodDescriptor.number` int default null,
  `periodDescriptor.periodType` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `periodDescriptor.maxRegulationPeriods` int default null,
  `timeInPeriod` time default '00:00:00',
  `timeRemaining` time default '00:00:00',
  `situationCode` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `homeTeamDefendingSide` varchar(10) collate utf8mb4_unicode_ci default null,
  `typeCode` int default null,
  `typeDescKey` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sortOrder` int default null,
  `details.eventOwnerTeamId` int default null,
  `details.losingPlayerId` int default null,
  `details.winningPlayerId` int default null,
  `details.xCoord` int default null,
  `details.yCoord` int default null,
  `details.zoneCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.reason` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.hittingPlayerId` int default null,
  `details.hitteePlayerId` int default null,
  `details.shotType` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.shootingPlayerId` int default null,
  `details.goalieInNetId` int default null,
  `details.awaySOG` int default null,
  `details.homeSOG` int default null,
  `details.playerId` int default null,
  `details.blockingPlayerId` int default null,
  `details.secondaryReason` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.typeCode` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.descKey` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.duration` int default null,
  `details.committedByPlayerId` int default null,
  `details.drawnByPlayerId` int default null,
  `details.scoringPlayerId` int default null,
  `details.scoringPlayerTotal` int default null,
  `details.assist1PlayerId` int default null,
  `details.assist1PlayerTotal` int default null,
  `details.assist2PlayerId` int default null,
  `details.assist2PlayerTotal` int default null,
  `details.awayScore` int default null,
  `details.homeScore` int default null,
  primary key (`id`),
  key `gameIdeventId` (`gameId`, `eventId`),
  key `typeCode_index` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`referees_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `default` varchar(100) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`roster_spots_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `teamId` int not null,
  `playerId` int not null,
  `sweaterNumber` int default null,
  `positionCode` varchar(5) collate utf8mb4_unicode_ci default null,
  `headshot` varchar(100) collate utf8mb4_unicode_ci default null,
  `firstName` varchar(75) collate utf8mb4_unicode_ci default null,
  `lastName` varchar(75) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `teamId` (`teamId`),
  key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`rosters_import` (
  `id` int not null auto_increment,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `playerId` int not null,
  primary key (`id`),
  key `triCode_index` (`triCode`),
  key `seasonId` (`seasonId`),
  key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`scratches_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `playerId` int not null,
  `firstName.default` varchar(75) collate utf8mb4_unicode_ci default '',
  `lastName.default` varchar(75) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`season_series_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seriesNumber` int not null,
  `refGameId` int not null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`shifts_import` (
  `id` int not null,
  `detailCode` int default null,
  `duration` time default null,
  `endTime` time default null,
  `eventDescription` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `eventDetails` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `eventNumber` int default null,
  `firstName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameId` int default null,
  `hexValue` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `lastName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `period` int default null,
  `playerId` int default null,
  `shiftNumber` int default null,
  `startTime` time default null,
  `teamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `teamId` int default null,
  `teamName` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `typeCode` int default null,
  primary key (`id`),
  key `gameId_index` (`gameId`),
  key `playerId_index` (`playerId`),
  key `teamId_index` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`skater_career_totals_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `regularSeason.gamesPlayed` int default null,
  `regularSeason.goals` int default null,
  `regularSeason.assists` int default null,
  `regularSeason.pim` int default null,
  `regularSeason.points` int default null,
  `regularSeason.plusMinus` int default null,
  `regularSeason.powerPlayGoals` int default null,
  `regularSeason.powerPlayPoints` int default null,
  `regularSeason.shorthandedPoints` int default null,
  `regularSeason.gameWinningGoals` int default null,
  `regularSeason.otGoals` int default null,
  `regularSeason.shots` int default null,
  `regularSeason.shootingPctg` decimal(10,8) default '0.00000000',
  `regularSeason.faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `regularSeason.avgToi` time default '00:00:00',
  `regularSeason.shorthandedGoals` int default null,
  `playoffs.gamesPlayed` int default null,
  `playoffs.goals` int default null,
  `playoffs.assists` int default null,
  `playoffs.pim` int default null,
  `playoffs.points` int default null,
  `playoffs.plusMinus` int default null,
  `playoffs.powerPlayGoals` int default null,
  `playoffs.powerPlayPoints` int default null,
  `playoffs.shorthandedPoints` int default null,
  `playoffs.gameWinningGoals` int default null,
  `playoffs.otGoals` int default null,
  `playoffs.shots` int default null,
  `playoffs.shootingPctg` decimal(10,8) default '0.00000000',
  `playoffs.faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `playoffs.avgToi` time default '00:00:00',
  `playoffs.shorthandedGoals` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`skater_season_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `assists` int default null,
  `gameTypeId` int default null,
  `gamesPlayed` int default null,
  `goals` int default null,
  `leagueAbbrev` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `pim` int default '0',
  `points` int default null,
  `season` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sequence` int default null,
  `teamName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `plusMinus` int default null,
  `avgToi` varchar(12) collate utf8mb4_unicode_ci default null,
  `faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `gameWinningGoals` int default null,
  `otGoals` int default null,
  `powerPlayGoals` int default null,
  `powerPlayPoints` int default null,
  `shootingPctg` decimal(10,8) default null,
  `shorthandedGoals` int default null,
  `shorthandedPoints` int default null,
  `shots` int default null,
  `teamCommonName.default` varchar(45) collate utf8mb4_unicode_ci default null,
  `teamPlaceNameWithPreposition.default` varchar(45) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `playerId` (`playerId`),
  key `gameTypeId` (`gameTypeId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`table_update_log` (
  `id` int not null auto_increment,
  `tableName` varchar(100) collate utf8mb4_unicode_ci default null,
  `lastDateUpdated` datetime default null,
  `updateFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `tableName` (`tableName`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`team_game_stats_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `category` varchar(20) collate utf8mb4_unicode_ci default null,
  `awayValue` varchar(20) collate utf8mb4_unicode_ci default null,
  `homeValue` varchar(20) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`team_seasons_import` (
  `id` int not null auto_increment,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `teamId` int default null,
  primary key (`id`),
  key `triCode_index` (`triCode`),
  key `seasonId_index` (`seasonId`),
  key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`team_seasons_import_log` (
  `id` int not null auto_increment,
  `teamId` int default null,
  `seasonId` varchar(8) collate utf8mb4_unicode_ci default '',
  `lastDateUpdated` datetime default null,
  `gamesFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `seasonId_idx` (`seasonId`),
  key `teamId_idx` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`teams_import` (
  `teamId` int not null,
  `franchiseId` int not null,
  `fullName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `leagueId` int not null,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  primary key (`teamId`),
  key `franchiseId_index` (`franchiseId`),
  key `triCode_index` (`triCode`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_import`.`tv_broadcasts_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `broadcastId` int not null,
  `market` varchar(10) collate utf8mb4_unicode_ci default null,
  `countryCode` varchar(5) collate utf8mb4_unicode_ci default null,
  `network` varchar(5) collate utf8mb4_unicode_ci default null,
  `sequenceNumber` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `broadcastId` (`broadcastId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


# prod tables
create table `puckpandas`.`coaches` (
	`coachId` int not null auto_increment,
    `coachName` varchar(255) not null,
    primary key (`coachId`),
    unique key `coachId` (`coachId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`leagues` (
	`leagueId` int not null auto_increment,
    `leagueAbbrev` varchar(25) not null,
    primary key (`leagueId`),
    unique key `leagueId` (`leagueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`linesmen` (
	`linesmanId` int not null auto_increment,
    `linesmanName` varchar(100),
    primary key (`linesmanId`),
    unique key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas`.`play_type_codes` (
	`typeCode` int not null,
    `typeDescKey` varchar(100),
    primary key (`typeCode`),
    unique key `typeCode` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas`.`referees` (
	`refereeId` int not null auto_increment,
    `refereeName` varchar(100),
    primary key (`refereeId`),
    unique key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

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

create table `puckpandas`.`trophies` (
	`trophyId` int not null auto_increment,
    `trophyName` varchar(100) not null,
    primary key (`trophyId`),
    unique key `trophyId` (`trophyId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas`.`venues` (
	`venueId` int not null auto_increment,
    `venue` varchar(255) not null,
    primary key (`venueId`),
    unique key `venueId` (`venueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`teams` (
	`teamId` int not null,
    `triCode` varchar(5) default null,
    `fullName` varchar(100) default null,
    `commonName` varchar(50) default null,
    `placeName` varchar(50) default null,
    primary key (`teamId`),
    unique key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`game_linesmen` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `linesmanId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`game_referees` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `refereeId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`game_series_groups` (
	`gameId` int not null,
    `seriesNumber` int not null,
    `refGameId` int not null,
    key `gameId` (`gameId`),
    key `refGameId` (`refGameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`game_videos` (
	`gameId` int not null,
    `threeMinRecap` varchar(25) default null,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`game_scratches` (
	`id` int not null auto_increment,
    `gameId` int not null,
    `playerId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`plays` (
	`playId` int not null auto_increment,
    `gameId` int not null,
	`eventId` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameIdeventId` (`gameId`, `eventId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`player_headshots` (
	`headshotId` int not null auto_increment,
    `playerId` int not null,
    `headshot` varchar(100) default null,
	primary key (`headshotId`),
    unique key `headshotId` (`headshotId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

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

create table `puckpandas`.`team_seasons` (
	`id` int not null auto_increment,
    `teamId` int not null,
    `seasonId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `teamId` (`teamId`),
    key `seasonId` (`seasonId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas`.`game_results` (
  `resultId` varchar(22) NOT NULL DEFAULT '',
  `gameId` bigint NOT NULL DEFAULT '0',
  `gameType` int NOT NULL,
  `teamId` int NOT NULL DEFAULT '0',
  `seasonId` int NOT NULL DEFAULT '0',
  `teamWin` int NOT NULL DEFAULT '0',
  `teamOT` int NOT NULL DEFAULT '0',
  `teamLoss` int NOT NULL DEFAULT '0',
  `awayGame` bigint NOT NULL DEFAULT '0',
  `awayWin` int NOT NULL DEFAULT '0',
  `awayOT` int NOT NULL DEFAULT '0',
  `awayLoss` int NOT NULL DEFAULT '0',
  `homeGame` bigint NOT NULL DEFAULT '0',
  `homeWin` int NOT NULL DEFAULT '0',
  `homeOT` int NOT NULL DEFAULT '0',
  `homeLoss` int NOT NULL DEFAULT '0',
  `tie` bigint NOT NULL DEFAULT '0',
  `overtime` bigint NOT NULL DEFAULT '0',
  `awayScore` int DEFAULT NULL,
  `homeScore` int DEFAULT NULL,
  `standingPoints` bigint NOT NULL DEFAULT '0',
  UNIQUE KEY `resultId` (`resultId`),
  KEY `gameId` (`gameId`),
  KEY `teamId` (`teamId`),
  KEY `seasonId` (`seasonId`)
) engine=myisam default charset=utf8mb4 collate=utf8mb4_unicode_ci;

# import test tables
create table `puckpandas_imp_test`.`game_center_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `season` varchar(8) collate utf8mb4_unicode_ci default null,
  `gameType` int default null,
  `limitedScoring` tinyint default null,
  `gameDate` date default null,
  `venue.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `venueLocation.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `startTimeUTC` datetime default null,
  `easternUTCOffset` varchar(10) collate utf8mb4_unicode_ci default null,
  `venueUTCOffset` varchar(10) collate utf8mb4_unicode_ci default null,
  `gameState` varchar(5) collate utf8mb4_unicode_ci default null,
  `gameScheduleState` varchar(5) collate utf8mb4_unicode_ci default null,
  `periodDescriptor.number` int default null,
  `periodDescriptor.periodType` varchar(5) collate utf8mb4_unicode_ci default null,
  `periodDescriptor.maxRegulationPeriods` int default null,
  `awayTeam.id` int default null,
  `awayTeam.commonName.default` varchar(20) collate utf8mb4_unicode_ci default null,
  `awayTeam.abbrev` varchar(5) collate utf8mb4_unicode_ci default null,
  `awayTeam.score` int default null,
  `awayTeam.sog` int default null,
  `awayTeam.logo` varchar(100) collate utf8mb4_unicode_ci default null,
  `awayTeam.placeName.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `awayTeam.placeNameWithPreposition.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `homeTeam.id` int default null,
  `homeTeam.commonName.default` varchar(20) collate utf8mb4_unicode_ci default null,
  `homeTeam.abbrev` varchar(5) collate utf8mb4_unicode_ci default null,
  `homeTeam.score` int default null,
  `homeTeam.sog` int default null,
  `homeTeam.logo` varchar(100) collate utf8mb4_unicode_ci default null,
  `homeTeam.placeName.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `homeTeam.placeNameWithPreposition.default` varchar(50) collate utf8mb4_unicode_ci default null,
  `shootoutInUse` tinyint default null,
  `otInUse` tinyint default null,
  `clock.timeRemaining` varchar(10) collate utf8mb4_unicode_ci default null,
  `clock.secondsRemaining` int default null,
  `clock.running` tinyint default null,
  `clock.inIntermission` tinyint default null,
  `displayPeriod` int default null,
  `maxPeriods` int default null,
  `gameOutcome.lastPeriodType` varchar(5) collate utf8mb4_unicode_ci default null,
  `regPeriods` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`),
  key `season` (`season`),
  key `gameType` (`gameType`),
  key `gameDate` (`gameDate`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`game_center_right_rail_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seasonSeriesWins.awayTeamWins` int default null,
  `seasonSeriesWins.homeTeamWins` int default null,
  `seasonSeriesWins.neededToWin` int default null,
  `gameInfo.awayTeam.headCoach.default` varchar(250) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameInfo.homeTeam.headCoach.default` varchar(250) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameVideo.threeMinRecap` bigint default null,
  `linescore.totals.away` int default null,
  `linescore.totals.home` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`games_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameType` int not null,
  `gameDate` date default null,
  `venue` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `neutralSite` tinyint default null,
  `startTimeUTC` datetime default null,
  `venueUTCOffset` time default '00:00:00',
  `venueTimezone` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameState` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameScheduleState` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `awayTeam` int not null,
  `awayTeamSplitSquad` tinyint default null,
  `awayTeamScore` int default null,
  `homeTeam` int not null,
  `homeTeamSplitSquad` tinyint default null,
  `homeTeamScore` int default null,
  `periodType` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameOutcome` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `seriesStatus.round` int default null,
  `seriesStatus.seriesAbbrev` varchar(8) collate utf8mb4_unicode_ci default null,
  `seriesStatus.seriesTitle` varchar(25) collate utf8mb4_unicode_ci default null,
  `seriesStatus.seriesLetter` varchar(3) collate utf8mb4_unicode_ci default null,
  `seriesStatus.neededToWin` int default null,
  `seriesStatus.topSeedWins` int default null,
  `seriesStatus.bottomSeedWins` int default null,
  `seriesStatus.gameNumberOfSeries` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `seasonId_index` (`seasonId`),
  key `gameDate_index` (`gameDate`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`games_import_log` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `lastDateUpdated` datetime default null,
  `gameFound` tinyint default null,
  `gameCenterFound` tinyint default null,
  `tvBroadcastsFound` tinyint default null,
  `playsFound` tinyint default null,
  `rosterSpotsFound` tinyint default null,
  `teamGameStatsFound` tinyint default null,
  `seasonSeriesFound` tinyint default null,
  `refereesFound` tinyint default null,
  `linesmenFound` tinyint default null,
  `scratchesFound` tinyint default null,
  `shiftsFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  unique key `gameId_unique` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`goalie_career_totals_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `regularSeason.gamesPlayed` int default '0',
  `regularSeason.goals` int default '0',
  `regularSeason.assists` int default '0',
  `regularSeason.pim` int default '0',
  `regularSeason.gamesStarted` int default '0',
  `regularSeason.points` int default '0',
  `regularSeason.wins` int default '0',
  `regularSeason.losses` int default '0',
  `regularSeason.otLosses` int default '0',
  `regularSeason.shotsAgainst` int default '0',
  `regularSeason.goalsAgainst` int default '0',
  `regularSeason.goalsAgainstAvg` decimal(10,8) default '0.00000000',
  `regularSeason.savePctg` decimal(10,8) default '0.00000000',
  `regularSeason.shutouts` int default '0',
  `regularSeason.timeOnIce` time default '00:00:00',
  `regularSeason.timeOnIceMinutes` int default '0',
  `regularSeason.timeOnIceSeconds` int default null,
  `playoffs.gamesPlayed` int default '0',
  `playoffs.goals` int default '0',
  `playoffs.assists` int default '0',
  `playoffs.pim` int default '0',
  `playoffs.gamesStarted` int default '0',
  `playoffs.points` int default '0',
  `playoffs.wins` int default '0',
  `playoffs.losses` int default '0',
  `playoffs.otLosses` int default '0',
  `playoffs.shotsAgainst` int default '0',
  `playoffs.goalsAgainst` int default '0',
  `playoffs.goalsAgainstAvg` decimal(10,8) default '0.00000000',
  `playoffs.savePctg` decimal(10,8) default '0.00000000',
  `playoffs.shutouts` int default '0',
  `playoffs.timeOnIce` time default '00:00:00',
  `playoffs.timeOnIceMinutes` int default '0',
  `playoffs.timeOnIceSeconds` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`goalie_season_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `gameTypeId` int default null,
  `gamesPlayed` int default null,
  `goalsAgainst` int default null,
  `goalsAgainstAvg` decimal(11,8) default '0.00000000',
  `leagueAbbrev` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `losses` int default null,
  `season` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci not null,
  `sequence` int default null,
  `shutouts` int default null,
  `ties` int default null,
  `timeOnIce` time default '00:00:00',
  `timeOnIceMinutes` int default '0',
  `timeOnIceSeconds` int default null,
  `wins` int default null,
  `teamName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `savePctg` decimal(10,8) default '0.00000000',
  `shotsAgainst` int default null,
  `otLosses` int default null,
  `assists` int default null,
  `gamesStarted` int default null,
  `goals` int default null,
  `pim` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`linesmen_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `default` varchar(100) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`player_award_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `trophy.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`player_bios_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `isActive` tinyint default null,
  `currentTeamId` int default null,
  `currentTeamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sweaterNumber` int default null,
  `position` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `heightInInches` int default null,
  `heightInCentimeters` int default null,
  `weightInPounds` int default null,
  `weightInKilograms` int default null,
  `birthDate` date default null,
  `birthCountry` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `shootsCatches` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `inTop100AllTime` tinyint default null,
  `inHHOF` tinyint default null,
  `firstName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `lastName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `birthCity.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `birthStateProvince.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `draftDetails.year` int default null,
  `draftDetails.teamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `draftDetails.round` int default null,
  `draftDetails.pickInRound` int default null,
  `draftDetails.overallPick` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`),
  key `teamId_index` (`currentTeamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`player_import_log` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `lastDateUpdated` datetime default null,
  `playerFound` tinyint default null,
  `careerTotalsFound` tinyint default null,
  `seasonTotalsFound` tinyint default null,
  `awardsFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  unique key `playerId_unique` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`plays_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `eventId` int not null,
  `periodDescriptor.number` int default null,
  `periodDescriptor.periodType` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `periodDescriptor.maxRegulationPeriods` int default null,
  `timeInPeriod` time default '00:00:00',
  `timeRemaining` time default '00:00:00',
  `situationCode` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `homeTeamDefendingSide` varchar(10) collate utf8mb4_unicode_ci default null,
  `typeCode` int default null,
  `typeDescKey` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sortOrder` int default null,
  `details.eventOwnerTeamId` int default null,
  `details.losingPlayerId` int default null,
  `details.winningPlayerId` int default null,
  `details.xCoord` int default null,
  `details.yCoord` int default null,
  `details.zoneCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.reason` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.hittingPlayerId` int default null,
  `details.hitteePlayerId` int default null,
  `details.shotType` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.shootingPlayerId` int default null,
  `details.goalieInNetId` int default null,
  `details.awaySOG` int default null,
  `details.homeSOG` int default null,
  `details.playerId` int default null,
  `details.blockingPlayerId` int default null,
  `details.secondaryReason` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.typeCode` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.descKey` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `details.duration` int default null,
  `details.committedByPlayerId` int default null,
  `details.drawnByPlayerId` int default null,
  `details.scoringPlayerId` int default null,
  `details.scoringPlayerTotal` int default null,
  `details.assist1PlayerId` int default null,
  `details.assist1PlayerTotal` int default null,
  `details.assist2PlayerId` int default null,
  `details.assist2PlayerTotal` int default null,
  `details.awayScore` int default null,
  `details.homeScore` int default null,
  primary key (`id`),
  key `gameIdeventId` (`gameId`, `eventId`),
  key `typeCode_index` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`referees_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `default` varchar(100) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`roster_spots_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `teamId` int not null,
  `playerId` int not null,
  `sweaterNumber` int default null,
  `positionCode` varchar(5) collate utf8mb4_unicode_ci default null,
  `headshot` varchar(100) collate utf8mb4_unicode_ci default null,
  `firstName` varchar(75) collate utf8mb4_unicode_ci default null,
  `lastName` varchar(75) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `teamId` (`teamId`),
  key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`rosters_import` (
  `id` int not null auto_increment,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `playerId` int not null,
  primary key (`id`),
  key `triCode_index` (`triCode`),
  key `seasonId` (`seasonId`),
  key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`scratches_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `playerId` int not null,
  `firstName.default` varchar(75) collate utf8mb4_unicode_ci default '',
  `lastName.default` varchar(75) collate utf8mb4_unicode_ci default '',
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`season_series_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `seriesNumber` int not null,
  `refGameId` int not null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`shifts_import` (
  `id` int not null,
  `detailCode` int default null,
  `duration` time default null,
  `endTime` time default null,
  `eventDescription` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `eventDetails` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `eventNumber` int default null,
  `firstName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `gameId` int default null,
  `hexValue` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `lastName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `period` int default null,
  `playerId` int default null,
  `shiftNumber` int default null,
  `startTime` time default null,
  `teamAbbrev` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `teamId` int default null,
  `teamName` varchar(25) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `typeCode` int default null,
  primary key (`id`),
  key `gameId_index` (`gameId`),
  key `playerId_index` (`playerId`),
  key `teamId_index` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`skater_career_totals_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `regularSeason.gamesPlayed` int default null,
  `regularSeason.goals` int default null,
  `regularSeason.assists` int default null,
  `regularSeason.pim` int default null,
  `regularSeason.points` int default null,
  `regularSeason.plusMinus` int default null,
  `regularSeason.powerPlayGoals` int default null,
  `regularSeason.powerPlayPoints` int default null,
  `regularSeason.shorthandedPoints` int default null,
  `regularSeason.gameWinningGoals` int default null,
  `regularSeason.otGoals` int default null,
  `regularSeason.shots` int default null,
  `regularSeason.shootingPctg` decimal(10,8) default '0.00000000',
  `regularSeason.faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `regularSeason.avgToi` time default '00:00:00',
  `regularSeason.shorthandedGoals` int default null,
  `playoffs.gamesPlayed` int default null,
  `playoffs.goals` int default null,
  `playoffs.assists` int default null,
  `playoffs.pim` int default null,
  `playoffs.points` int default null,
  `playoffs.plusMinus` int default null,
  `playoffs.powerPlayGoals` int default null,
  `playoffs.powerPlayPoints` int default null,
  `playoffs.shorthandedPoints` int default null,
  `playoffs.gameWinningGoals` int default null,
  `playoffs.otGoals` int default null,
  `playoffs.shots` int default null,
  `playoffs.shootingPctg` decimal(10,8) default '0.00000000',
  `playoffs.faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `playoffs.avgToi` time default '00:00:00',
  `playoffs.shorthandedGoals` int default null,
  primary key (`id`),
  key `playerId_index` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`skater_season_import` (
  `id` int not null auto_increment,
  `playerId` int not null,
  `assists` int default null,
  `gameTypeId` int default null,
  `gamesPlayed` int default null,
  `goals` int default null,
  `leagueAbbrev` varchar(12) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `pim` int default '0',
  `points` int default null,
  `season` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `sequence` int default null,
  `teamName.default` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `plusMinus` int default null,
  `avgToi` varchar(12) collate utf8mb4_unicode_ci default null,
  `faceoffWinningPctg` decimal(10,8) default '0.00000000',
  `gameWinningGoals` int default null,
  `otGoals` int default null,
  `powerPlayGoals` int default null,
  `powerPlayPoints` int default null,
  `shootingPctg` decimal(10,8) default null,
  `shorthandedGoals` int default null,
  `shorthandedPoints` int default null,
  `shots` int default null,
  `teamCommonName.default` varchar(45) collate utf8mb4_unicode_ci default null,
  `teamPlaceNameWithPreposition.default` varchar(45) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `playerId` (`playerId`),
  key `gameTypeId` (`gameTypeId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`table_update_log` (
  `id` int not null auto_increment,
  `tableName` varchar(100) collate utf8mb4_unicode_ci default null,
  `lastDateUpdated` datetime default null,
  `updateFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `tableName` (`tableName`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`team_game_stats_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `category` varchar(20) collate utf8mb4_unicode_ci default null,
  `awayValue` varchar(20) collate utf8mb4_unicode_ci default null,
  `homeValue` varchar(20) collate utf8mb4_unicode_ci default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameTypeId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`team_seasons_import` (
  `id` int not null auto_increment,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci not null,
  `seasonId` varchar(8) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `teamId` int default null,
  primary key (`id`),
  key `triCode_index` (`triCode`),
  key `seasonId_index` (`seasonId`),
  key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`team_seasons_import_log` (
  `id` int not null auto_increment,
  `teamId` int default null,
  `seasonId` varchar(8) collate utf8mb4_unicode_ci default '',
  `lastDateUpdated` datetime default null,
  `gamesFound` tinyint default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `seasonId_idx` (`seasonId`),
  key `teamId_idx` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`teams_import` (
  `teamId` int not null,
  `franchiseId` int not null,
  `fullName` varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  `leagueId` int not null,
  `triCode` varchar(3) character set utf8mb4 collate utf8mb4_unicode_ci default null,
  primary key (`teamId`),
  key `franchiseId_index` (`franchiseId`),
  key `triCode_index` (`triCode`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_imp_test`.`tv_broadcasts_import` (
  `id` int not null auto_increment,
  `gameId` int not null,
  `broadcastId` int not null,
  `market` varchar(10) collate utf8mb4_unicode_ci default null,
  `countryCode` varchar(5) collate utf8mb4_unicode_ci default null,
  `network` varchar(5) collate utf8mb4_unicode_ci default null,
  `sequenceNumber` int default null,
  primary key (`id`),
  unique key `id` (`id`),
  key `gameId` (`gameId`),
  key `broadcastId` (`broadcastId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;


# prod test tables
create table `puckpandas_test`.`coaches` (
	`coachId` int not null auto_increment,
    `coachName` varchar(255) not null,
    primary key (`coachId`),
    unique key `coachId` (`coachId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`leagues` (
	`leagueId` int not null auto_increment,
    `leagueAbbrev` varchar(25) not null,
    primary key (`leagueId`),
    unique key `leagueId` (`leagueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`linesmen` (
	`linesmanId` int not null auto_increment,
    `linesmanName` varchar(100),
    primary key (`linesmanId`),
    unique key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas_test`.`play_type_codes` (
	`typeCode` int not null,
    `typeDescKey` varchar(100),
    primary key (`typeCode`),
    unique key `typeCode` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas_test`.`referees` (
	`refereeId` int not null auto_increment,
    `refereeName` varchar(100),
    primary key (`refereeId`),
    unique key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas_test`.`team_logos` (
	`logoId` int not null auto_increment,
	teamLogo varchar(255),
    teamId	int not null,
    away tinyint not null,
    home tinyint not null,
    primary key (`logoId`),
    unique key `logoId` (`logoId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`trophies` (
	`trophyId` int not null auto_increment,
    `trophyName` varchar(100) not null,
    primary key (`trophyId`),
    unique key `trophyId` (`trophyId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

create table `puckpandas_test`.`venues` (
	`venueId` int not null auto_increment,
    `venue` varchar(255) not null,
    primary key (`venueId`),
    unique key `venueId` (`venueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`teams` (
	`teamId` int not null,
    `triCode` varchar(5) default null,
    `fullName` varchar(100) default null,
    `commonName` varchar(50) default null,
    `placeName` varchar(50) default null,
    primary key (`teamId`),
    unique key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`games` (
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

create table `puckpandas_test`.`game_coaches` (
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

create table `puckpandas_test`.`game_linesmen` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `linesmanId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_referees` (
	`id` int not null auto_increment,
	`gameId` bigint not null,
    `refereeId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_rules` (
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

create table `puckpandas_test`.`game_series` (
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

create table `puckpandas_test`.`game_series_groups` (
	`gameId` int not null,
    `seriesNumber` int not null,
    `refGameId` int not null,
    key `gameId` (`gameId`),
    key `refGameId` (`refGameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_tv_broadcasts` (
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

create table `puckpandas_test`.`game_videos` (
	`gameId` int not null,
    `threeMinRecap` varchar(25) default null,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_progress` (
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

create table `puckpandas_test`.`game_scores` (
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

create table `puckpandas_test`.`game_team_stats` (
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

create table `puckpandas_test`.`game_roster_spots` (
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

create table `puckpandas_test`.`game_scratches` (
	`id` int not null auto_increment,
    `gameId` int not null,
    `playerId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `gameId` (`gameId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`plays` (
	`playId` int not null auto_increment,
    `gameId` int not null,
	`eventId` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameIdeventId` (`gameId`, `eventId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_plays` (
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

create table `puckpandas_test`.`game_play_timings` (
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

create table `puckpandas_test`.`game_faceoffs` (
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

create table `puckpandas_test`.`game_giveaway_takeaway` (
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

create table `puckpandas_test`.`game_goals` (
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

create table `puckpandas_test`.`game_hits` (
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

create table `puckpandas_test`.`game_penalties` (
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

create table `puckpandas_test`.`game_shots` (
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

create table `puckpandas_test`.`game_stoppages` (
	`playId` int not null,
    `gameId` int not null,
	`eventId` int not null,
    `sortOrder` int not null,
    `typeCode` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`shifts` (
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

create table `puckpandas_test`.`shift_goals` (
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

create table `puckpandas_test`.`player_bios` (
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

create table `puckpandas_test`.`player_statuses` (
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

create table `puckpandas_test`.`player_awards` (
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

create table `puckpandas_test`.`player_drafts` (
	`playerId` int not null,
    `draftYear` int default null,
    `teamId` int not null,
    `draftRound` int default null,
    `pickInRound` int default null,
    `overallPick` int default null,
	primary key (`playerId`),
    unique key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`player_headshots` (
	`headshotId` int not null auto_increment,
    `playerId` int not null,
    `headshot` varchar(100) default null,
	primary key (`headshotId`),
    unique key `headshotId` (`headshotId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`goalie_career_totals` (
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

create table `puckpandas_test`.`goalie_seasons` (
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

create table `puckpandas_test`.`skater_career_totals` (
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

create table `puckpandas_test`.`skater_seasons` (
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

create table `puckpandas_test`.`team_rosters` (
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

create table `puckpandas_test`.`team_seasons` (
	`id` int not null auto_increment,
    `teamId` int not null,
    `seasonId` int not null,
    primary key (`id`),
    unique key `id` (`id`),
    key `teamId` (`teamId`),
    key `seasonId` (`seasonId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

create table `puckpandas_test`.`game_results` (
  `resultId` varchar(22) not null,
  `gameId` bigint not null,
  `teamId` int not null,
  `seasonId` int not null,
  `teamWin` int not null default '0',
  `teamOT` int not null default '0',
  `teamLoss` int not null default '0',
  `awayGame` bigint not null default '0',
  `awayWin` int not null default '0',
  `awayOT` int not null default '0',
  `awayLoss` int not null default '0',
  `homeGame` bigint not null default '0',
  `homeWin` int not null default '0',
  `homeOT` int not null default '0',
  `homeLoss` int not null default '0',
  `tie` bigint not null default '0',
  `overtime` bigint not null default '0',
  `awayScore` int default null,
  `homeScore` int default null,
  `standingPoints` bigint not null default '0',
  unique key `resultId` (`resultId`),
  key `gameid` (`gameId`),
  key `teamid` (`teamId`),
  key `seasonId` (`seasonId`)
) engine=myisam default charset=utf8mb4 collate=utf8mb4_unicode_ci;
