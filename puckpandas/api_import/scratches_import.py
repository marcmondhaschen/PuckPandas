import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class ScratchesImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'playerId', 'firstName.default', 'lastName.default']
        self.scratches_df = pd.DataFrame()
        self.query_db()
        self.scratches_df = self.scratches_df.reindex(columns=self.table_columns)

    def update_db(self):
        scratches_found = 0
        if self.scratches_df.size > 0:
            scratches_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.scratches_import (gameId, playerId, `firstName.default`, " \
                  "`lastName.default`) values (:gameId, :playerId, :firstNamedefault, :lastNamedefault)"
            scratches_df = self.scratches_df
            scratches_df.columns = scratches_df.columns.str.replace('.', '')
            params = scratches_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.GamesImportLog(game_id=self.game_id, scratches_found=scratches_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.scratches_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, playerId, `firstName.default`, `lastName.default` from " \
              "puckpandas_import.scratches_import where gameId = " + str(self.game_id)
        scratches_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if scratches_df.size > 0:
            scratches_df = scratches_df.reindex(columns=self.table_columns)
            scratches_df.infer_objects().fillna('', inplace=True)
            self.scratches_df = scratches_df

        return True

    def query_api(self):
        scratches_df = pd.json_normalize(self.json)
        scratches_df.insert(0, 'gameId', self.game_id)
        scratches_df.rename(columns={"id": "playerId"}, inplace=True)

        if scratches_df.size > 0:
            scratches_df = scratches_df.reindex(columns=self.table_columns)
            scratches_df.infer_objects().fillna('', inplace=True)
            self.scratches_df = scratches_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
