import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayerBios:
    def __init__(self):
        self.table_columns = ['']
        self.player_bios_df = pd.DataFrame()
        self.query_db()
        self.player_bios_df = self.player_bios_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.player_bios_df.size > 0:
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
        player_bios_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_bios_df.size > 0:
            player_bios_df = player_bios_df.reindex(columns=self.table_columns)
            player_bios_df.infer_objects().fillna('', inplace=True)
            player_bios_df.drop_duplicates(inplace=True)
            self.player_bios_df = player_bios_df

        return self.player_bios_df
