import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameVideos:
    def __init__(self):
        self.table_columns = ['gameId','threeMinRecap']
        self.game_videos_df = pd.DataFrame()
        self.query_db()
        self.game_videos_df = self.game_videos_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_videos_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_videos (gameId, threeMinRecap) select r.gameId, case when 
                r.`gameVideo.threeMinRecap` = '0' then '' else r.`gameVideo.threeMinRecap` end as threeMinRecap from 
                puckpandas_import.game_center_right_rail_import as r join puckpandas_import.games_import as g on 
                g.gameId = r.gameId where g.seasonId = """ + str(season_id)
            else:
                sql = """insert into puckpandas.game_videos (gameId, threeMinRecap) select r.gameId, case when 
                r.`gameVideo.threeMinRecap` = '0' then '' else r.`gameVideo.threeMinRecap` end as threeMinRecap from 
                puckpandas_import.game_center_right_rail_import as r join puckpandas_import.games_import as g on 
                g.gameId = r.gameId"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_videos"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select gameId, threeMinRecap from puckpandas.game_videos"""
        game_videos_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_videos_df.size > 0:
            game_videos_df = game_videos_df.reindex(columns=self.table_columns)
            game_videos_df.infer_objects().fillna('', inplace=True)
            game_videos_df.drop_duplicates(inplace=True)
            self.game_videos_df = game_videos_df

        return self.game_videos_df
