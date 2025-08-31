import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class Shifts:
    def __init__(self):
        self.table_columns = ['id','gameId','eventNumber','detailCode','teamId','playerId','shiftNumber','period',
                              'startTimeSeconds','endTimeSeconds','durationSeconds','typeCode']
        self.shifts_df = pd.DataFrame()
        self.query_db()
        self.shifts_df = self.shifts_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.shifts_df.size > 0:
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
        sql = "select id, gameId, eventNumber, detailCode, teamId, playerId, shiftNumber, period, startTimeSeconds, " \
              "endTimeSeconds, durationSeconds, typeCode from puckpandas.shifts"
        shifts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if shifts_df.size > 0:
            shifts_df = shifts_df.reindex(columns=self.table_columns)
            shifts_df.infer_objects().fillna('', inplace=True)
            shifts_df.drop_duplicates(inplace=True)
            self.shifts_df = shifts_df

        return self.shifts_df
