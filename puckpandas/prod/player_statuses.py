import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayerStatuses:
    def __init__(self):
        self.table_columns = ['playerId','isActive','currentTeamId','currentTeamAbbrev','sweaterNumber','position',
                              'inTop100AllTime','inHHOF']
        self.player_statuses_df = pd.DataFrame()
        self.query_db()
        self.player_statuses_df = self.player_statuses_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.player_statuses_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.player_statuses (playerId, isActive, currentTeamId, currentTeamAbbrev, 
            sweaterNumber, position, inTop100AllTime, inHHOF) select playerId, isActive, currentTeamId, 
            currentTeamAbbrev, sweaterNumber, position, inTop100AllTime, inHHOF from 
            puckpandas_import.player_bios_import"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.player_statuses"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playerId, isActive, currentTeamId, currentTeamAbbrev, sweaterNumber, position, " \
              "inTop100AllTime, inHHOF from puckpandas.player_statuses"
        player_statuses_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_statuses_df.size > 0:
            player_statuses_df = player_statuses_df.reindex(columns=self.table_columns)
            player_statuses_df.infer_objects().fillna('', inplace=True)
            player_statuses_df.drop_duplicates(inplace=True)
            self.player_statuses_df = player_statuses_df

        return self.player_statuses_df
