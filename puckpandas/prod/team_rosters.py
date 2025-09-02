import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class TeamRosters:
    def __init__(self):
        self.table_columns = ['id','teamId','seasonId','playerId']
        self.team_rosters_df = pd.DataFrame()
        self.query_db()
        self.team_rosters_df = self.team_rosters_df.reindex(columns=self.table_columns)


    def update_db(self, season_id=0):
        if self.team_rosters_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.team_rosters (teamId, seasonId, playerId) select b.teamId, a.seasonId, 
                a.playerId from puckpandas_import.rosters_import as a join puckpandas_import.teams_import as b on 
                a.triCode = b.triCode where a.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.team_rosters (teamId, seasonId, playerId) select b.teamId, a.seasonId, 
                a.playerId from puckpandas_import.rosters_import as a join puckpandas_import.teams_import as b on 
                a.triCode = b.triCode"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.team_rosters"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, teamId, seasonId, playerId from puckpandas.team_rosters"""

        team_rosters_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if team_rosters_df.size > 0:
            team_rosters_df = team_rosters_df.reindex(columns=self.table_columns)
            team_rosters_df.infer_objects().fillna('', inplace=True)
            team_rosters_df.drop_duplicates(inplace=True)
            self.team_rosters_df = team_rosters_df

        return self.team_rosters_df
