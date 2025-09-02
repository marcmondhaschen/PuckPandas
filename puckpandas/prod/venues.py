import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class Venues:
    def __init__(self):
        self.table_columns = ['venueId', 'venue']
        self.venues_df = pd.DataFrame()
        self.query_db()
        self.venues_df = self.venues_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.venues_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into `puckpandas`.`venues` (venue) select distinct venue as venueName from 
            puckpandas_import.games_import order by venue"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
            engine = pp.dba_prod_login()
            sql = """delete from puckpandas.venues"""

            with engine.connect() as conn:
                conn.execute(text(sql))
            engine.dispose()

            return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select venueId, venue from puckpandas.venues"""
        venues_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if venues_df.size > 0:
            venues_df = venues_df.reindex(columns=self.table_columns)
            venues_df.infer_objects().fillna('', inplace=True)
            venues_df.drop_duplicates(inplace=True)
            self.venues_df = venues_df

        return self.venues_df
