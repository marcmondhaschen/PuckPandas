import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class DivisionConference:
    def __init__(self):
        self.table_columns = ['id','seasonId','teamId','fullName','era','conference','division']
        self.division_conference_df = pd.DataFrame()
        self.query_db()
        self.division_conference_df = self.division_conference_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.division_conference_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.division_conference"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select id, seasonId, teamId, fullName, era, conference, division from puckpandas.division_conference"
        division_conference_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if division_conference_df.size > 0:
            division_conference_df = division_conference_df.reindex(columns=self.table_columns)
            division_conference_df.infer_objects().fillna('', inplace=True)
            division_conference_df.drop_duplicates(inplace=True)
            self.division_conference_df = division_conference_df

        return self.division_conference_df
