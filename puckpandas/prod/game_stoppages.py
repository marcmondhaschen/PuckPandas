import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameStoppages:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','typeCode']
        self.game_stoppages_df = pd.DataFrame()
        self.query_db()
        self.game_stoppages_df = self.game_stoppages_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_stoppages_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_stoppages (playId, gameId, eventId, sortOrder, typeCode) select 
                a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode from puckpandas.plays as a join 
                puckpandas_import.games_import as g on a.gameId = g.gameId join puckpandas_import.plays_import as b 
                on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode in ('516', '520', '521', '523', 
                '524') and g.seasonId = """ + str(season_id) + """ order by playId"""
            else:
                sql = """insert into puckpandas.game_stoppages (playId, gameId, eventId, sortOrder, typeCode) select 
                a.playId, b.gameId, b.eventId, b.sortOrder, b.typeCode from puckpandas.plays as a join 
                puckpandas_import.games_import as g on a.gameId = g.gameId join puckpandas_import.plays_import as b 
                on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode in ('516', '520', '521', '523', 
                '524')"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_stoppages"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playId, gameId, eventId, sortOrder, typeCode from puckpandas.game_stoppages"""
        game_stoppages_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_stoppages_df.size > 0:
            game_stoppages_df = game_stoppages_df.reindex(columns=self.table_columns)
            game_stoppages_df.infer_objects().fillna('', inplace=True)
            game_stoppages_df.drop_duplicates(inplace=True)
            self.game_stoppages_df = game_stoppages_df

        return self.game_stoppages_df
