import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Teams:
    def __init__(self):
        self.table_columns = ['teamId','triCode','fullName','commonName','placeName']
        self.teams_df = pd.DataFrame()
        self.query_db()
        self.teams_df = self.teams_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.teams_df.size > 0:
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
        sql = "select teamId, triCode, fullName, commonName, placeName from puckpandas.teams"
        teams_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if teams_df.size > 0:
            teams_df = teams_df.reindex(columns=self.table_columns)
            teams_df.infer_objects().fillna('', inplace=True)
            teams_df.drop_duplicates(inplace=True)
            self.teams_df = teams_df

        return self.teams_df
