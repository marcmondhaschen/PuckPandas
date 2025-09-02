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

    def update_db(self, season_id=0):
        if self.shift_goals_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.shift_goals (gameId, eventNumber, detailCode, teamId, playerId, period, 
                goalTimeSeconds, eventDescription, eventDetails, typeCode) select s.gameId, s.eventNumber, s.detailCode, 
                s.teamId, s.playerId, s.period, time_to_sec(left(s.endTime, locate(':', s.endTime)+2))/60 as 
                goalTimeSeconds, s.eventDescription, s.eventDetails, s.typeCode from puckpandas_import.shifts_import 
                as s join puckpandas_import.games_import as g on s.gameId = g.gameId where s.typeCode = 505 and 
                g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.shift_goals (gameId, eventNumber, detailCode, teamId, playerId, period, 
                goalTimeSeconds, eventDescription, eventDetails, typeCode) select s.gameId, s.eventNumber, s.detailCode, 
                s.teamId, s.playerId, s.period, time_to_sec(left(s.endTime, locate(':', s.endTime)+2))/60 as 
                goalTimeSeconds, s.eventDescription, s.eventDetails, s.typeCode from puckpandas_import.shifts_import 
                as s join puckpandas_import.games_import as g on s.gameId = g.gameId where s.typeCode = 505"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.shift_goals"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, gameId, eventNumber, detailCode, teamId, playerId, period, goalTimeSeconds, 
        eventDescription, eventDetails, typeCode from puckpandas.shift_goals"""

        shift_goals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if shift_goals_df.size > 0:
            shift_goals_df = shift_goals_df.reindex(columns=self.table_columns)
            shift_goals_df.infer_objects().fillna('', inplace=True)
            shift_goals_df.drop_duplicates(inplace=True)
            self.shift_goals_df = shift_goals_df

        return self.shift_goals_df
