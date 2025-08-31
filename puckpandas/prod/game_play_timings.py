import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GamePlayTimings:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','periodNumber','periodType','maxRegulationPeriods',
                              'secondsInPeriod','secondsRemaining','sortOrder']
        self.game_play_timings_df = pd.DataFrame()
        self.query_db()
        self.game_play_timings_df = self.game_play_timings_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_play_timings_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_play_timings"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playId, gameId, eventId, periodNumber, periodType, maxRegulationPeriods, secondsInPeriod, " \
              "secondsRemaining, sortOrder from puckpandas.game_play_timings"
        game_play_timings_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_play_timings_df.size > 0:
            game_play_timings_df = game_play_timings_df.reindex(columns=self.table_columns)
            game_play_timings_df.infer_objects().fillna('', inplace=True)
            game_play_timings_df.drop_duplicates(inplace=True)
            self.game_play_timings_df = game_play_timings_df

        return self.game_play_timings_df
