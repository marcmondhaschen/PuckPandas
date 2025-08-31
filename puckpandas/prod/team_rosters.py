import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class TeamRosters:
    def __init__(self):
        self.table_columns = ['id','teamId','seasonId','playerId']
        self.team_rosters_df = pd.DataFrame()
        self.query_db()
        self.team_rosters_df = self.team_rosters_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.team_rosters_df.size > 0:
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
        sql = "select id, teamId, seasonId, playerId from puckpandas.team_rosters"
        team_rosters_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if team_rosters_df.size > 0:
            team_rosters_df = team_rosters_df.reindex(columns=self.table_columns)
            team_rosters_df.infer_objects().fillna('', inplace=True)
            team_rosters_df.drop_duplicates(inplace=True)
            self.team_rosters_df = team_rosters_df

        return self.team_rosters_df
