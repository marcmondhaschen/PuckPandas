import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameCareerTotals:
    def __init__(self):
        self.table_columns = ['playerId','gameType','GP','G','A','PIM','GS','PTS','W','L','OTL','SA','GA','GAA','SPCT',
                              'SO','TOISEC']
        self.goalie_career_totals_df = pd.DataFrame()
        self.query_db()
        self.goalie_career_totals_df = self.goalie_career_totals_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.goalie_career_totals_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.goalie_career_totals (playerId, gameType, GP, G, A, PIM, GS, PTS, W, L, 
            OTL, SA, GA, GAA, SPCT, SO, TOISEC) select playerId, 2 as gameType, `regularSeason.gamesPlayed` as GP, 
            `regularSeason.goals` as G, `regularSeason.assists` as A, `regularSeason.pim` as PIM, 
            `regularSeason.gamesStarted` as GS, `regularSeason.points` as PTS, `regularSeason.wins` as W, 
            `regularSeason.losses` as L, `regularSeason.otLosses` as OTL, `regularSeason.shotsAgainst` as SA, 
            `regularSeason.goalsAgainst` as GA, `regularSeason.goalsAgainstAvg` as GAA, 
            `regularSeason.savePctg` as SPCT, `regularSeason.shutouts` as SO, `regularSeason.timeOnIceSeconds` as 
            TOISEC from puckpandas_import.goalie_career_totals_import union select playerId, 3 as gameType, 
            `playoffs.gamesPlayed` as GP, `playoffs.goals` as G, `playoffs.assists` as A, `playoffs.pim` as PIM, 
            `playoffs.gamesStarted` as GS, `playoffs.points` as PTS, `playoffs.wins` as W, `playoffs.losses` as L, 
            `playoffs.otLosses` as OTL, `playoffs.shotsAgainst` as SA, `playoffs.goalsAgainst` as GA, 
            `playoffs.goalsAgainstAvg` as GAA, `playoffs.savePctg` as SPCT, `playoffs.shutouts` as SO, 
            `playoffs.timeOnIceSeconds` as TOISEC from puckpandas_import.goalie_career_totals_import where 
            playoffs.gamesPlayed > 0"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.goalie_career_totals"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playerId, gameType, GP, G, A, PIM, GS, PTS, W, L, OTL, SA, GA, GAA, SPCT, SO, TOISEC from " \
              "puckpandas.goalie_career_totals"
        goalie_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.infer_objects().fillna('', inplace=True)
            goalie_career_totals_df.drop_duplicates(inplace=True)
            self.goalie_career_totals_df = goalie_career_totals_df

        return self.goalie_career_totals_df
