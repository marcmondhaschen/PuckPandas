### COACHES ### 
truncate table `puckpandas`.`coaches`;
insert into `puckpandas`.`coaches` (coachName)
select distinct a.coachName
  from (select `gameInfo.awayTeam.headCoach.default` as coachName
          from puckpandas_import.game_center_right_rail_import
         union
        select `gameInfo.homeTeam.headCoach.default` as coach
          from puckpandas_import.game_center_right_rail_import) as a
 where a.coachName != '0.0'
 order by coachName;


### LEAGUES ###
truncate table `puckpandas`.`leagues`;
insert into `puckpandas`.`leagues` (leagueAbbrev)
select distinct leagueAbbrev
  from puckpandas_import.skater_season_import
 order by leagueAbbrev;


### LINESMEN ###
truncate table `puckpandas`.`linesmen`;
insert into `puckpandas`.`linesmen` (linesmanName)
select distinct `default` as linesmanName
  from puckpandas_import.linesmen_import;


### PLAY TYPE CODES ###
truncate table `puckpandas`.`play_type_codes`;
insert into `puckpandas`.`play_type_codes` (typeCode, typeDescKey)
select distinct typeCode, typeDescKey
  from puckpandas_import.plays_import
 order by typeCode;


### REFEREES ###
truncate table `puckpandas`.`referees`;
insert into `puckpandas`.`referees` (refereeName)
select distinct `default` as refereeName
  from puckpandas_import.referees_import;


### TEAM LOGOS ###
truncate table `puckpandas`.`team_logos`;
insert into `puckpandas`.`team_logos` (teamLogo, teamId, away, home)
select distinct `awayTeam.logo` as teamLogo, `awayTeam.id` as teamId, 1 as away, 0 as home
  from puckpandas_import.game_center_import
 where `awayTeam.logo` != '0.0'
 union 
select distinct `homeTeam.logo` as teamLogo, `homeTeam.id` as teamId, 0 as away, 1 as home
  from puckpandas_import.game_center_import
 where `homeTeam.logo` != '0.0';


### TROPHIES ###
truncate table `puckpandas`.`trophies`;
insert into `puckpandas`.`trophies` (trophyName)
select distinct `trophy.default` as trophyName
  from puckpandas_import.player_award_import;


### VENUES ### 
truncate table `puckpandas`.`venues`;
insert into `puckpandas`.`venues` (venue)
select distinct venue as venueName
  from puckpandas_import.games_import
 order by venue;


### TEAMS ###
truncate table `puckpandas`.`teams`;
insert into `puckpandas`.`teams` (teamId, triCode, fullName, commonName, placeName)
select distinct `awayTeam.id` as teamId, `awayTeam.abbrev` as triCode, 
       concat(`awayTeam.placeName.default`, ' ', `awayTeam.commonName.default`) as fullName, 
       `awayTeam.commonName.default` as commonName, `awayTeam.placeName.default` as placeName
  from puckpandas_import.game_center_import
 union
select `homeTeam.id` as teamId, `homeTeam.abbrev` as triCode,
       concat(`homeTeam.placeName.default`, ' ', `homeTeam.commonName.default`) as fullName,
       `homeTeam.commonName.default` as commonName, `homeTeam.placeName.default` as placeName
  from puckpandas_import.game_center_import;


### GAMES ###
truncate table `puckpandas`.`games`;
insert into `puckpandas`.`games` (gameId, seasonId, gameType, gameDate, venueId, startTimeUTC, startTimeVenue, awayTeam, homeTeam)
select a.gameId, a.seasonId, a.gameType, a.gameDate, b.venueId, a.startTimeUTC, date_add(a.startTimeUTC, INTERVAL
       time_to_sec(left(a.venueUTCOffset, locate(':', a.venueUTCOffset)+2)) second) as startTimeVenue, 
       a.awayTeam, a.homeTeam
  from puckpandas_import.games_import as a
  join puckpandas.venues as b on a.venue = b.venue;


### GAME COACHES ###
truncate table `puckpandas`.`game_coaches`;
insert into `puckpandas`.`game_coaches` (gameId, teamId, coachId, home, away)
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
truncate table `puckpandas`.`game_linesmen`;
insert into `puckpandas`.`game_linesmen` (gameId, linesmanId)
select a.gameId, b.linesmanId
  from puckpandas_import.linesmen_import as a
  join puckpandas.linesmen as b on a.`default` = b.linesmanName;


### GAME REFEREES
truncate table `puckpandas`.`game_referees`;
insert into `puckpandas`.`game_referees` (gameId, refereeId)
select a.gameId, b.refereeId
  from puckpandas_import.referees_import as a
  join puckpandas.referees as b on a.`default` = b.refereeName;


### GAME RULES ###
truncate table `puckpandas`.`game_rules`;
insert into `puckpandas`.`game_rules` (gameId, neutralSite, awayTeamSplitSquad, homeTeamSplitSquad, maxRegulationPeriods, maxPeriods, regPeriods)
select a.gameId, a.neutralSite, a.awayTeamSplitSquad, a.homeTeamSplitSquad, b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, 
       b.maxPeriods, b.regPeriods
  from puckpandas_import.games_import as a
  join puckpandas_import.game_center_import as b on a.gameId = b.gameId;


### GAME SERIES ### 
truncate table `puckpandas`.`game_series`;
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
truncate table `puckpandas`.`game_series_groups`;
insert into `puckpandas`.`game_series_groups` (gameId, seriesNumber, refGameId)
select a.gameId, a.seriesNumber, a.refGameId
  from puckpandas_import.season_series_import as a;


### GAME TV BROADCASTS ###
truncate table `puckpandas`.`game_tv_broadcasts`;
insert into `puckpandas`.`game_tv_broadcasts` (gameId, broadcastId, sequenceNumber, market, countryCode, network)
select gameId, broadcastId, sequenceNumber, market, countryCode, network
  from puckpandas_import.tv_broadcasts_import
 order by gameId, sequenceNumber;


### GAME VIDEOS ###
truncate table `puckpandas`.`game_videos`;
insert into `puckpandas`.`game_videos` (gameId, threeMinRecap)
select gameId, case when `gameVideo.threeMinRecap` = '0' then '' else `gameVideo.threeMinRecap` end as threeMinRecap
  from `puckpandas_import`.`game_center_right_rail_import`;


### GAME PROGRESS ###
truncate table `puckpandas`.`game_progress`;
insert into `puckpandas`.`game_progress` (gameId, gameState, gameScheduleState, periodNumber, periodType, secondsRemaining, clockRunning, inIntermission, maxPeriods, lastPeriodType, regPeriods)
select a.gameId, a.gameState, a.gameScheduleState, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
       b.`clock.secondsRemaining` as secondsRemaining, b.`clock.running` as clockRunning, b.`clock.inIntermission` as inIntermission, b.maxPeriods,
       b.`gameOutcome.lastPeriodType` as lastPeriodType, b.regPeriods
  from `puckpandas_import`.`games_import` as a
  join `puckpandas_import`.`game_center_import` as b on a.gameId = b.gameId;
 

### GAME SCORES ###
truncate table `puckpandas`.`game_scores`;
insert into `puckpandas`.`game_scores` (gameId, periodType, gameOutcome, awayTeam, awayScore, awayLineScore, awaySOG, homeTeam, homeScore, homeLineScore, homeSOG)
select a.gameId, a.periodType, a.gameOutcome, a.awayTeam, a.awayTeamScore as awayScore, c.`linescore.totals.away` as awayLineScore, b.`awayTeam.sog` as awaySOG,
       a.homeTeam, a.homeTeamScore as homeScore, c.`linescore.totals.home` as homeLineScore, b.`homeTeam.sog` as homeSOG 
  from `puckpandas_import`.`games_import` as a
  join `puckpandas_import`.`game_center_import` as b on a.gameId = b.gameId
  join `puckpandas_import`.`game_center_right_rail_import` as c on a.gameId = c.gameId;


### GAME TEAM STATS ###
truncate table `puckpandas`.`game_team_stats`;
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
truncate table `puckpandas`.`game_roster_spots`;
insert into `puckpandas`.`game_roster_spots` (gameId, teamId, playerId, sweaterNumber, positionCode)
select gameId, teamId, playerId, sweaterNumber, positionCode
  from `puckpandas_import`.`roster_spots_import`;


### GAME SCRATCHES ###
truncate table `puckpandas`.`game_scratches`;
insert into `puckpandas`.`game_scratches` (gameId, playerId)
select gameId, playerId
  from `puckpandas_import`.`scratches_import`;


### PLAYS ###
truncate table `puckpandas`.`plays`;
insert into `puckpandas`.`plays` (gameId, eventId)
select gameId, eventId
  from `puckpandas_import`.`plays_import`;


### GAME PLAYS ###
truncate table `puckpandas`.`game_plays`;
insert into `puckpandas`.`game_plays` (playId, gameId, eventId, sortOrder, teamId, typeCode, situationCode,
                                       homeTeamDefendingSide, xCoord, yCoord, zoneCode)
select b.playId, a.gameId, a.eventId, a.sortOrder, a.`details.eventOwnerTeamId` as teamId, a.typeCode,
       case when a.situationCode = 0 then null else lpad(a.situationCode, 4, '0') end as situationCode,
       case when a.homeTeamDefendingSide like '0%' then null else a.homeTeamDefendingSide end as homeTeamDefendingSide,
       case when a.`details.zoneCode` like '0%' then null else a.`details.xCoord` end as xCoord,
       case when a.`details.zoneCode` like '0%'then null else a.`details.yCoord` end as yCoord,
       case when a.`details.zoneCode` like '0%' then null else a.`details.zoneCode` end as zoneCode
  from `puckpandas_import`.`plays_import` as a
  join `puckpandas`.`plays` as b on a.gameId = b.gameId and a.eventId = b.eventId;


### GAME PLAY TIMINGS ###
truncate table `puckpandas`.`game_play_timings`;
insert into `puckpandas`.`game_play_timings` (playId, gameId, eventId, periodNumber, periodType, maxRegulationPeriods, secondsInPeriod, secondsRemaining, sortOrder)
select a.playId, b.gameId, b.eventId, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
       time_to_sec(left(b.timeInPeriod, locate(':', b.timeInPeriod)+2))/60 as secondsInPeriod, 
       time_to_sec(left(b.timeRemaining, locate(':', b.timeRemaining)+2))/60 as secondsRemaining,
       b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, b.sortOrder
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId;


### GAME FACEOFFS ###
truncate table `puckpandas`.`game_faceoffs`;
insert into `puckpandas`.`game_faceoffs` (playId, gameId, eventId, losingPlayerId, winningPlayerId)
select a.playId, b.gameId, b.eventId, b.`details.losingPlayerId` as losingPlayerId, b.`details.winningPlayerId` as winningPlayerId
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode = '502';


### GAME GIVEAWAY TAKEAWAY ###
truncate table `puckpandas`.`game_giveaway_takeaway`;
insert into `puckpandas`.`game_giveaway_takeaway` (playId, gameId, eventId, sortOrder, playerId, typeCode)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.playerId` as playerId, b.typeCode
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('504', '525');


### GAME GOALS ###
truncate table `puckpandas`.`game_goals`;
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
truncate table `puckpandas`.`game_hits`;
insert into `puckpandas`.`game_hits` (playId, gameId, eventId, sortOrder, hittingPlayerId, hitteePlayerId)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.hittingPlayerId` as hittingPlayerId, b.`details.hitteePlayerId` as hitteePlayerId 
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode = '503';


### GAME PENALTIES ###
truncate table `puckpandas`.`game_penalties`;
insert into `puckpandas`.`game_penalties` (playId, gameId, eventId, sortOrder, typeCode, penaltyTypeCode, penaltyDescKey, penaltyDuration, committedByPlayerId, drawnByPlayerId)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.typeCode` as penaltyTypeCode, b.`details.descKey` as penaltyDescKey, 
       b.`details.duration` as duration, b.`details.committedByPlayerId` as committedByPlayerId, b.`details.drawnByPlayerId` as drawnByPlayerId
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('509', '535');

 
### GAME SHOTS ###
truncate table `puckpandas`.`game_shots`;
insert into `puckpandas`.`game_shots` (playId, gameId, eventId, sortOrder, typeCode, reason, shotType, shootingPlayerId, blockingPlayerId, goalieInNetId, awaySOG, homeSOG)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.reason` as reason, b.`details.shotType` as shotType, b.`details.shootingPlayerId` as shootingPlayerId, 
       b.`details.blockingPlayerId` as blockingPlayerId, b.`details.goalieInNetId` as goalieInNetId, b.`details.awaySOG` as awaySOG, b.`details.homeSOG` as homeSOG
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('506', '507', '538', '537');


### GAME STOPPAGES ### 
truncate table `puckpandas`.`game_stoppages`;
insert into `puckpandas`.`game_stoppages` (playId, gameId, eventId, sortOrder, typeCode)
select a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode
  from `puckpandas`.`plays` as a
  join `puckpandas_import`.`plays_import` as b on a.gameId = b.gameId and a.eventId = b.eventId
 where b.typeCode in ('516', '520', '521', '523', '524')
 order by playId;


### SHIFTS ###
truncate table `puckpandas`.`shifts`;
insert into `puckpandas`.`shifts` (gameId, eventNumber, detailCode, teamId, playerId, shiftNumber, period,
                                   startTimeSeconds, endTimeSeconds, durationSeconds, typeCode)
select s.gameId, s.eventNumber, s.detailCode, r.teamId, s.playerId, s.shiftNumber, s.period,
       time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 as startTimeSeconds,
       time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 +
       time_to_sec(left(s.duration, locate(':', s.duration)+2))/60 as endTimeSeconds,
       time_to_sec(left(s.duration, locate(':', s.duration)+2))/60 as durationSeconds,
       s.typeCode
  from `puckpandas_import`.`shifts_import` as s
  join `puckpandas_import`.`roster_spots_import` as r on s.gameId = r.gameId and s.playerId = r.playerId
 where s.typeCode = 517;


### SHIFT GOALS ###
truncate table `puckpandas`.`shift_goals`;
insert into `puckpandas`.`shift_goals` (gameId, eventNumber, detailCode, teamId, playerId, period, 
       goalTimeSeconds, eventDescription, eventDetails, typeCode)
select gameId, eventNumber, detailCode, teamId, playerId, period, 
       time_to_sec(left(endTime, locate(':', endTime)+2))/60 as goalTimeSeconds, 
       eventDescription, eventDetails, typeCode
  from `puckpandas_import`.`shifts_import`
where typeCode = 505;


### PLAYER BIOS ###
truncate table `puckpandas`.`player_bios`;
insert into `puckpandas`.`player_bios` (playerId, firstName, lastName, birthDate, birthCountry, birthState, birthCity,
	   shootsCatches, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms)
select playerId, `firstName.default` as firstName, `lastName.default` as lastName, birthDate,
       birthCountry, `birthStateProvince.default` as birthState, `birthCity.default` as birthCity,  
       shootsCatches, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms
  from `puckpandas_import`.`player_bios_import`;


### PLAYER STATUSES ###
truncate table `puckpandas`.`player_statuses`;
insert into `puckpandas`.`player_statuses` (playerId, isActive, currentTeamId, currentTeamAbbrev, 
       sweaterNumber, position, inTop100AllTime, inHHOF)
select playerId, isActive, currentTeamId, currentTeamAbbrev, sweaterNumber, position, inTop100AllTime, inHHOF
  from `puckpandas_import`.`player_bios_import`;


### PLAYER AWARDS ###
truncate table `puckpandas`.`player_awards`;
insert into `puckpandas`.`player_awards` (playerId, seasonId, trophyId)
select a.playerId, a.seasonId, b.trophyId
  from `puckpandas_import`.`player_award_import` as a
  join `puckpandas`.`trophies` as b on a.`trophy.default` = b.trophyName;


### PLAYER DRAFTS ###
truncate table `puckpandas`.`player_drafts`;
insert into `puckpandas`.`player_drafts` (playerId, draftYear, teamId, draftRound, pickInRound, overallPick)
select playerId, `draftDetails.year` as draftYear, b.teamId, `draftDetails.round` as draftRound, `draftDetails.pickInRound` as pickInRound, `draftDetails.overallPick` as overallPick
  from `puckpandas_import`.`player_bios_import` as a
  join `puckpandas_import`.`teams_import` as b on a.`draftDetails.teamAbbrev` = b.triCode;


### PLAYER HEADSHOTS ###
truncate table `puckpandas`.`player_headshots`;
insert into `puckpandas`.`player_headshots` (playerId, headshot)
select distinct playerId, headshot
  from `puckpandas_import`.`roster_spots_import`;


### GOALIE CAREER TOTALS ###
truncate table `puckpandas`.`goalie_career_totals`;
insert into `puckpandas`.`goalie_career_totals` (playerId, gameType, GP, G, A, PIM, GS, PTS, W, L, OTL, SA, GA, GAA, SPCT, SO, TOISEC)
select playerId, 2 as gameType, `regularSeason.gamesPlayed` as GP, `regularSeason.goals` as G, `regularSeason.assists` as A, `regularSeason.pim` as PIM, 
       `regularSeason.gamesStarted` as GS, `regularSeason.points` as PTS, `regularSeason.wins` as W, `regularSeason.losses` as L, 
       `regularSeason.otLosses` as OTL, `regularSeason.shotsAgainst` as SA, `regularSeason.goalsAgainst` as GA, 
       `regularSeason.goalsAgainstAvg` as GAA, `regularSeason.savePctg` as SPCT, `regularSeason.shutouts` as SO, 
       `regularSeason.timeOnIceSeconds` as TOISEC
  from `puckpandas_import`.`goalie_career_totals_import`
 union
select playerId, 3 as gameType, `playoffs.gamesPlayed` as GP, `playoffs.goals` as G, `playoffs.assists` as A, `playoffs.pim` as PIM, 
       `playoffs.gamesStarted` as GS, `playoffs.points` as PTS, `playoffs.wins` as W, `playoffs.losses` as L, 
       `playoffs.otLosses` as OTL, `playoffs.shotsAgainst` as SA, `playoffs.goalsAgainst` as GA, 
       `playoffs.goalsAgainstAvg` as GAA, `playoffs.savePctg` as SPCT, `playoffs.shutouts` as SO, 
       `playoffs.timeOnIceSeconds` as TOISEC
  from `puckpandas_import`.`goalie_career_totals_import`
 where `playoffs.gamesPlayed` > 0;


### GOALIE SEASONS ###
truncate table `puckpandas`.`goalie_seasons`;
insert into `puckpandas`.`goalie_seasons` (playerId, seasonId, leagueAbbrev, teamName, teamId, sequence, gameType, GP, GS, G, A, PIM, W, L, OTL, 
       `ties`, SA, GA, GAA, SPCT, SO, TOISEC)
select a.playerId, a.`season` as seasonId, a.`leagueAbbrev`, a.`teamName.default` as teamName, b.teamId, a.`sequence`, a.`gameTypeId` as gameType, 
       a.`gamesPlayed` as GP, a.`gamesStarted` as GS, a.`goals` as G, a.`assists` as A, a.`pim` as PIM, a.`wins` as W, a.`losses` as L, 
       a.`otLosses` as OTL, a.`ties`, a.`shotsAgainst` as SA, a.`goalsAgainst` as GA, a.`goalsAgainstAvg` as GAA, a.`savePctg` as SPCT, a.`shutouts` as SO, 
       a.`timeOnIceSeconds` as TOISEC
  from `puckpandas_import`.`goalie_season_import` as a
  left join `puckpandas`.`teams` as b on a.`teamName.default` = b.`fullName`;


### SKATER CAREER TOTALS ### 
truncate table `puckpandas`.`skater_career_totals`;
insert into `puckpandas`.`skater_career_totals` (playerId, gameType, GP, G, A, P, PM, PIM, PPG, PPP, SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, FOPCT)
select playerId, 2 as gameType, `regularSeason.gamesPlayed` as GP, `regularSeason.goals` as G, `regularSeason.assists` as A, 
       `regularSeason.points` as P, `regularSeason.plusMinus` as PM, `regularSeason.pim` as PIM, `regularSeason.powerPlayGoals` as PPG, 
       `regularSeason.powerPlayPoints` as PPP, `regularSeason.shorthandedGoals` as SHG, `regularSeason.shorthandedPoints` as SHP, 
       time_to_sec(left(`regularSeason.avgToi`, locate(':', `regularSeason.avgToi`)+2))/60 as TOIGSEC, 
       `regularSeason.gameWinningGoals` as GWG, `regularSeason.otGoals` as OTG, `regularSeason.shots` as S, 
       `regularSeason.shootingPctg` as SPCT, `regularSeason.faceoffWinningPctg` as FOPCT
  from `puckpandas_import`.`skater_career_totals_import`
 union
select playerId, 3 as gameType, `playoffs.gamesPlayed` as GP, `playoffs.goals` as G, `playoffs.assists` as A, 
       `playoffs.points` as P, `playoffs.plusMinus` as PM, `playoffs.pim` as PIM, `playoffs.powerPlayGoals` as PPG, 
       `playoffs.powerPlayPoints` as PPP, `playoffs.shorthandedGoals` as SHG, `playoffs.shorthandedPoints` as SHP, 
       time_to_sec(left(`playoffs.avgToi`, locate(':', `playoffs.avgToi`)+2))/60 as TOIGSEC, 
       `playoffs.gameWinningGoals` as GWG, `playoffs.otGoals` as OTG, `playoffs.shots` as S, 
       `playoffs.shootingPctg` as SPCT, `playoffs.faceoffWinningPctg` as FOPCT
  from `puckpandas_import`.`skater_career_totals_import`
 where `playoffs.gamesPlayed` > 0;



### SKATER SEASONS ###
truncate table `puckpandas`.`skater_seasons`;
insert into `puckpandas`.`skater_seasons` (playerId, seasonId, leagueId, teamName, teamId, sequence, gameType, GP, G, A, P, PM, PIM, PPG, 
       PPP, SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, FOPCT)
select a.playerId, a.season as seasonId, b.leagueId, a.`teamName.default` as teamName, c.teamId, a.sequence, a.gameTypeId as gameType, 
	   a.gamesPlayed as GP, a.goals as G, a.assists as A, a.points as P, a.plusMinus as PM, a.pim as PIM, a.powerPlayGoals as PPG, a.powerPlayPoints as PPP,
       a.shorthandedGoals as SHG, a.shorthandedPoints as SHP, 
       time_to_sec(left(a.avgToi, locate(':', a.avgToi)+2))/60 as TOIGSEC,
       a.gameWinningGoals as GWG, a.otGoals as OTG, a.shots as S, 
       a.shootingPctg as SPCT, a.faceoffWinningPctg as FOPCT
  from `puckpandas_import`.`skater_season_import` as a
  join `puckpandas`.`leagues` as b on a.leagueAbbrev = b.leagueAbbrev
  left join `puckpandas`.`teams` as c on a.`teamName.default` = c.fullName;


### TEAM ROSTERS ### 
truncate table `puckpandas`.`team_rosters`;
insert into `puckpandas`.`team_rosters` (teamId, seasonId, playerId)
select b.teamId, a.seasonId, a.playerId
  from `puckpandas_import`.`rosters_import` as a
  join `puckpandas_import`.`teams_import` as b on a.triCode = b.triCode;


### TEAMS SEASONS ###
truncate table `puckpandas`.`team_seasons`;
insert into `puckpandas`.`team_seasons` (seasonId, teamId)
select seasonId, teamId
  from `puckpandas_import`.`team_seasons_import`;


### GAME RESULTS ###
truncate table `puckpandas`.`game_results`;
insert into`puckpandas`.`game_results`
select concat(gameId, lpad(teamId, 2, 0)) as resultId, gameId, gameType, teamId, seasonId,
       teamWin, teamOT, teamLoss, awayGame, awayWin, awayOT, awayLoss, homeGame,
	   homeWin, homeOT, homeLoss, tie, overtime, awayScore, homeScore,
       case when gameType = 2 and teamWin = 1
                 then 2
            when gameType = 2 and overtime = 1 and teamWin = 0
                 then 1
            when gameType = 3 and teamWin = 1
                 then 1
            else 0
                 end as standingPoints
  from (select gameId, gameType, teamId, seasonId, awayGame, homeGame,
               case when (awayGame = 1 and awayWin = 1) or (homeGame = 1 and
               homeWin = 1) then 1 else 0 end as teamWin,
               case when (awayGame = 1 and awayWin = 0 and overtime = 1) or (homeGame = 1 and homeWin = 0 and overtime = 1) then 1 else 0 end as teamOT,
               case when (awayGame = 1 and awayWin = 0 and overtime = 0) or (homeGame = 1 and homeWin = 0 and overtime = 0) then 1 else 0 end as teamLoss,
               case when awayGame = 1 and awayWin = 1 then 1 else 0 end as awayWin,
               case when awayGame = 1 and awayWin = 0 and overtime = 1 then 1 else 0 end as awayOT,
               case when awayGame = 1 and awayWin = 0 and overtime = 0 then 1 else 0 end as awayLoss,
               case when homeGame = 1 and homeWin = 1 then 1 else 0 end as homeWin,
               case when homeGame = 1 and homeWin = 0 and overtime = 1 then 1 else 0 end as homeOT,
               case when homeGame = 1 and homeWin = 0 and overtime = 0 then 1 else 0 end as homeLoss,
			   tie, overtime, awayScore, homeScore
          from (select g.gameId, g.gameType, t.teamId, g.seasonId, 1 as awayGame, 0 as homeGame,
                       case when s.awayScore > s.homeScore then 1 else 0 end as awayWin,
                       case when s.awayScore < s.homeScore then 1 else 0 end as homeWin,
                       case when s.awayScore = s.homeScore then 1 else 0 end as tie,
                       s.awayScore, s.homeScore,
                       case when s.periodType in ("OT", "SO") then 1 else 0 end as overtime
                  from `puckpandas`.`games` as g
                  join `puckpandas`.`game_scores` as s on g.gameId = s.gameId
                  join `puckpandas`.`teams` as t on t.teamId = g.awayTeam
                  join `puckpandas`.`game_progress` as p on g.gameId = p.gameId
        		 where g.gameType in (2, 3)
                   and s.periodType in ('OT', 'REG', 'SO')
                   and p.gameState in ('FINAL', 'OFF')
                 union
				select g.gameId, g.gameType, t.teamId, g.seasonId, 0 as awayGame, 1 as homeGame,
                       case when s.awayScore > s.homeScore then 1 else 0 end as awayWin,
                       case when s.awayScore < s.homeScore then 1 else 0 end as homeWin,
                       case when s.awayScore = s.homeScore then 1 else 0 end as tie,
                       s.awayScore, s.homeScore,
                       case when s.periodType in ("OT", "SO") then 1 else 0 end as overtime
                  from `puckpandas`.`games` as g
                  join `puckpandas`.`game_scores` as s on g.gameId = s.gameId
                  join `puckpandas`.`teams` as t on t.teamId = g.homeTeam
                  join `puckpandas`.`game_progress` as p on g.gameId = p.gameId
        		 where g.gameType in (2, 3)
                   and s.periodType in ('OT', 'REG', 'SO')
                   and p.gameState in ('FINAL', 'OFF')) as a) as b;
