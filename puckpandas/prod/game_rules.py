import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameRules:
    def __init__(self):
        self.table_columns = ['']
        self.game_rules_df = pd.DataFrame()
        self.query_db()
        self.game_rules_df = self.game_rules_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_rules_df.size > 0:
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
        sql = "select "
        game_rules_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_rules_df.size > 0:
            game_rules_df = game_rules_df.reindex(columns=self.table_columns)
            game_rules_df.infer_objects().fillna('', inplace=True)
            game_rules_df.drop_duplicates(inplace=True)
            self.game_rules_df = game_rules_df

        return self.game_rules_df
