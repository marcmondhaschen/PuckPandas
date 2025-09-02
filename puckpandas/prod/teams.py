import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Teams:
    def __init__(self):
        self.table_columns = ['teamId','triCode','fullName','commonName','placeName']
        self.teams_df = pd.DataFrame()
        self.query_db()
        self.teams_df = self.teams_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.teams_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.teams (teamId, triCode, fullName, commonName, placeName) select distinct 
            `awayTeam.id` as teamId, `awayTeam.abbrev` as triCode, concat(`awayTeam.placeName.default`, ' ', 
            `awayTeam.commonName.default`) as fullName, `awayTeam.commonName.default` as commonName, 
            `awayTeam.placeName.default` as placeName from puckpandas_import.game_center_import union select 
            `homeTeam.id` as teamId, `homeTeam.abbrev` as triCode, concat(`homeTeam.placeName.default`, ' ', 
            `homeTeam.commonName.default`) as fullName, `homeTeam.commonName.default` as commonName, 
            `homeTeam.placeName.default` as placeName from puckpandas_import.game_center_import"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.teams"""

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select teamId, triCode, fullName, commonName, placeName from puckpandas.teams"""
        teams_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if teams_df.size > 0:
            teams_df = teams_df.reindex(columns=self.table_columns)
            teams_df.infer_objects().fillna('', inplace=True)
            teams_df.drop_duplicates(inplace=True)
            self.teams_df = teams_df

        return self.teams_df
