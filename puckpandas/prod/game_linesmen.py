import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameLinesmen:
    def __init__(self):
        self.table_columns = ['id','gameId','linesmanId']
        self.game_linesmen_df = pd.DataFrame()
        self.query_db()
        self.game_linesmen_df = self.game_linesmen_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_linesmen_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from "

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select id, gameId, linesmanId from puckpandas.game_linesmen"
        game_linesmen_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_linesmen_df.size > 0:
            game_linesmen_df = game_linesmen_df.reindex(columns=self.table_columns)
            game_linesmen_df.infer_objects().fillna('', inplace=True)
            game_linesmen_df.drop_duplicates(inplace=True)
            self.game_linesmen_df = game_linesmen_df

        return self.game_linesmen_df
