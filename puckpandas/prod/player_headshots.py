import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayerHeadshots:
    def __init__(self):
        self.table_columns = ['headshotId','playerId','headshot']
        self.player_headshots_df = pd.DataFrame()
        self.query_db()
        self.player_headshots_df = self.player_headshots_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.player_headshots_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.player_headshots"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select headshotId, playerId, headshot from puckpandas.player_headshots"
        player_headshots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_headshots_df.size > 0:
            player_headshots_df = player_headshots_df.reindex(columns=self.table_columns)
            player_headshots_df.infer_objects().fillna('', inplace=True)
            player_headshots_df.drop_duplicates(inplace=True)
            self.player_headshots_df = player_headshots_df

        return self.player_headshots_df
