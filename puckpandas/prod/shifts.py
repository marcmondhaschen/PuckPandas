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

    def update_db(self, season_id=0):
        if self.shifts_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.shifts (gameId, eventNumber, detailCode, teamId, playerId, shiftNumber, 
                period, startTimeSeconds, endTimeSeconds, durationSeconds, typeCode) select s.gameId, s.eventNumber, 
                s.detailCode, r.teamId, s.playerId, s.shiftNumber, s.period, 
                time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 as startTimeSeconds, 
                time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 + time_to_sec(left(s.duration, 
                locate(':', s.duration)+2))/60 as endTimeSeconds, time_to_sec(left(s.duration, 
                locate(':', s.duration)+2))/60 as durationSeconds, s.typeCode from puckpandas_import.shifts_import as s 
                join puckpandas_import.games_import as g on s.gameId = g.gameId join 
                puckpandas_import.roster_spots_import as r on s.gameId = r.gameId and s.playerId = r.playerId where 
                s.typeCode = 517 and g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.shifts (gameId, eventNumber, detailCode, teamId, playerId, shiftNumber, 
                period, startTimeSeconds, endTimeSeconds, durationSeconds, typeCode) select s.gameId, s.eventNumber, 
                s.detailCode, r.teamId, s.playerId, s.shiftNumber, s.period, 
                time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 as startTimeSeconds, 
                time_to_sec(left(s.startTime, locate(':', s.startTime)+2))/60 + time_to_sec(left(s.duration, 
                locate(':', s.duration)+2))/60 as endTimeSeconds, time_to_sec(left(s.duration, 
                locate(':', s.duration)+2))/60 as durationSeconds, s.typeCode from puckpandas_import.shifts_import as s 
                join puckpandas_import.games_import as g on s.gameId = g.gameId join 
                puckpandas_import.roster_spots_import as r on s.gameId = r.gameId and s.playerId = r.playerId where 
                s.typeCode = 517"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.shifts"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, gameId, eventNumber, detailCode, teamId, playerId, shiftNumber, period, startTimeSeconds, 
        endTimeSeconds, durationSeconds, typeCode from puckpandas.shifts"""

        shifts_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if shifts_df.size > 0:
            shifts_df = shifts_df.reindex(columns=self.table_columns)
            shifts_df.infer_objects().fillna('', inplace=True)
            shifts_df.drop_duplicates(inplace=True)
            self.shifts_df = shifts_df

        return self.shifts_df
