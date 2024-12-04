# 2024 NHL API Query notes

Drew Hynes github update on 2024-11-02 has a great many more queries. 
Most of those have been added to the existing lists, below.

### teams
	- use https://api.nhle.com/stats/rest/en/team
		returns every 3 letter [TEAM TRI-CODE]

### seasons by team
	- use https://api-web.nhle.com/v1/roster-season/ [TEAM TRI-CODE]
	- returns 8-digit [SEASON ID]

### club schedules
	- use https://api-web.nhle.com/v1/club-schedule-season/ [TRI-CODE]/now
	- use https://api-web.nhle.com/v1/club-schedule-season/ [TRI-CODE]/ [SEASON ID]
	- returns 10-digit [GAME ID]

### rosters
	- use https://api-web.nhle.com/v1/roster/ [TRI-CODE]/current
	- use https://api-web.nhle.com/v1/roster/ [TRI-CODE]/ [SEASON ID]
	- returns 7- or 8-digit [PLAYER ID]

### game center
	- use https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/play-by-play
		- most of the game details are contained here
		- capture using multiple tables for each sub-array under the game center header
			- game center header
			- tvBroadcasts array
			- play-by-play array
			- rosterSpots array
	- use https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/right-rail
		- slightly less useful detail that's displayed along the game summary web page's "right rail"
		- as with the play-by-play report, this data should be captured in multiple tables
		- no need to recapture header info as it's redundant, but useful sub-arrays are...
			- seasonSeries array
			- linescore/byPeriod array
			- gameInfo/linesmen array
			- gameInfo/referees array
			- gameInfo/awayTeam/scratches array
			- gameInfo/homeTeam/scratches array

### players
	- use https://api-web.nhle.com/v1/player/ [PLAYER ID]/landing
	- will want multiple tables to capture
		- one for draft details
		- one for totals by season
		- one for career totals


## GOOD TO HAVE

### countries
	- use https://api.nhle.com/stats/rest/en/country
	
### draft picks
	- use https://api-web.nhle.com/v1/draft/picks/ [YEAR]/all
		draft picks for a given calendar year (not SEASON ID)
		
### draft rankings
	- use https://api-web.nhle.com/v1/draft/rankings/ [YEAR]/now
	- use https://api-web.nhle.com/v1/draft/rankings/ [YEAR]/ [CATEGORY]
		Categories are 0 - NA forwards & defenders, 1 - Intl forwards & defenders, 
		2 - NA goalies, 3 - Intl goalies

### playoff-series
	- use https://api-web.nhle.com/v1/schedule/playoff-series
		- only valid while in playoff season

### players
	- use https://api-web.nhle.com/v1/player/ [PLAYER ID]/game-log/now
	- use https://api-web.nhle.com/v1/player/ [PLAYER ID]/game-log/ [SEASON ID]/ [GAME TYPE]
		useful summary of stats for this player by season id and game type
		'now' version defaults to current season and game type (preseason/regular/playoff)

### prospects
	- use https://api-web.nhle.com/v1/prospects/ [TRI-CODE]
		summary of current prospects by team	
		sub-arrays for each position (forwards, defense, goalies)
		
### schedule
	- use https://api-web.nhle.com/v1/schedule/now
	- use https://api-web.nhle.com/v1/schedule/ [DATE]
		for any given date, provides an array of all the games played that week 
			and all the oddsPartners and odds for any unplayed games

### schedule by club and month
	- use https://api-web.nhle.com/v1/club-schedule/ [TRI-CODE]/month/now
	- use https://api-web.nhle.com/v1/club-schedule/ [TRI-CODE]/month/2024-12
	- use https://api-web.nhle.com/v1/club-schedule/ [TRI-CODE]/week/now
	- use https://api-web.nhle.com/v1/club-schedule/ [TRI-CODE]/week/2024-12-26
		games scheduled for a given team on a given month/week

### schedule calendar
	- use https://api-web.nhle.com/v1/schedule-calendar/now
	- use https://api-web.nhle.com/v1/schedule-calendar/ [DATE]
		for any given date (or today) gives a detailed list of teams

### score
	- use https://api-web.nhle.com/v1/score/now
	- use https://api-web.nhle.com/v1/score/ [DATE]
		summary of the day's scores by game
		scoring info is mostly redundant
		includes oddsmakers and game odds
		for games not yet played, includes odds published by oddsmaker

### scoreboard
	- use https://api-web.nhle.com/v1/scoreboard/ [TRI-CODE]/now
	- use https://api-web.nhle.com/v1/scoreboard/now
		provides current calendar of events, focused by team if desired

### season
	- use https://api-web.nhle.com/v1/season
		provides an array of all seasons played to date

### season start and stop 
	- use https://api-web.nhle.com/v1/standings-season
		start and stop dates for the regular season, for all seasons 
 		some fields here aren't included in the comparable https://api.nhle.com/stats/rest/en/season

### skater stats leaders
	- use https://api-web.nhle.com/v1/skater-stats-leaders/current
	- use https://api-web.nhle.com/v1/skater-stats-leaders/ [SEASON ID]/ [GAME TYPE]
		Top 5 stats summaries for eh goals, plus/minus, assists, pp goals, faceoffs, goals, points, toi

### standings
	- use https://api-web.nhle.com/v1/standings/now
	- use https://api-web.nhle.com/v1/standings/ [DATE]
		- HAS CONFERENCE AND DIVISION!!! (can't seem to find on any other query?)
		- will need to source appropriate dates for each season, probably close of each reg season?
		- close of each reg season is contained in .../standings-season/

### tv schedule
	- use https://api-web.nhle.com/v1/network/tv-schedule/now
	- use https://api-web.nhle.com/v1/network/tv-schedule/ [DATE]
		summary of all programs scheduled for a given day (or today)

### where to watch
	- use https://api-web.nhle.com/v1/where-to-watch
		League recommended streaming & web links by country code

## DON'T NEED

### club stats
	- use https://api-web.nhle.com/v1/club-stats/ [TRI-CODE]/now
	- use https://api-web.nhle.com/v1/club-stats/ [TRI-CODE]/ [SEASON ID]/ [GAME TYPE]
		summary statistics by season & game type for each skater or goalie on a given team
		redundant with other reports

### franchises
	- use https://api.nhle.com/stats/rest/en/franchise

### game center
	- use https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/boxscore
		summary of game stats and score
		useful info in the playerByGameStats/[homeTeam/awayTeam]/[forwards/defense/goalies]/ 
			arrays - 6 arrays in total!
	- use https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/landing
		all of this data should be redundant with other reports

### goalie stats leaders
	- use https://api-web.nhle.com/v1/goalie-stats-leaders/current
	- use https://api-web.nhle.com/v1/goalie-stats-leaders/ [SEASON ID]/ [GAME TYPE]
		Top 5 goalies in wins, shutouts, savePctg, goalsAgainstAverage, focused by season & game type if desired

### player spotlight
	- use https://api-web.nhle.com/v1/player-spotlight
		- top 10 players hand picked by NHL


## [KEY GLOSSARY]

[GAME ID]
	- unique to game
	- 10-digits
	- first four digits are year of season open

[GAME TYPE]
	- sometimes gameTypeId
	- 1 = preseason and exhibition games
	- 2 = regular season
	- 3 = post season
	- 4 = intra-league exhibition games

[PLAYER ID]
	- unique to player
	- follows player through trades, etc

[SEASON ID]
	- unique to season
	- four-digit beginning year + four-digit ending year, no spaces i.e. '20212022'

[TEAM TRI-CODE]
	- unique to team
	- defunct teams (ATL, HFD) listed

[DATE]
	- a calendar date, in YYYY-MM-DD format