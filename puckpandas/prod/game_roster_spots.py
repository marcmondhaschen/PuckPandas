import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameRosterSpots:
    def __init__(self):
        self.table_columns = ['id','gameId','teamId','playerId','sweaterNumber','positionCode']
        self.game_roster_spots_df = pd.DataFrame()
        self.query_db()
        self.game_roster_spots_df = self.game_roster_spots_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_roster_spots_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_roster_spots"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select id, gameId, teamId, playerId, sweaterNumber, positionCode from puckpandas.game_roster_spots"
        game_roster_spots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_roster_spots_df.size > 0:
            game_roster_spots_df = game_roster_spots_df.reindex(columns=self.table_columns)
            game_roster_spots_df.infer_objects().fillna('', inplace=True)
            game_roster_spots_df.drop_duplicates(inplace=True)
            self.game_roster_spots_df = game_roster_spots_df

        return self.game_roster_spots_df
