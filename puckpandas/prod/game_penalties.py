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

    def update_db(self, season_id=0):
        if self.game_penalties_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_penalties (playId, gameId, eventId, sortOrder, typeCode, 
                penaltyTypeCode, penaltyDescKey, penaltyDuration, committedByPlayerId, drawnByPlayerId) select 
                a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.typeCode` as penaltyTypeCode, 
                b.`details.descKey` as penaltyDescKey, b.`details.duration` as duration, 
                b.`details.committedByPlayerId` as committedByPlayerId, b.`details.drawnByPlayerId` as drawnByPlayerId 
                from puckpandas.plays as a  join puckpandas_import.games_import as g on a.gameId = g.gameId join 
                puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode 
                in ('509', '535') and g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_penalties (playId, gameId, eventId, sortOrder, typeCode, 
                penaltyTypeCode, penaltyDescKey, penaltyDuration, committedByPlayerId, drawnByPlayerId) select 
                a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode, b.`details.typeCode` as penaltyTypeCode, 
                b.`details.descKey` as penaltyDescKey, b.`details.duration` as duration, 
                b.`details.committedByPlayerId` as committedByPlayerId, b.`details.drawnByPlayerId` as drawnByPlayerId 
                from puckpandas.plays as a join puckpandas_import.games_import as g on a.gameId = g.gameId join 
                puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode 
                in ('509', '535')"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_penalties"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playId, gameId, eventId, sortOrder, typeCode, penaltyTypeCode, penaltyDescKey, penaltyDuration, 
        committedByPlayerId, drawnByPlayerId from puckpandas.game_penalties"""

        game_penalties_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_penalties_df.size > 0:
            game_penalties_df = game_penalties_df.reindex(columns=self.table_columns)
            game_penalties_df.infer_objects().fillna('', inplace=True)
            game_penalties_df.drop_duplicates(inplace=True)
            self.game_penalties_df = game_penalties_df

        return self.game_penalties_df
