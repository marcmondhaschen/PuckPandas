import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class LinesmenImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'default']
        self.linesmen_df = pd.DataFrame()
        self.query_db()
        self.linesmen_df = self.linesmen_df.reindex(columns=self.table_columns)

    def update_db(self):
        linesmen_found = 0
        if self.linesmen_df.size > 0:
            linesmen_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.linesmen_import (gameId, `default`) values (:gameId, :default)"
            params = self.linesmen_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id,
                                        linesmen_found=linesmen_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.linesmen_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, `default` from puckpandas_import.linesmen_import where gameId = " + str(self.game_id)
        linesmen_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if linesmen_df.size > 0:
            linesmen_df = linesmen_df.reindex(columns=self.table_columns)
            linesmen_df.infer_objects().fillna('', inplace=True)
            self.linesmen_df = linesmen_df

        return True

    def query_api(self):
        linesmen_df = pd.json_normalize(self.json)
        linesmen_df.insert(0, 'gameId', self.game_id)

        if linesmen_df.size > 0:
            linesmen_df = linesmen_df.reindex(columns=self.table_columns)
            linesmen_df.infer_objects().fillna('', inplace=True)
            self.linesmen_df = linesmen_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
