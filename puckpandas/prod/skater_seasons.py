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
            sql = """insert into puckpandas.skater_seasons (playerId, seasonId, leagueId, teamName, teamId, sequence, 
            gameType, GP, G, A, P, PM, PIM, PPG, PPP, SHG, SHP, TOIGSEC, GWG, OTG, S, SPCT, FOPCT) select a.playerId, 
            a.season as seasonId, b.leagueId, a.`teamName.default` as teamName, c.teamId, a.sequence, a.gameTypeId as 
            gameType, coalesce(a.gamesPlayed, 0) as GP, coalesce(a.goals, 0) as G, coalesce(a.assists, 0) as A, 
            coalesce(a.points, 0) as P, coalesce(a.plusMinus, 0) as PM, coalesce(a.pim, 0) as PIM, 
            coalesce(a.powerPlayGoals, 0) as PPG, coalesce(a.powerPlayPoints, 0) as PPP, 
            coalesce(a.shorthandedGoals, 0) as SHG, coalesce(a.shorthandedPoints, 0) as SHP, 
            time_to_sec(left(a.avgToi, locate(':', a.avgToi)+2))/60 as TOIGSEC, coalesce(a.gameWinningGoals, 0) as GWG, 
            coalesce(a.otGoals, 0) as OTG, coalesce(a.shots, 0) as S, coalesce(a.shootingPctg, 0) as SPCT, 
            coalesce(a.faceoffWinningPctg, 0) as FOPCT from puckpandas_import.skater_season_import as a join 
            puckpandas.leagues as b on a.leagueAbbrev = b.leagueAbbrev left join (select g.seasonId, t.teamId, 
            t.fullName, count(gameId) as games from puckpandas.game_results as g join puckpandas.teams as t on 
            g.teamId = t.teamId where t.teamId between 1 and 99 and g.gameType = 2 group by g.seasonId, t.teamId) as c 
            on a.season = c.seasonId and a.`teamName.default` = c.fullName where 
            a.season = """ + str(self.current_season)

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
