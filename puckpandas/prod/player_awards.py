import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayerAwards:
    def __init__(self):
        self.table_columns = ['id','playerId','seasonId','trophyId']
        self.player_awards_df = pd.DataFrame()
        self.query_db()
        self.player_awards_df = self.player_awards_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.player_awards_df.size > 0:
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
        sql = "select id, playerId, seasonId, trophyId from puckpandas.player_awards"
        player_awards_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_awards_df.size > 0:
            player_awards_df = player_awards_df.reindex(columns=self.table_columns)
            player_awards_df.infer_objects().fillna('', inplace=True)
            player_awards_df.drop_duplicates(inplace=True)
            self.player_awards_df = player_awards_df

        return self.player_awards_df
