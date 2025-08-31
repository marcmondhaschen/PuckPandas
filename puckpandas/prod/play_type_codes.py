import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class PlayTypeCodes:
    def __init__(self):
        self.table_columns = ['typeCode','typeDescKey']
        self.play_type_codes_df = pd.DataFrame()
        self.query_db()
        self.play_type_codes_df = self.play_type_codes_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.play_type_codes_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.play_type_codes"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select typeCode, typeDescKey from puckpandas.play_type_codes"
        play_type_codes_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if play_type_codes_df.size > 0:
            play_type_codes_df = play_type_codes_df.reindex(columns=self.table_columns)
            play_type_codes_df.infer_objects().fillna('', inplace=True)
            play_type_codes_df.drop_duplicates(inplace=True)
            self.play_type_codes_df = play_type_codes_df

        return self.play_type_codes_df
