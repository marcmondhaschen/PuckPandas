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

    def update_db(self, season_id=0):
        if self.game_play_timings_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_play_timings (playId, gameId, eventId, periodNumber, periodType, 
                maxRegulationPeriods, secondsInPeriod, secondsRemaining, sortOrder) select a.playId, b.gameId, 
                b.eventId, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
                time_to_sec(left(b.timeInPeriod, locate(':', b.timeInPeriod)+2))/60 as secondsInPeriod, 
                time_to_sec(left(b.timeRemaining, locate(':', b.timeRemaining)+2))/60 as secondsRemaining, 
                b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, b.sortOrder from puckpandas.plays 
                as a join puckpandas_import.games_import as g on a.gameId = g.gameId join 
                puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId where 
                g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_play_timings (playId, gameId, eventId, periodNumber, periodType, 
                maxRegulationPeriods, secondsInPeriod, secondsRemaining, sortOrder) select a.playId, b.gameId, 
                b.eventId, b.`periodDescriptor.number` as periodNumber, b.`periodDescriptor.periodType` as periodType, 
                time_to_sec(left(b.timeInPeriod, locate(':', b.timeInPeriod)+2))/60 as secondsInPeriod, 
                time_to_sec(left(b.timeRemaining, locate(':', b.timeRemaining)+2))/60 as secondsRemaining, 
                b.`periodDescriptor.maxRegulationPeriods` as maxRegulationPeriods, b.sortOrder from puckpandas.plays 
                as a join puckpandas_import.games_import as g on a.gameId = g.gameId join 
                puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_play_timings"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playId, gameId, eventId, periodNumber, periodType, maxRegulationPeriods, secondsInPeriod, 
        secondsRemaining, sortOrder from puckpandas.game_play_timings"""

        game_play_timings_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_play_timings_df.size > 0:
            game_play_timings_df = game_play_timings_df.reindex(columns=self.table_columns)
            game_play_timings_df.infer_objects().fillna('', inplace=True)
            game_play_timings_df.drop_duplicates(inplace=True)
            self.game_play_timings_df = game_play_timings_df

        return self.game_play_timings_df
