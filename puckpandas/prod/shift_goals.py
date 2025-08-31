import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class ShiftGoals:
    def __init__(self):
        self.table_columns = ['id','gameId','eventNumber','detailCode','teamId','playerId','period','goalTimeSeconds',
                              'eventDescription','eventDetails','typeCode']
        self.shift_goals_df = pd.DataFrame()
        self.query_db()
        self.shift_goals_df = self.shift_goals_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.shift_goals_df.size > 0:
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
        sql = "select id, gameId, eventNumber, detailCode, teamId, playerId, period, goalTimeSeconds, " \
              "eventDescription, eventDetails, typeCode from puckpandas.shift_goals"
        shift_goals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if shift_goals_df.size > 0:
            shift_goals_df = shift_goals_df.reindex(columns=self.table_columns)
            shift_goals_df.infer_objects().fillna('', inplace=True)
            shift_goals_df.drop_duplicates(inplace=True)
            self.shift_goals_df = shift_goals_df

        return self.shift_goals_df
