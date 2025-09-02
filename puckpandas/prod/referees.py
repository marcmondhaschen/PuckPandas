import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Referees:
    def __init__(self):
        self.table_columns = ['refereeId','refereeName']
        self.referees_df = pd.DataFrame()
        self.query_db()
        self.referees_df = self.referees_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.referees_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.referees (refereeName) select distinct `default` as refereeName from 
            puckpandas_import.referees_import"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.referees"""

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select refereeId, refereeName from puckpandas.referees"""

        referees_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if referees_df.size > 0:
            referees_df = referees_df.reindex(columns=self.table_columns)
            referees_df.infer_objects().fillna('', inplace=True)
            referees_df.drop_duplicates(inplace=True)
            self.referees_df = referees_df

        return self.referees_df
