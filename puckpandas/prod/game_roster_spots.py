import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameRosterSpots:
    def __init__(self):
        self.table_columns = ['id','gameId','teamId','playerId','sweaterNumber','positionCode']
        self.game_roster_spots_df = pd.DataFrame()
        self.query_db()
        self.game_roster_spots_df = self.game_roster_spots_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_roster_spots_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_roster_spots (gameId, teamId, playerId, sweaterNumber, 
                positionCode) select r.gameId, r.teamId, r.playerId, r.sweaterNumber, r.positionCode from 
                puckpandas_import.roster_spots_import as r  join puckpandas_import.games_import as g on r.gameId = 
                g.gameId where g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_roster_spots (gameId, teamId, playerId, sweaterNumber, 
                positionCode) select r.gameId, r.teamId, r.playerId, r.sweaterNumber, r.positionCode from 
                puckpandas_import.roster_spots_import as r  join puckpandas_import.games_import as g on r.gameId = 
                g.gameId"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_roster_spots"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, gameId, teamId, playerId, sweaterNumber, positionCode from puckpandas.game_roster_spots"""
        game_roster_spots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_roster_spots_df.size > 0:
            game_roster_spots_df = game_roster_spots_df.reindex(columns=self.table_columns)
            game_roster_spots_df.infer_objects().fillna('', inplace=True)
            game_roster_spots_df.drop_duplicates(inplace=True)
            self.game_roster_spots_df = game_roster_spots_df

        return self.game_roster_spots_df
