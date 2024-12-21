from datetime import datetime, timezone
import pandas as pd
import nhlpd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class GamesImport:
    games_df = pd.DataFrame(columns=['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite',
                                     'startTimeUTC', 'venueUTCOffset', 'venueTimezone', 'gameState',
                                     'gameScheduleState', 'awayTeam', 'awayTeamSplitSquad', 'awayTeamScore',
                                     'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore', 'periodType', 'gameOutcome',
                                     'seriesStatus.round', 'seriesStatus.seriesAbbrev', 'seriesStatus.seriesTitle',
                                     'seriesStatus.seriesLetter', 'seriesStatus.neededToWin',
                                     'seriesStatus.topSeedWins', 'seriesStatus.bottomSeedWins',
                                     'seriesStatus.gameNumberOfSeries'])

    def __init__(self, team_id, season_id):
        self.team_id = team_id
        self.season_id = season_id
        self.teams = nhlpd.TeamsImport()
        self.games_df = pd.concat([self.games_df, self.query_db()])

    def update_db(self):
        if self.games_df.size > 0:
            cursor, db = db_import_login()

            for index, row in self.games_df.iterrows():
                sql = "insert into games_import (gameId, seasonId, gameType, gameDate, venue, neutralSite, " \
                      "startTimeUTC, venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, " \
                      "awayTeamSplitSquad, awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, " \
                      "periodType, gameOutcome, `seriesStatus.round`, `seriesStatus.seriesAbbrev`, " \
                      "`seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, `seriesStatus.neededToWin`, " \
                      "`seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, `seriesStatus.gameNumberOfSeries`) " \
                      "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                      "%s, %s, %s, %s, %s, %s)"
                val = (row['gameId'], row['seasonId'], row['gameType'], row['gameDate'], row['venue'],
                       row['neutralSite'], row['startTimeUTC'], row['venueUTCOffset'], row['venueTimezone'],
                       row['gameState'], row['gameScheduleState'], row['awayTeam'], row['awayTeamSplitSquad'],
                       row['awayTeamScore'], row['homeTeam'], row['homeTeamSplitSquad'], row['homeTeamScore'],
                       row['periodType'], row['gameOutcome'], row['seriesStatus.round'],
                       row['seriesStatus.seriesAbbrev'], row['seriesStatus.seriesTitle'],
                       row['seriesStatus.seriesLetter'], row['seriesStatus.neededToWin'],
                       row['seriesStatus.topSeedWins'], row['seriesStatus.bottomSeedWins'],
                       row['seriesStatus.gameNumberOfSeries'])
                cursor.execute(sql, val)

                game_log = nhlpd.GamesImportLog(row['gameId'], datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                                                game_found=1)
                game_log.insert_db()

            season_log = nhlpd.SeasonsImportLog(team_id=self.team_id, season_id=self.season_id)
            season_log.insert_db()

            db.commit()
            cursor.close()
            db.close()

        return True

    def clear_db(self):
        if self.team_id != '' and self.season_id != '':
            cursor, db = db_import_login()
            sql = "delete from games_import where gameId > 0" + " and (homeTeam = " + str(self.team_id) + \
                  " or awayTeam = " + str(self.team_id) + ")" + " and seasonId = '" + str(self.season_id) + "'"

            cursor.execute(sql)

            db.commit()
            cursor.close()
            db.close()

        return True

    def query_db(self):
        cursor, db = db_import_login()
        sql = (("select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, venueUTCOffset, "
               "venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, awayTeamScore, homeTeam, "
               "homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome, `seriesStatus.round`, "
               "`seriesStatus.seriesAbbrev`, `seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, "
               "`seriesStatus.neededToWin`, `seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, "
               "`seriesStatus.gameNumberOfSeries` from games_import where gameId > 0 and (homeTeam = ") +
               str(self.team_id) + " or awayTeam = " + str(self.team_id) + ") and seasonId = '" +
               self.season_id + "'")
        query_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        games_df = self.games_df.head(0)
        games_df = pd.concat([games_df, query_df])
        games_df.fillna('', inplace=True)
        games_df.drop_duplicates(inplace=True)
        self.games_df = games_df

        return self.games_df

    def query_nhl(self):
        # each page call is a complete season for a given team
        tri_code = self.teams.tri_code_from_team_id(team_id=self.team_id)

        base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
        query_string = "{}{}/{}".format(base_url, tri_code, self.season_id)
        json_data = fetch_json_data(query_string)

        if 'games' in json_data:
            team_schedule_df = pd.json_normalize(json_data, record_path=['games'])
            if 'tvBroadcasts' in team_schedule_df:
                team_schedule_df.drop(columns='tvBroadcasts', inplace=True)

            team_schedule_df.rename(columns={'id': 'gameId', 'season': 'seasonId', 'venue.default': 'venue',
                                             'awayTeam.id': 'awayTeam', 'awayTeam.awaySplitSquad': 'awayTeamSplitSquad',
                                             'awayTeam.score': 'awayTeamScore', 'homeTeam.id': 'homeTeam',
                                             'homeTeam.homeSplitSquad': 'homeTeamSplitSquad',
                                             'homeTeam.score': 'homeTeamScore',
                                             'periodDescriptor.periodType': 'periodType',
                                             'gameOutcome.lastPeriodType': 'gameOutcome'}, inplace=True)
            games_df = self.games_df.head(0)
            games_df = pd.concat([games_df, team_schedule_df])
            games_df.fillna('', inplace=True)
            games_df.dropna(axis=1, inplace=True)

            self.games_df = games_df

        return self.games_df

    def query_nhl_update_db(self):
        # for this object, this pattern has the beneficial side benefit of deleting duplicate gameIds in the
        # games_import table. each game is presented twice by the API calls - once for each opposing team. the
        # clear method will drop games from a team about to be imported, removing their impending duplication on import
        # but leaving behind all the previous competitors' matches that didn't involve them.
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True
