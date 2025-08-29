import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class TvBroadcastsImport:
    def __init__(self, game_id):
        self.game_id = game_id
        self.json = {}
        self.table_columns = ['gameId', 'broadcastId', 'market', 'countryCode', 'network', 'sequenceNumber']
        self.tv_broadcasts_df = pd.DataFrame()
        self.query_db()
        self.tv_broadcasts_df = self.tv_broadcasts_df.reindex(columns=self.table_columns)

    def update_db(self):
        tv_broadcasts_found = 0
        if self.tv_broadcasts_df.size > 0:
            tv_broadcasts_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.tv_broadcasts_import (gameId, broadcastId, market, countryCode, " \
                  "network, sequenceNumber) values (:gameId, :broadcastId, :market, :countryCode, :network, " \
                  ":sequenceNumber)"
            params = self.tv_broadcasts_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), params)

        log = pp.GamesImportLog(game_id=self.game_id, tv_broadcasts_found=tv_broadcasts_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.tv_broadcasts_import where gameId = " + str(self.game_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select gameId, broadcastId, market, countryCode, network, sequenceNumber from " \
              "puckpandas_import.tv_broadcasts_import where gameId = " + str(self.game_id)
        tv_broadcasts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if tv_broadcasts_df.size > 0:
            tv_broadcasts_df = tv_broadcasts_df.reindex(columns=self.table_columns)
            tv_broadcasts_df.infer_objects().fillna('', inplace=True)
            self.tv_broadcasts_df = tv_broadcasts_df

        return True

    def query_api(self):
        tv_broadcasts_df = pd.json_normalize(self.json)
        tv_broadcasts_df.rename(columns={"id": "broadcastId"}, inplace=True)
        tv_broadcasts_df.insert(0, 'gameId', self.game_id)

        if tv_broadcasts_df.size > 0:
            tv_broadcasts_df = tv_broadcasts_df.reindex(columns=self.table_columns)
            tv_broadcasts_df.infer_objects().fillna('', inplace=True)
            self.tv_broadcasts_df = tv_broadcasts_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
