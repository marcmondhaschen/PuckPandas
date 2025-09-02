import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Leagues:
    def __init__(self):
        self.table_columns = ['leagueId','leagueAbbrev']
        self.leagues_df = pd.DataFrame()
        self.query_db()
        self.leagues_df = self.leagues_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.leagues_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.leagues (leagueAbbrev) select distinct leagueAbbrev from 
            puckpandas_import.skater_season_import order by leagueAbbrev"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.leagues"""

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select leagueId, leagueAbbrev from puckpandas.leagues"""
        leagues_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if leagues_df.size > 0:
            leagues_df = leagues_df.reindex(columns=self.table_columns)
            leagues_df.infer_objects().fillna('', inplace=True)
            leagues_df.drop_duplicates(inplace=True)
            self.leagues_df = leagues_df

        return self.leagues_df
