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


# create game_progress
# create game_scores
# create game_team_stats

# create game_roster_spots
# create game_scratches

# create game_plays
# create game_play_timings
# create game_faceoffs
# create game_giveaway_takeaway
# create game_goals
# create game_hits
# create game_penalties
# create game_shots
# create game_stoppages

# create shifts
# create shifts_goals


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
