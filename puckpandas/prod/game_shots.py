import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameShots:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','typeCode','reason','shotType',
                              'shootingPlayerId','blockingPlayerId','goalieInNetId','awaySOG','homeSOG']
        self.game_shots_df = pd.DataFrame()
        self.query_db()
        self.game_shots_df = self.game_shots_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_shots_df.size > 0:
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
        sql = "select playId, gameId, eventId, sortOrder, typeCode, reason, shotType, shootingPlayerId, " \
              "blockingPlayerId, goalieInNetId, awaySOG, homeSOG from puckpandas.gameshots"
        game_shots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_shots_df.size > 0:
            game_shots_df = game_shots_df.reindex(columns=self.table_columns)
            game_shots_df.infer_objects().fillna('', inplace=True)
            game_shots_df.drop_duplicates(inplace=True)
            self.game_shots_df = game_shots_df

        return self.game_shots_df
