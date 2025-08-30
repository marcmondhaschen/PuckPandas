import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Linesmen:
    def __init__(self):
        self.table_columns = ['']
        self.xxxx_df = pd.DataFrame()
        self.query_db()
        self.xxxx_df = self.xxxx_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.xxxx_df.size > 0:
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
        sql = "select "
        xxxx_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if xxxx_df.size > 0:
            xxxx_df = xxxx_df.reindex(columns=self.table_columns)
            xxxx_df.infer_objects().fillna('', inplace=True)
            xxxx_df.drop_duplicates(inplace=True)
            self.xxxx_df = xxxx_df

        return self.xxxx_df
