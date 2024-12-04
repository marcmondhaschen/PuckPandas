# 2024 NHL API Query notes

## MUST HAVE

### teams
	- use https://api.nhle.com/stats/rest/en/team
	- returns 3 letter [TEAM TRI-CODE]

### seasons played by team
	- use https://api-web.nhle.com/v1/roster-season/ [TEAM TRI-CODE]
	- returns 8-digit [SEASON ID]

### schedules
	- use https://api-web.nhle.com/v1/club-schedule-season/ [TEAM TRI-CODE]/ [SEASON ID]
	- returns 10-digit [GAME ID]

### rosters
	- use https://api-web.nhle.com/v1/roster/ [TEAM TRI-CODE]/ [SEASON ID]
	- returns 7- or 8-digit [PLAYER ID]

### game details
	- use https://api-web.nhle.com/v1/gamecenter/ [GAME ID]/play-by-play
	- will want multiple tables to capture
		- one for match information (teams, venue, date, etc.)
		- one for the play by play
		- one for summary information (scores, reg/OT)
		- one for rosters
	- notice plays array - most of the PBP info is here

### players
	- use https://api-web.nhle.com/v1/player/ [PLAYER ID]/landing
	- will want multiple tables to capture
		- one for draft details
		- one for totals by season
		- one for career totals


## GOOD TO HAVE

### divisions, conferences, and standings
	- use https://api-web.nhle.com/v1/standings/[DATE]
		- will need to source appropriate dates for each season, probably close of each reg season?
		- close of each reg season is contained in .../standings-season/


### standings calculation details by season (standings-season)
	- use https://api-web.nhle.com/v1/standings-season
 		- some fields here aren't included in the comparable https://api.nhle.com/stats/rest/en/season

### franchises
	- use https://api.nhle.com/stats/rest/en/franchise

### countries
	- use https://api.nhle.com/stats/rest/en/country

### game summary by player
	- use https://api-web.nhle.com/v1/player/ [PLAYER ID]/game-log/ [SEASON ID]/ [GAME TYPE]
	
### team details
	- venue details
	- UTC offsets
	- broadcast details

### build a gif out of progressive player images???

## [KEY GLOSSARY]

[GAME ID]
	- unique to game
	- 10-digits
	- first four digits are year of season open

[GAME TYPE]
	- sometimes gameTypeId
	- 2 = regular season
	- 3 = post season

[PLAYER ID]
	- unique to player
	- follows player through trades, etc

[SEASON ID]
	- unique to season
	- four-digit beginning year + four-digit ending year, no spaces i.e. '20212022'

[TEAM TRI-CODE]
	- unique to team
	- defunct teams (ATL, HFD) listed