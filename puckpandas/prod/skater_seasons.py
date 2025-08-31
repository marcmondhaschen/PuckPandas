import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class SkaterSeasons:
    def __init__(self):
        self.table_columns = ['id','playerId','seasonId','leagueId','teamName','teamId','sequence','gameType','GP','G',
                              'A','P','PM','PIM','PPG','PPP','SHG','SHP','TOIGSEC','GWG','OTG','S','SPCT','FOPCT']
        self.skater_seasons_df = pd.DataFrame()
        self.query_db()
        self.skater_seasons_df = self.skater_seasons_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.skater_seasons_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.skater_seasons"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select id, playerId, seasonId, leagueId, teamName, teamId, sequence, gameType, GP, G, A, P, PM, PIM, " \
              "PPG, PPP, SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, FOPCT from puckpandas.skater_seasons"
        skater_seasons_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_seasons_df.size > 0:
            skater_seasons_df = skater_seasons_df.reindex(columns=self.table_columns)
            skater_seasons_df.infer_objects().fillna('', inplace=True)
            skater_seasons_df.drop_duplicates(inplace=True)
            self.skater_seasons_df = skater_seasons_df

        return self.skater_seasons_df
