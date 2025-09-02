import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class SkaterCareerTotals:
    def __init__(self):
        self.table_columns = ['playerId','gameType','GP','G','A','P','PM','PIM','PPG','PPP','SHG','SHP','TOIGSEC',
                              'GWG','OTG','S','SPCT','FOPCT']
        self.skater_career_totals_df = pd.DataFrame()
        self.query_db()
        self.skater_career_totals_df = self.skater_career_totals_df.reindex(columns=self.table_columns)

    def update_db(self):
        if self.skater_career_totals_df.size > 0:
            engine = pp.dba_prod_login()
            sql = """insert into puckpandas.skater_career_totals (playerId, gameType, GP, G, A, P, PM, PIM, PPG, PPP, 
            SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, FOPCT) select playerId, 2 as gameType, `regularSeason.gamesPlayed` as 
            GP, `regularSeason.goals` as G, `regularSeason.assists` as A, `regularSeason.points` as P, 
            `regularSeason.plusMinus` as PM, `regularSeason.pim` as PIM, `regularSeason.powerPlayGoals` as PPG, 
            `regularSeason.powerPlayPoints` as PPP, `regularSeason.shorthandedGoals` as SHG, 
            `regularSeason.shorthandedPoints` as SHP, time_to_sec(left(`regularSeason.avgToi`, 
            locate(':', `regularSeason.avgToi`)+2))/60 as TOIGSEC, `regularSeason.gameWinningGoals` as GWG, 
            `regularSeason.otGoals` as OTG, `regularSeason.shots` as S, `regularSeason.shootingPctg` as SPCT, 
            `regularSeason.faceoffWinningPctg` as FOPCT from puckpandas_import.skater_career_totals_import union 
            select playerId, 3 as gameType, `playoffs.gamesPlayed` as GP, `playoffs.goals` as G, 
            `playoffs.assists` as A, `playoffs.points` as P, `playoffs.plusMinus` as PM, `playoffs.pim` as PIM, 
            `playoffs.powerPlayGoals` as PPG, `playoffs.powerPlayPoints` as PPP, `playoffs.shorthandedGoals` as SHG, 
            `playoffs.shorthandedPoints` as SHP, 
            time_to_sec(left(`playoffs.avgToi`, locate(':', `playoffs.avgToi`)+2))/60 as TOIGSEC, 
            `playoffs.gameWinningGoals` as GWG, `playoffs.otGoals` as OTG, `playoffs.shots` as S, 
            `playoffs.shootingPctg` as SPCT, `playoffs.faceoffWinningPctg` as FOPCT from 
            puckpandas_import.skater_career_totals_import where `playoffs.gamesPlayed` > 0"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.skater_career_totals"""

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select playerId, gameType, GP, G, A, P, PM, PIM, PPG, PPP, SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, 
        FOPCT from puckpandas.skater_career_totals"""

        skater_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_career_totals_df.size > 0:
            skater_career_totals_df = skater_career_totals_df.reindex(columns=self.table_columns)
            skater_career_totals_df.infer_objects().fillna('', inplace=True)
            skater_career_totals_df.drop_duplicates(inplace=True)
            self.skater_career_totals_df = skater_career_totals_df

        return self.skater_career_totals_df
