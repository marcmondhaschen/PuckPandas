import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class GameProgress:
    def __init__(self):
        self.table_columns = ['gameId', 'gameState', 'gameScheduleState', 'periodNumber', 'periodType',
                              'secondsRemaining', 'clockRunning', 'inIntermission', 'maxPeriods', 'lastPeriodType',
                              'regPeriods']
        self.game_progress_df = pd.DataFrame()
        self.query_db()
        self.game_progress_df = self.game_progress_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_progress_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_progress (gameId, gameState, gameScheduleState, periodNumber, " \
                  "periodType, secondsRemaining, clockRunning, inIntermission, maxPeriods, lastPeriodType, " \
                  "regPeriods) select a.gameId, a.gameState, a.gameScheduleState, b.`periodDescriptor.number` as " \
                  "periodNumber, b.`periodDescriptor.periodType` as periodType, b.`clock.secondsRemaining` as " \
                  "secondsRemaining, b.`clock.running` as clockRunning, b.`clock.inIntermission` as inIntermission, " \
                  "b.maxPeriods, b.`gameOutcome.lastPeriodType` as lastPeriodType, b.regPeriods from " \
                  "puckpandas_import.games_import as a join puckpandas_import.game_center_import as b on " \
                  "a.gameId = b.gameId where a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_progress"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select gameId, gameState, gameScheduleState, periodNumber, periodType, secondsRemaining, " \
              "clockRunning, inIntermission, maxPeriods, lastPeriodType, regPeriods from puckpandas.game_progress"
        game_progress_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_progress_df.size > 0:
            game_progress_df = game_progress_df.reindex(columns=self.table_columns)
            game_progress_df.infer_objects().fillna('', inplace=True)
            game_progress_df.drop_duplicates(inplace=True)
            self.game_progress_df = game_progress_df

        return self.game_progress_df
