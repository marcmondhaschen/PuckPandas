import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameSeriesGroups:
    def __init__(self):
        self.table_columns = ['gameId','seriesNumber','refGameId']
        self.game_series_groups_df = pd.DataFrame()
        self.query_db()
        self.game_series_groups_df = self.game_series_groups_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_series_groups_df.size > 0:
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
        sql = "select gameId, seriesNumber, refGameId from puckpandas.game_series_groups"
        game_series_groups_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_series_groups_df.size > 0:
            game_series_groups_df = game_series_groups_df.reindex(columns=self.table_columns)
            game_series_groups_df.infer_objects().fillna('', inplace=True)
            game_series_groups_df.drop_duplicates(inplace=True)
            self.game_series_groups_df = game_series_groups_df

        return self.game_series_groups_df
