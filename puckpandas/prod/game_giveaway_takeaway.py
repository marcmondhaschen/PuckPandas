import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameGiveawayTakeaway:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','playerId','typeCode']
        self.game_giveaway_takeaway_df = pd.DataFrame()
        self.query_db()
        self.game_giveaway_takeaway_df = self.game_giveaway_takeaway_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_giveaway_takeaway_df.size > 0:
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
        sql = "select playId, gameId, eventId, sortOrder, playerId, typeCode from puckpandas.game_giveaway_takeaway"
        game_giveaway_takeaway_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_giveaway_takeaway_df.size > 0:
            game_giveaway_takeaway_df = game_giveaway_takeaway_df.reindex(columns=self.table_columns)
            game_giveaway_takeaway_df.infer_objects().fillna('', inplace=True)
            game_giveaway_takeaway_df.drop_duplicates(inplace=True)
            self.game_giveaway_takeaway_df = game_giveaway_takeaway_df

        return self.game_giveaway_takeaway_df
