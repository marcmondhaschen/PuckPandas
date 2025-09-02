import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameLinesmen:
    def __init__(self):
        self.table_columns = ['id','gameId','linesmanId']
        self.game_linesmen_df = pd.DataFrame()
        self.query_db()
        self.game_linesmen_df = self.game_linesmen_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_linesmen_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_linesmen (gameId, linesmanId) select a.gameId, b.linesmanId from 
                puckpandas_import.linesmen_import as a  join puckpandas_import.games_import as g on a.gameId = g.gameId 
                join puckpandas.linesmen as b on a.default = b.linesmanName where 
                g.seasonId = """ + str(season_id)

            else:
                sql = """insert into puckpandas.game_linesmen (gameId, linesmanId) select a.gameId, b.linesmanId from 
                puckpandas_import.linesmen_import as a  join puckpandas_import.games_import as g on a.gameId = 
                g.gameId join puckpandas.linesmen as b on a.default = b.linesmanName"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_linesmen"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, gameId, linesmanId from puckpandas.game_linesmen"""
        game_linesmen_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_linesmen_df.size > 0:
            game_linesmen_df = game_linesmen_df.reindex(columns=self.table_columns)
            game_linesmen_df.infer_objects().fillna('', inplace=True)
            game_linesmen_df.drop_duplicates(inplace=True)
            self.game_linesmen_df = game_linesmen_df

        return self.game_linesmen_df
