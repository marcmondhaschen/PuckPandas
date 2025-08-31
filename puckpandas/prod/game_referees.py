import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameReferees:
    def __init__(self):
        self.table_columns = ['id','gameId','refereeId']
        self.game_referees_df = pd.DataFrame()
        self.query_db()
        self.game_referees_df = self.game_referees_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_referees_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "select "

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = ""
        game_referees_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_referees_df.size > 0:
            game_referees_df = game_referees_df.reindex(columns=self.table_columns)
            game_referees_df.infer_objects().fillna('', inplace=True)
            game_referees_df.drop_duplicates(inplace=True)
            self.game_referees_df = game_referees_df

        return self.game_referees_df