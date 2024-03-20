## [KEY GLOSSARY]
# the api uses a set of useful 'keys' to relate tables together
# most of these keys are fairly intuitive, but each that this code uses 
# is listed below

[gameId]
	- unique to game
	- 10-digits
	- first four digits are year of season open

[gameType]
	- sometimes gameTypeId
	- 1 = preseason or exhibition?
	- 2 = regular season
	- 3 = post season
	- 4 = preseason or exhibition?

[playerId]
	- unique to player
	- follows player through trades, etc

[seasonId]
	- unique to season
	- four-digit beginning year + four-digit ending year, no spaces i.e. '20212022'

[teamId]
	- numeric
	- unique to team
	- 1 or 2 digits
	- issued in chronological order (old teams are low digits)
	- not to be confused with franchiseId

[triCode] 
	- unique to team
	- defunct teams (ATL, HFD) listed