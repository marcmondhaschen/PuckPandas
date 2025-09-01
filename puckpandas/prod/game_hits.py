import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameHits:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','hittingPlayerId','hitteePlayerId']
        self.game_hits_df = pd.DataFrame()
        self.query_db()
        self.game_hits_df = self.game_hits_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_hits_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_hits (playId, gameId, eventId, sortOrder, hittingPlayerId, " \
                  "hitteePlayerId) select a.playId, b.gameId, b.eventId, b.sortOrder, b.`details.hittingPlayerId` " \
                  "as hittingPlayerId, b.`details.hitteePlayerId` as hitteePlayerId  from puckpandas.plays as a join " \
                  "puckpandas_import.games_import as g on a.gameId = g.gameId  join puckpandas_import.plays_import " \
                  "as b on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode = '503' and " \
                  "g.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_hits"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playId, gameId, eventId, sortOrder, hittingPlayerId, hitteePlayerId from puckpandas.game_hits"
        game_hits_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_hits_df.size > 0:
            game_hits_df = game_hits_df.reindex(columns=self.table_columns)
            game_hits_df.infer_objects().fillna('', inplace=True)
            game_hits_df.drop_duplicates(inplace=True)
            self.game_hits_df = game_hits_df

        return self.game_hits_df
