import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameCareerTotals:
    def __init__(self):
        self.table_columns = ['']
        self.goalie_career_totals_df = pd.DataFrame()
        self.query_db()
        self.goalie_career_totals_df = self.goalie_career_totals_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.goalie_career_totals_df.size > 0:
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
        goalie_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.infer_objects().fillna('', inplace=True)
            goalie_career_totals_df.drop_duplicates(inplace=True)
            self.goalie_career_totals_df = goalie_career_totals_df

        return self.goalie_career_totals_df
