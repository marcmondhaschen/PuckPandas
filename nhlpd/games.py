import pandas as pd
import nhlpd
from sqlalchemy import text


class GamesImport:
    def __init__(self, team_id, season_id):
        self.team_id = team_id
        self.season_id = season_id
        self.teams = nhlpd.TeamsImport()
        self.table_columns = ['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite', 'startTimeUTC',
                              'venueUTCOffset', 'venueTimezone', 'gameState', 'gameScheduleState', 'awayTeam',
                              'awayTeamSplitSquad', 'awayTeamScore', 'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore',
                              'periodType', 'gameOutcome', 'seriesStatus.round', 'seriesStatus.seriesAbbrev',
                              'seriesStatus.seriesTitle', 'seriesStatus.seriesLetter', 'seriesStatus.neededToWin',
                              'seriesStatus.topSeedWins', 'seriesStatus.bottomSeedWins',
                              'seriesStatus.gameNumberOfSeries']
        self.games_df = pd.DataFrame()
        self.query_db()
        self.games_df = self.games_df.reindex(columns=self.table_columns)

    def update_db(self):
        games_found = 0
        if self.games_df.size > 0:
            games_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into games_import (gameId, seasonId, gameType, gameDate, venue, neutralSite, " \
                  "startTimeUTC, venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, " \
                  "awayTeamSplitSquad, awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, " \
                  "periodType, gameOutcome, `seriesStatus.round`, `seriesStatus.seriesAbbrev`, " \
                  "`seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, `seriesStatus.neededToWin`, " \
                  "`seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, `seriesStatus.gameNumberOfSeries`) " \
                  "values (:gameId, :seasonId, :gameType, :gameDate, :venue, :neutralSite, :startTimeUTC, " \
                  ":venueUTCOffset, :venueTimezone, :gameState, :gameScheduleState, :awayTeam, " \
                  ":awayTeamSplitSquad, :awayTeamScore, :homeTeam, :homeTeamSplitSquad, :homeTeamScore, " \
                  ":periodType, :gameOutcome, :seriesStatusround, :seriesStatusseriesAbbrev, " \
                  ":seriesStatusseriesTitle, :seriesStatusseriesLetter, :seriesStatusneededToWin, " \
                  ":seriesStatustopSeedWins, :seriesStatusbottomSeedWins, :seriesStatusgameNumberOfSeries)"
            games_transform_df = self.games_df
            games_transform_df.columns = games_transform_df.columns.str.replace('.', '')
            params = games_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

            for index, row in games_transform_df.iterrows():
                game_log = nhlpd.GamesImportLog(row['gameId'], game_found=1)
                game_log.insert_db()

            season_log = nhlpd.SeasonsImportLog(team_id=self.team_id, season_id=self.season_id, games_found=games_found)
            season_log.insert_db()

            engine.dispose()

        return True

    def clear_db(self):
        if self.team_id != '' and self.season_id != '':
            engine = nhlpd.dba_import_login()
            sql = "delete from games_import where gameId > 0" + " and (homeTeam = " + str(self.team_id) + \
                  " or awayTeam = " + str(self.team_id) + ")" + " and seasonId = '" + str(self.season_id) + "'"
            with engine.connect() as conn:
                conn.execute(text(sql))
            engine.dispose()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, venueUTCOffset, " \
              "venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, awayTeamScore, homeTeam, " \
              "homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome, `seriesStatus.round`, " \
              "`seriesStatus.seriesAbbrev`, `seriesStatus.seriesTitle`, `seriesStatus.seriesLetter`, " \
              "`seriesStatus.neededToWin`, `seriesStatus.topSeedWins`, `seriesStatus.bottomSeedWins`, " \
              "`seriesStatus.gameNumberOfSeries` from games_import where gameId > 0 and (homeTeam = " + \
               str(self.team_id) + " or awayTeam = " + str(self.team_id) + ") and seasonId = '" + \
               str(self.season_id) + "'"
        games_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if games_df.size > 0:
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.infer_objects().fillna('', inplace=True)
            games_df.drop_duplicates(inplace=True)
            self.games_df = games_df

        return self.games_df

    def query_nhl(self):
        # each page call is a complete season for a given team
        tri_code = self.teams.tri_code_from_team_id(team_id=self.team_id)

        base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
        query_string = "{}{}/{}".format(base_url, tri_code, self.season_id)
        json_data = nhlpd.fetch_json_data(query_string)

        if 'games' in json_data:
            games_df = pd.json_normalize(json_data, record_path=['games'])
            if 'tvBroadcasts' in games_df:
                games_df.drop(columns='tvBroadcasts', inplace=True)

            games_df.rename(columns={'id': 'gameId', 'season': 'seasonId', 'venue.default': 'venue',
                                     'awayTeam.id': 'awayTeam', 'awayTeam.awaySplitSquad': 'awayTeamSplitSquad',
                                     'awayTeam.score': 'awayTeamScore', 'homeTeam.id': 'homeTeam',
                                     'homeTeam.homeSplitSquad': 'homeTeamSplitSquad', 'homeTeam.score': 'homeTeamScore',
                                     'periodDescriptor.periodType': 'periodType',
                                     'gameOutcome.lastPeriodType': 'gameOutcome'}, inplace=True)
            games_df = games_df.reindex(columns=self.table_columns)
            games_df.drop(columns=['homeTeam.commonName.fr', 'awayTeam.commonName.fr'], errors='ignore')
            games_df.fillna(0, inplace=True)

            if games_df.size > 0:
                self.games_df = games_df

        return self.games_df

    def query_nhl_update_db(self):
        # For this object, this pattern has the side effect of deleting duplicate gameIds in the games_import table.
        # Each game is presented twice by the API - once for each opposing team. the
        # clear method will drop games from a team about to be imported, removing their impending duplication on import
        # but leaving behind all the previous competitors' matches that didn't involve them.
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True
