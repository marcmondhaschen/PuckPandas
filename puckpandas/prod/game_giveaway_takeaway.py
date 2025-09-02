import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameGiveawayTakeaway:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','playerId','typeCode']
        self.game_giveaway_takeaway_df = pd.DataFrame()
        self.query_db()
        self.game_giveaway_takeaway_df = self.game_giveaway_takeaway_df.reindex(columns=self.table_columns)


    def update_db(self, season_id=0):
        if self.game_giveaway_takeaway_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_giveaway_takeaway (playId, gameId, eventId, sortOrder, playerId, 
                typeCode) select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.playerId` as playerId, 
                b.typeCode from puckpandas.plays as a join puckpandas_import.games_import as g on a.gameId = g.gameId 
                join puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId where 
                b.typeCode in ('504', '525') and g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_giveaway_takeaway (playId, gameId, eventId, sortOrder, playerId, 
                typeCode) select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.playerId` as playerId, 
                b.typeCode from puckpandas.plays as a join puckpandas_import.games_import as g on a.gameId = g.gameId 
                join puckpandas_import.plays_import as b on a.gameId = b.gameId and a.eventId = b.eventId where 
                b.typeCode in ('504', '525')"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_giveaway_takeaway"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playId, gameId, eventId, sortOrder, playerId, typeCode from puckpandas.game_giveaway_takeaway"""
        game_giveaway_takeaway_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_giveaway_takeaway_df.size > 0:
            game_giveaway_takeaway_df = game_giveaway_takeaway_df.reindex(columns=self.table_columns)
            game_giveaway_takeaway_df.infer_objects().fillna('', inplace=True)
            game_giveaway_takeaway_df.drop_duplicates(inplace=True)
            self.game_giveaway_takeaway_df = game_giveaway_takeaway_df

        return self.game_giveaway_takeaway_df
