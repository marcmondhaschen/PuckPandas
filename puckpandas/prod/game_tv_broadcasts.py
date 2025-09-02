import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameTVBroadcasts:
    def __init__(self):
        self.table_columns = ['gameBroadcastId','gameId','broadcastId','sequenceNumber','market','countryCode',
                              'network']
        self.game_tv_broadcasts_df = pd.DataFrame()
        self.query_db()
        self.game_tv_broadcasts_df = self.game_tv_broadcasts_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_tv_broadcasts_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_tv_broadcasts (gameId, broadcastId, sequenceNumber, market, 
                countryCode, network) select t.gameId, t.broadcastId, t.sequenceNumber, t.market, t.countryCode, 
                t.network from puckpandas_import.tv_broadcasts_import as t join puckpandas_import.games_import as g on 
                t.gameId = g.gameId where g.seasonId = """ + str(season_id) + """ order by t.gameId, 
                t.sequenceNumber"""
            else:
                sql = """insert into puckpandas.game_tv_broadcasts (gameId, broadcastId, sequenceNumber, market, 
                countryCode, network) select t.gameId, t.broadcastId, t.sequenceNumber, t.market, t.countryCode, 
                t.network from puckpandas_import.tv_broadcasts_import as t join puckpandas_import.games_import as g on 
                t.gameId = g.gameId order by t.gameId, t.sequenceNumber"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_tv_broadcasts"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select gameBroadcastId, gameId, broadcastId, sequenceNumber, market, countryCode, network from 
        puckpandas.game_tv_broadcasts"""
        game_tv_broadcasts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_tv_broadcasts_df.size > 0:
            game_tv_broadcasts_df = game_tv_broadcasts_df.reindex(columns=self.table_columns)
            game_tv_broadcasts_df.infer_objects().fillna('', inplace=True)
            game_tv_broadcasts_df.drop_duplicates(inplace=True)
            self.game_tv_broadcasts_df = game_tv_broadcasts_df

        return self.game_tv_broadcasts_df
