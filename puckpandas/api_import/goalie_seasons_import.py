import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class GoalieSeasonsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'gameTypeId', 'gamesPlayed', 'goalsAgainst', 'goalsAgainstAvg',
                              'leagueAbbrev', 'losses', 'season', 'sequence', 'shutouts', 'ties', 'timeOnIce',
                              'timeOnIceMinutes', 'timeOnIceSeconds', 'wins', 'teamName.default', 'savePctg',
                              'shotsAgainst', 'otLosses', 'assists', 'gamesStarted', 'goals', 'pim']
        self.goalie_season_df = pd.DataFrame()
        self.goalie_season_df = self.goalie_season_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_totals_found = 0
        if self.json != {}:
            season_totals_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.goalie_season_import (playerId, gameTypeId, gamesPlayed, " \
                  "goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, season, sequence, shutouts, ties, timeOnIce, " \
                  "timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, savePctg, shotsAgainst, " \
                  "otLosses, assists, gamesStarted, goals, pim) values (:playerId, :gameTypeId, :gamesPlayed, " \
                  ":goalsAgainst, :goalsAgainstAvg, :leagueAbbrev, :losses, :season, :sequence, :shutouts, :ties, " \
                  ":timeOnIce, :timeOnIceMinutes, :timeOnIceSeconds, :wins, :teamNamedefault, :savePctg, " \
                  ":shotsAgainst, :otLosses, :assists, :gamesStarted, :goals, :pim)"
            goalie_season_transform_df = self.goalie_season_df
            goalie_season_transform_df.columns = goalie_season_transform_df.columns.str.replace('.', '')
            params = goalie_season_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.PlayerImportLog(player_id=self.player_id, season_totals_found=season_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.goalie_season_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, season, "\
              "sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, "\
              "savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, pim from " \
              "puckpandas_import.goalie_season_import where playerId = " + str(self.player_id)
        goalie_season_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_season_df.size > 0:
            goalie_season_df = goalie_season_df.reindex(columns=self.table_columns)
            goalie_season_df.infer_objects().fillna('', inplace=True)
            self.goalie_season_df = goalie_season_df

        return True

    def query_api(self):
        goalie_season_df = pd.json_normalize(self.json)
        goalie_season_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_season_df.insert(0, 'playerId', self.player_id)

        if goalie_season_df.size > 0:
            goalie_season_df = goalie_season_df.reindex(columns=self.table_columns)
            goalie_season_df.fillna(0, inplace=True)
            self.goalie_season_df = goalie_season_df

        if not self.goalie_season_df.empty:
            self.goalie_season_df['timeOnIce'] = self.goalie_season_df['timeOnIce'].astype(object)
            self.goalie_season_df.loc[self.goalie_season_df.timeOnIce == 0, 'timeOnIce'] = '00:00'
            self.goalie_season_df[['timeOnIceMinutes', 'timeOnIceSeconds']] = (
                self.goalie_season_df['timeOnIce'].str.split(":", expand=True))
            self.goalie_season_df['timeOnIceSeconds'] = (self.goalie_season_df['timeOnIceMinutes'].astype(int) * 60 +
                                                         self.goalie_season_df['timeOnIceSeconds'].astype(int))

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
