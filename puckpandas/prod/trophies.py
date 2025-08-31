import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Trophies:
    def __init__(self):
        self.table_columns = ['trophyId','trophyName']
        self.trophies_df = pd.DataFrame()
        self.query_db()
        self.trophies_df = self.trophies_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.trophies_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.trophies"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select trophyId, trophyName from puckpandas.trophies"
        trophies_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if trophies_df.size > 0:
            trophies_df = trophies_df.reindex(columns=self.table_columns)
            trophies_df.infer_objects().fillna('', inplace=True)
            trophies_df.drop_duplicates(inplace=True)
            self.trophies_df = trophies_df

        return self.trophies_df
