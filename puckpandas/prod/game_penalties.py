import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GamePenalties:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','typeCode','penaltyTypeCode','penaltyDescKey',
                              'penaltyDuration','committedByPlayerId','drawnByPlayerId']
        self.game_penalties_df = pd.DataFrame()
        self.query_db()
        self.game_penalties_df = self.game_penalties_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_penalties_df.size > 0:
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
        game_penalties_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_penalties_df.size > 0:
            game_penalties_df = game_penalties_df.reindex(columns=self.table_columns)
            game_penalties_df.infer_objects().fillna('', inplace=True)
            game_penalties_df.drop_duplicates(inplace=True)
            self.game_penalties_df = game_penalties_df

        return self.game_penalties_df
