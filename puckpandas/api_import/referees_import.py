import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class RefereesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'default']
        self.referees_df = pd.DataFrame()
        self.query_db()
        self.referees_df = self.referees_df.reindex(columns=self.table_columns)

    def update_db(self):
        referees_found = 0
        if self.referees_df.size > 0:
            referees_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.referees_import (gameId, `default`) values (:gameId, :default)"
            params = self.referees_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, referees_found=referees_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.referees_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, `default` from puckpandas_import.referees_import where gameId = " + str(self.game_id)
        referees_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if referees_df.size > 0:
            referees_df = referees_df.reindex(columns=self.table_columns)
            referees_df.infer_objects().fillna('', inplace=True)
            self.referees_df = referees_df

        return True

    def query_api(self):
        referees_df = pd.json_normalize(self.json)
        referees_df.insert(0, 'gameId', self.game_id)

        if referees_df.size > 0:
            referees_df = referees_df.reindex(columns=self.table_columns)
            referees_df.infer_objects().fillna('', inplace=True)
            self.referees_df = referees_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
