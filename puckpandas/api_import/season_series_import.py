import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class SeasonSeriesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'seriesNumber', 'refGameId']
        self.season_series_df = pd.DataFrame()
        self.query_db()
        self.season_series_df = self.season_series_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_series_found = 0
        if self.season_series_df.size > 0:
            season_series_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.season_series_import (gameId, seriesNumber, refGameId) values " \
                  "(:gameId, :seriesNumber, :refGameId)"
            params = self.season_series_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, season_series_found=season_series_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.season_series_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, seriesNumber, refGameId from puckpandas_import.season_series_import where gameId = " + \
              str(self.game_id)
        season_series_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if season_series_df.size > 0:
            season_series_df = season_series_df.reindex(columns=self.table_columns)
            season_series_df.infer_objects().fillna('', inplace=True)
            self.season_series_df = season_series_df

        return True

    def query_api(self):
        season_series_df = pd.json_normalize(self.json)
        # noinspection PyTypeChecker
        season_series_df.insert(0, 'seriesNumber', range(len(season_series_df)))
        season_series_df.insert(0, 'gameId', self.game_id)
        season_series_df.rename(columns={"id": "refGameId"}, inplace=True)

        if season_series_df.size > 0:
            season_series_df = season_series_df.reindex(columns=self.table_columns)
            season_series_df.infer_objects().fillna('', inplace=True)
            self.season_series_df = season_series_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
