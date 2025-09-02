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

    def update_db(self, season_id=0):
        if self.game_shots_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_shots (playId, gameId, eventId, sortOrder, typeCode, reason, 
                shotType, shootingPlayerId, blockingPlayerId, goalieInNetId, awaySOG, homeSOG) select a.playId, 
                b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.reason` as reason, b.`details.shotType` 
                as shotType, b.`details.shootingPlayerId` as shootingPlayerId, b.`details.blockingPlayerId` as 
                blockingPlayerId, b.`details.goalieInNetId` as goalieInNetId, b.`details.awaySOG` as awaySOG, 
                b.`details.homeSOG` as homeSOG from puckpandas.plays as a join puckpandas_import.games_import as g on 
                a.gameId = g.gameId join puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = 
                b.eventId where b.typeCode in ('506', '507', '538', '537') and g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_shots (playId, gameId, eventId, sortOrder, typeCode, reason, 
                shotType, shootingPlayerId, blockingPlayerId, goalieInNetId, awaySOG, homeSOG) select a.playId, 
                b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.reason` as reason, b.`details.shotType` 
                as shotType, b.`details.shootingPlayerId` as shootingPlayerId, b.`details.blockingPlayerId` as 
                blockingPlayerId, b.`details.goalieInNetId` as goalieInNetId, b.`details.awaySOG` as awaySOG, 
                b.`details.homeSOG` as homeSOG from puckpandas.plays as a join puckpandas_import.games_import as g on 
                a.gameId = g.gameId join puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = 
                b.eventId where b.typeCode in ('506', '507', '538', '537')"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_shots"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playId, gameId, eventId, sortOrder, typeCode, reason, shotType, shootingPlayerId, 
        blockingPlayerId, goalieInNetId, awaySOG, homeSOG from puckpandas.gameshots"""
        game_shots_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_shots_df.size > 0:
            game_shots_df = game_shots_df.reindex(columns=self.table_columns)
            game_shots_df.infer_objects().fillna('', inplace=True)
            game_shots_df.drop_duplicates(inplace=True)
            self.game_shots_df = game_shots_df

        return self.game_shots_df
