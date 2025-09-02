import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameScratches:
    def __init__(self):
        self.table_columns = ['id','gameId','playerId']
        self.game_scratches_df = pd.DataFrame()
        self.query_db()
        self.game_scratches_df = self.game_scratches_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_scratches_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_scratches (gameId, playerId) select s.gameId, s.playerId from 
                puckpandas_import.scratches_import as s join puckpandas_import.games_import as g on s.gameId = 
                g.gameId where g.seasonId =  """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_scratches (gameId, playerId) select s.gameId, s.playerId from 
                puckpandas_import.scratches_import as s join puckpandas_import.games_import as g on s.gameId = 
                g.gameId"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_scratches"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, gameId, playerId puckpandas.game_scratches"""
        game_scratches_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_scratches_df.size > 0:
            game_scratches_df = game_scratches_df.reindex(columns=self.table_columns)
            game_scratches_df.infer_objects().fillna('', inplace=True)
            game_scratches_df.drop_duplicates(inplace=True)
            self.game_scratches_df = game_scratches_df

        return self.game_scratches_df
