import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Linesmen:
    def __init__(self):
        self.table_columns = ['linesmanId','linesmanName']
        self.linesmen_df = pd.DataFrame()
        self.query_db()
        self.linesmen_df = self.linesmen_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.linesmen_df.size > 0:
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
        sql = "select linesmanId, linesmanName from puckpandas.linesmen"
        linesmen_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if linesmen_df.size > 0:
            linesmen_df = linesmen_df.reindex(columns=self.table_columns)
            linesmen_df.infer_objects().fillna('', inplace=True)
            linesmen_df.drop_duplicates(inplace=True)
            self.linesmen_df = linesmen_df

        return self.linesmen_df
