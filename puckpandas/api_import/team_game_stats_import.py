import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class TeamGameStatsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'category', 'awayValue', 'homeValue']
        self.team_game_stats_df = pd.DataFrame()
        self.query_db()
        self.team_game_stats_df = self.team_game_stats_df.reindex(columns=self.table_columns)

    def update_db(self):
        team_game_stats_found = 0
        if self.team_game_stats_df.size > 0:
            team_game_stats_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.team_game_stats_import (gameId, category, awayValue, homeValue) " \
                  "values (:gameId, :category, :awayValue, :homeValue)"
            params = self.team_game_stats_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, team_game_stats_found=team_game_stats_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.team_game_stats_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, category, awayValue, homeValue from puckpandas_import.team_game_stats_import " \
              "where gameId = " + str(self.game_id)
        team_game_stats_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if team_game_stats_df.size > 0:
            team_game_stats_df = team_game_stats_df.reindex(columns=self.table_columns)
            team_game_stats_df.infer_objects().fillna('', inplace=True)
            self.team_game_stats_df = team_game_stats_df

        return True

    def query_api(self):
        team_game_stats_df = pd.json_normalize(self.json)
        team_game_stats_df.insert(0, 'gameId', self.game_id)

        if team_game_stats_df.size > 0:
            team_game_stats_df = team_game_stats_df.reindex(columns=self.table_columns)
            team_game_stats_df.infer_objects().fillna('', inplace=True)
            self.team_game_stats_df = team_game_stats_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
