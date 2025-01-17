### COACHES ### 
create table puckpandas.coaches (
	`coachId` int not null auto_increment,
    `coachName` varchar(255) not null,
    primary key (`coachId`),
    unique key `coachId` (`coachId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into puckpandas.coaches (coachName)
select distinct a.coachName
  from (select `gameInfo.awayTeam.headCoach.default` as coachName
          from puckpandas_import.game_center_right_rail_import
         union 
        select `gameInfo.homeTeam.headCoach.default` as coach
          from puckpandas_import.game_center_right_rail_import) as a
 where a.coachName != '0.0'
 order by coachName;


### LEAGUES ###
create table puckpandas.leagues (
	`leagueId` int not null auto_increment,
    `leagueAbbrev` varchar(25) not null,
    primary key (`leagueId`),
    unique key `leagueId` (`leagueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into puckpandas.leagues (leagueAbbrev)
select distinct leagueAbbrev
  from puckpandas_import.skater_season_import
 order by leagueAbbrev;


### LINESMEN ###
create table puckpandas.linesmen (
	`linesmanId` int not null auto_increment,
    `linesmanName` varchar(100),
    primary key (`linesmanId`),
    unique key `linesmanId` (`linesmanId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

insert into puckpandas.linesmen (linesmanName)
select distinct `default` as linesmanName
  from puckpandas_import.linesmen_import;


### PLAY TYPE CODES ###
create table puckpandas.playTypeCodes (
	`typeCode` int not null,
    `typeDescKey` varchar(100),
    primary key (`typeCode`),
    unique key `typeCode` (`typeCode`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

insert into puckpandas.playTypeCodes (typeCode, typeDescKey)
select distinct typeCode, typeDescKey
  from puckpandas_import.plays_import
 order by typeCode;


### REFEREES ###
create table puckpandas.referees (
	`refereeId` int not null auto_increment,
    `refereeName` varchar(100),
    primary key (`refereeId`),
    unique key `refereeId` (`refereeId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

insert into puckpandas.referees (refereeName)
select distinct `default` as refereeName
  from puckpandas_import.referees_import;


### TEAM LOGOS ###
create table puckpandas.team_logos (
	`logoId` int not null auto_increment,
	teamLogo varchar(255),
    teamId	int not null,
    away tinyint not null,
    home tinyint not null,
    primary key (`logoId`),
    unique key `logoId` (`logoId`),
    key `teamId` (`teamId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into puckpandas.team_logos (teamLogo, teamId, away, home)
select distinct `awayTeam.logo` as teamLogo, `awayTeam.id` as teamId, 1 as away, 0 as home
  from puckpandas_import.game_center_import
 where `awayTeam.logo` != '0.0'
 union 
select distinct `homeTeam.logo` as teamLogo, `homeTeam.id` as teamId, 0 as away, 1 as home
  from puckpandas_import.game_center_import
 where `homeTeam.logo` != '0.0';


### TROPHIES ###
create table puckpandas.trophies (
	`trophyId` int not null auto_increment,
    `trophyName` varchar(100) not null,
    primary key (`trophyId`),
    unique key `trophyId` (`trophyId`)
) engine=MyISAM default charset=utf8mb4 collate utf8mb4_unicode_ci;

insert into puckpandas.trophies (trophyName)
select distinct `trophy.default` as trophyName
  from puckpandas_import.player_award_import;


### VENUES ### 
create table puckpandas.venues (
	`venueId` int not null auto_increment,
    `venue` varchar(255) not null,
    primary key (`venueId`),
    unique key `venueId` (`venueId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into puckpandas.venues (venue)
select distinct venue as venueName
  from puckpandas_import.games_import
 order by venue;


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

insert into `puckpandas`.`teams` (teamId, triCode, fullName, commonName, placeName)
select distinct `awayTeam.id` as teamId, `awayTeam.abbrev` as triCode, 
       concat(`awayTeam.placeName.default`, ' ', `awayTeam.commonName.default`) as fullName, 
       `awayTeam.commonName.default` as commonName, `awayTeam.placeName.default` as placeName
  from puckpandas_import.game_center_import
 union 
select `homeTeam.id` as teamId, `homeTeam.abbrev` as triCode, concat(`homeTeam.placeName.default`, ' ', `homeTeam.commonName.default`) as fullName, `homeTeam.commonName.default` as commonName, `homeTeam.placeName.default` as placeName
  from puckpandas_import.game_center_import;


### GAMES ###
create table puckpandas.games (
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

insert into games (gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, startTimeVenue, awayTeam, homeTeam)
select a.gameId, a.seasonId, a.gameType, a.gameDate, b.venueId, a.startTimeUTC, date_add(a.startTimeUTC, INTERVAL
       time_to_sec(left(a.venueUTCOffset, locate(':', a.venueUTCOffset)+2)) second) as startTimeVenue, 
       a.awayTeam, a.homeTeam
  from puckpandas_import.games_import as a
  join puckpandas.venues as b on a.venue = b.venue;


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

insert into game_coaches (gameId, teamId, coachId, home, away)
select a.gameId, a.awayTeam as teamId, c.coachId, 1 as away, 0 as home
  from puckpandas_import.games_import as a
  join puckpandas_import.game_center_right_rail_import as b on a.gameId = b.gameId
  join coaches as c on b.`gameInfo.awayTeam.headCoach.default` = c.coachName
 union
select a.gameId, a.homeTeam as teamId, c.coachId, 0 as away, 1 as home
  from puckpandas_import.games_import as a
  join puckpandas_import.game_center_right_rail_import as b on a.gameId = b.gameId
  join coaches as c on b.`gameInfo.homeTeam.headCoach.default` = c.coachName;


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

insert into `puckpandas`.`game_linesmen` (gameId, linesmanId)
select a.gameId, b.linesmanId
  from puckpandas_import.linesmen_import as a
  join puckpandas.linesmen as b on a.`default` = b.linesmanName;


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

insert into `puckpandas`.`game_referees` (gameId, refereeId)
select a.gameId, b.refereeId
  from puckpandas_import.referees_import as a
  join puckpandas.referees as b on a.`default` = b.refereeName;


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

insert into `puckpandas`.`game_rules` (gameId, neutralSite, awayTeamSplitSquad, homeTeamSplitSquad, maxRegulationPeriods, maxPeriods, regPeriods)
select a.gameId, a.neutralSite, a.awayTeamSplitSquad, a.homeTeamSplitSquad, b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, 
       b.maxPeriods, b.regPeriods
  from puckpandas_import.games_import as a
  join puckpandas_import.game_center_import as b on a.gameId = b.gameId;


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

insert into `puckpandas`.`game_series` (gameId, seriesLetter, neededToWin, topSeedWins, bottomSeedWins, gameNumberOfSeries, awayTeam, awayTeamWins, homeTeam, homeTeamWins)
select a.gameId, case when a.`seriesStatus.seriesLetter` = '0' then '' else a.`seriesStatus.seriesLetter` end as seriesLetter, 
       a.`seriesStatus.neededToWin` as neededToWin, a.`seriesStatus.topSeedWins` as topSeedWins,
       a.`seriesStatus.bottomSeedWins` as bottomSeedWins, a.`seriesStatus.gameNumberOfSeries` as gameNumberOfSeries, 
       a.awayTeam, b.`seasonSeriesWins.awayTeamWins` as awayTeamWins,
       a.homeTeam, b.`seasonSeriesWins.homeTeamWins` as homeTeamWins
  from `puckpandas_import`.`games_import` as a
  join `puckpandas_import`.`game_center_right_rail_import` as b on a.gameId = b.gameId
 order by gameId;


### GAME SERIES GROUPS ###
create table `puckpandas`.`game_series_groups` (
	`gameId` int not null,
    `seriesNumber` int not null,
    `refGameId` int not null,
    key `gameId` (`gameId`),
    key `refGameId` (`refGameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into `puckpandas`.`game_series_groups` (gameId, seriesNumber, refGameId)
select a.gameId, a.seriesNumber, a.refGameId
  from puckpandas_import.season_series_import as a;


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

insert into `puckpandas`.`game_tv_broadcasts` (gameId, broadcastId, sequenceNumber, market, countryCode, network)
select gameId, broadcastId, sequenceNumber, market, countryCode, network
  from puckpandas_import.tv_broadcasts_import
 order by gameId, sequenceNumber;


### GAME VIDEOS ###
create table `puckpandas`.`game_videos` (
	`gameId` int not null,
    `threeMinRecap` varchar(25) default null,
    primary key (`gameId`),
    unique key `gameId` (`gameId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into `puckpandas`.`game_videos` (gameId, threeMinRecap)
select gameId, case when `gameVideo.threeMinRecap` = '0' then '' else `gameVideo.threeMinRecap` end as threeMinRecap
  from `puckpandas_import`.`game_center_right_rail_import`;


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

insert into `puckpandas`.`game_progress` (gameId, gameState, gameScheduleState, periodNumber, periodType, secondsRemaining, clockRunning, inIntermission, maxPeriods, lastPeriodType, regPeriods)
select a.gameId, a.gameState, a.gameScheduleState, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
       b.`clock.secondsRemaining` as secondsRemaining, b.`clock.running` as clockRunning, b.`clock.inIntermission` as inIntermission, b.maxPeriods,
       b.`gameOutcome.lastPeriodType` as lastPeriodType, b.regPeriods
  from `puckpandas_import`.`games_import` as a
  join `puckpandas_import`.`game_center_import` as b on a.gameId = b.gameId;
 

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

insert into `puckpandas`.`game_scores` (gameId, periodType, gameOutcome, awayTeam, awayScore, awayLineScore, awaySOG, homeTeam, homeScore, homeLineScore, homeSOG)
select a.gameId, a.periodType, a.gameOutcome, a.awayTeam, a.awayTeamScore as awayScore, c.`linescore.totals.away` as awayLineScore, b.`awayTeam.sog` as awaySOG,
       a.homeTeam, a.homeTeamScore as homeScore, c.`linescore.totals.home` as homeLineScore, b.`homeTeam.sog` as homeSOG 
  from `puckpandas_import`.`games_import` as a
  join `puckpandas_import`.`game_center_import` as b on a.gameId = b.gameId
  join `puckpandas_import`.`game_center_right_rail_import` as c on a.gameId = c.gameId;


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

insert into `puckpandas`.`game_team_stats` (gameId, teamId, sog, faceoffWinningPctg, powerPlay, powerPlayPctg, pim, hits, blockedShots, giveaways, takeaways)
select a.gameId, b.awayTeam as teamId, 
       sum(case when a.category = 'sog' then a.awayValue else '' end) as sog,
       sum(case when a.category = 'faceoffWinningPctg' then a.awayValue else '' end) as faceoffWinningPctg,
       e.awayValue as powerPlay,
       sum(case when a.category = 'powerPlayPctg' then a.awayValue else '' end) as powerPlayPctg,
       sum(case when a.category = 'pim' then a.awayValue else '' end) as pim,
       sum(case when a.category = 'hits' then a.awayValue else '' end) as hits,
       sum(case when a.category = 'blockedShots' then a.awayValue else '' end) as blockedShots,
       sum(case when a.category = 'giveaways' then a.awayValue else '' end) as giveaways,
       sum(case when a.category = 'takeaways' then a.awayValue else '' end) as takeaways
  from `puckpandas_import`.`team_game_stats_import` as a
  join `puckpandas_import`.`games_import` as b on a.gameId = b.gameId
  join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue
          from `puckpandas_import`.`team_game_stats_import` as c 
          join `puckpandas_import`.`games_import` as d on c.gameId = d.gameId
		 where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.awayTeam = e.awayTeam
 group by a.gameId, b.awayTeam
 union 
select a.gameId, b.homeTeam as teamId, 
       sum(case when a.category = 'sog' then a.homeValue else '' end) as sog,
       sum(case when a.category = 'faceoffWinningPctg' then a.homeValue else '' end) as faceoffWinningPctg,
       e.homeValue as powerPlay,
       sum(case when a.category = 'powerPlayPctg' then a.homeValue else '' end) as powerPlayPctg,
       sum(case when a.category = 'pim' then a.homeValue else '' end) as pim,
       sum(case when a.category = 'hits' then a.homeValue else '' end) as hits,
       sum(case when a.category = 'blockedShots' then a.homeValue else '' end) as blockedShots,
       sum(case when a.category = 'giveaways' then a.homeValue else '' end) as givehomes,
       sum(case when a.category = 'takeaways' then a.homeValue else '' end) as takehomes
  from `puckpandas_import`.`team_game_stats_import` as a
  join `puckpandas_import`.`games_import` as b on a.gameId = b.gameId
  join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue
          from `puckpandas_import`.`team_game_stats_import` as c 
          join `puckpandas_import`.`games_import` as d on c.gameId = d.gameId
		 where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.homeTeam = e.homeTeam
 group by a.gameId, b.homeTeam;


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

insert into `puckpandas`.`game_roster_spots` (gameId, teamId, playerId, sweaterNumber, positionCode)
select gameId, teamId, playerId, sweaterNumber, positionCode
  from `puckpandas_import`.`roster_spots_import`;


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

insert into `puckpandas`.`game_scratches` (gameId, playerId)
select gameId, playerId
  from `puckpandas_import`.`scratches_import`;

### PLAYS ###
create table `puckpandas`.`plays` (
	`playId` int not null auto_increment,
    `gameId` int not null, 
	`eventId` int not null,
    primary key (`playId`),
    unique key `playId` (`playId`),
    key `gameIdeventId` (`gameId`, `eventId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into `puckpandas`.`plays` (gameId, eventId)
select gameId, eventId
  from `puckpandas_import`.`plays_import`;


### GAME PLAYS ###
create table `puckpandas`.`game_plays` (
	`playId` int not null,
    `gameId` int not null, 
	`eventId` int not null, 
	`sortOrder` int not null, 
	`teamId` int not null, 
	`typeCode` int not null, 
	`situationCode`  int default 0, 
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

insert into `puckpandas`.`game_plays` (playId, gameId, eventId, sortOrder, teamId, typeCode, situationCode, homeTeamDefendingSide, xCoord, yCoord, zoneCode)
select b.playId, a.gameId, a.eventId, a.sortOrder, a.`details.eventOwnerTeamId` as teamId, a.typeCode, a.situationCode, a.homeTeamDefendingSide, 
       a.`details.xCoord` as xCoord, a.`details.yCoord` as yCoord, a.`details.zoneCode` as zoneCode 
  from `puckpandas_import`.`plays_import` as a
  join `puckpandas`.`plays` as b on a.gameId = b.gameId and a.eventId = b.eventId;


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

insert into `puckpandas`.`game_play_timings` (playId, gameId, eventId, periodNumber, periodType, maxRegulationPeriods, secondsInPeriod, secondsRemaining, sortOrder)
select a.playId, b.gameId, b.eventId, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
       time_to_sec(left(b.timeInPeriod, locate(':', b.timeInPeriod)+2))/60 as secondsInPeriod, 
       time_to_sec(left(b.timeRemaining, locate(':', b.timeRemaining)+2))/60 as secondsRemaining,
       b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, b.sortOrder
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId;


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

insert into `puckpandas`.`game_faceoffs` (playId, gameId, eventId, losingPlayerId, winningPlayerId)
select a.playId, b.gameId, b.eventId, b.`details.losingPlayerId` as losingPlayerId, b.`details.winningPlayerId` as winningPlayerId
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode = '502';


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

insert into `puckpandas`.`game_giveaway_takeaway` (playId, gameId, eventId, sortOrder, playerId, typeCode)
select a.playId, b.gameId, b.eventId, b.sortOrder, 
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('504', '525');


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

insert into `puckpandas`.`game_goals` (playId, gameId, eventId, sortOrder, reason, shotType, goalieInNetId, scoringPlayerId, scoringPlayerTotal, assist1PlayerId, 
                                       assist1PlayerTotal, assist2PlayerId, assist2PlayerTotal, awayScore, homeScore)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.reason` as reason, b.`details.shotType` as shotType,
       b.`details.goalieInNetId` as goalieInNetId, b.`details.scoringPlayerId` as scoringPlayerId, b.`details.scoringPlayerTotal` as scoringPlayerTotal, 
       b.`details.assist1PlayerId` as assist1PlayerId, b.`details.assist1PlayerTotal` as assist1PlayerTotal, b.`details.assist2PlayerId` as assist2PlayerId, 
       b.`details.assist2PlayerTotal` as assist2PlayerTotal, b.`details.awayScore` as awayScore, b.`details.homeScore` as homeScore
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode = '505';


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

insert into `puckpandas`.`game_hits` (playId, gameId, eventId, sortOrder, hittingPlayerId, hitteePlayerId)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.hittingPlayerId` as hittingPlayerId, b.`details.hitteePlayerId` as hitteePlayerId 
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode = '503';


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

insert into `puckpandas`.`game_penalties` (playId, gameId, eventId, sortOrder, typeCode, penaltyTypeCode, penaltyDescKey, penaltyDuration, committedByPlayerId, drawnByPlayerId)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.typeCode` as penaltyTypeCode, b.`details.descKey` as penaltyDescKey, 
       b.`details.duration` as duration, b.`details.committedByPlayerId` as committedByPlayerId, b.`details.drawnByPlayerId` as drawnByPlayerId
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('509', '535');

 
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

insert into `puckpandas`.`game_shots` (playId, gameId, eventId, sortOrder, typeCode, reason, shotType, shootingPlayerId, blockingPlayerId, goalieInNetId, awaySOG, homeSOG)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.reason` as reason, b.`details.shotType` as shotType, b.`details.shootingPlayerId` as shootingPlayerId, 
       b.`details.blockingPlayerId` as blockingPlayerId, b.`details.goalieInNetId` as goalieInNetId, b.`details.awaySOG` as awaySOG, b.`details.homeSOG` as homeSOG
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('506', '507', '538', '537');


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

insert into `puckpandas`.`game_stoppages` (playId, gameId, eventId, sortOrder, typeCode)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('516', '520', '521', '523', '524')
 order by playId;


# create shifts
create table `puckpandas`.`shifts` (
	`shiftId` int not null auto_increment,
    `gameId` int not null,
    `playerId` int not null,
    `shiftNumber` int default null,
    `period` int not null,
    `startTimeSeconds` int default 0,
    `durationSeconds` int default 0,
    `detailCode` int default null,
    `eventNumber` int default null,
    `typeCode` int default null,
    primary key (`shiftId`),
    unique key `shiftId` (`shiftId`),
    key `gameId` (`gameId`),
    key `playerId` (`playerId`)
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into `puckpandas`.`shifts` (shiftId, detailCode, duration, eventNumber, gameId, period, playerId, shiftNumber, startTime, typeCode)
select gameId, eventNumber, detailCode, period, playerId, shiftNumber, startTime, duration, typeCode
  from `puckpandas_import`.`shifts_import`;

# create shifts_goals
create table `puckpandas`.`shift_goals` (
) engine=MyISAM default charset=utf8mb4 collate=utf8mb4_unicode_ci;

insert into `puckpandas`.`shift_goals` ()
where typeCode = 505

# create player_bios

# create player_statuses
# create player_awards
# create player_drafts
# create player_headshots

# create goalie_career_totals
# create goalie_seasons
# create skater_career_totals
# create skater_seasons

# create team_rosters
# create team_seasons
