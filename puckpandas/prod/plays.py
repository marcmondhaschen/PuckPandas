import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Plays:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId']
        self.plays_df = pd.DataFrame()
        self.query_db()
        self.plays_df = self.plays_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.plays_df.size > 0:
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
        sql = "select playId, gameId, eventId from puckpandas.plays"
        plays_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if plays_df.size > 0:
            plays_df = plays_df.reindex(columns=self.table_columns)
            plays_df.infer_objects().fillna('', inplace=True)
            plays_df.drop_duplicates(inplace=True)
            self.plays_df = plays_df

        return self.plays_df
