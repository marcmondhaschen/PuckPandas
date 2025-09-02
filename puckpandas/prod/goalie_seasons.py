import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GoalieSeasons:
    def __init__(self):
        self.table_columns = ['id','playerId','seasonId','leagueId','teamName','teamId','sequence','gameType','GP',
                              'GS','G','A','PIM','W','L','OTL','ties','SA','GA','GAA','SPCT','SO','TOISEC']
        self.goalie_seasons_df = pd.DataFrame()
        self.query_db()
        self.goalie_seasons_df = self.goalie_seasons_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.goalie_seasons_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.goalie_seasons (playerId, seasonId, leagueId, teamName, teamId, 
                sequence, gameType, GP, GS, G, A, PIM, W, L, OTL, `ties`, SA, GA, GAA, SPCT, SO, TOISEC) select 
                a.playerId, a.`season` as seasonId, b.`leagueId`, a.`teamName.default` as teamName, b.teamId, 
                a.`sequence`, a.`gameTypeId` as gameType, a.`gamesPlayed` as GP, a.`gamesStarted` as GS, a.`goals` as G, 
                a.`assists` as A, a.`pim` as PIM, a.`wins` as W, a.`losses` as L, a.`otLosses` as OTL, a.`ties`, 
                a.`shotsAgainst` as SA, a.`goalsAgainst` as GA, a.`goalsAgainstAvg` as GAA, a.`savePctg` as SPCT, 
                a.`shutouts` as SO, a.`timeOnIceSeconds` as TOISEC from puckpandas_import.goalie_season_import as a 
                join puckpandas.leagues as b on a.leagueAbbrev = b.leagueAbbrev left join (select g.seasonId, t.teamId, 
                t.fullName, count(gameId) as games from puckpandas.game_results as g join puckpandas.teams as t on 
                g.teamId = t.teamId where t.teamId between 1 and 99 and g.gameType = 2 group by g.seasonId, 
                t.teamId) as b on a.season = b.seasonId and a.`teamName.default` = b.fullName where 
                a.`season` = """ + str(season_id)
            else:
                sql = """insert into puckpandas.goalie_seasons (playerId, seasonId, leagueId, teamName, teamId, 
                sequence, gameType, GP, GS, G, A, PIM, W, L, OTL, `ties`, SA, GA, GAA, SPCT, SO, TOISEC) select 
                a.playerId, a.`season` as seasonId, b.`leagueId`, a.`teamName.default` as teamName, b.teamId, 
                a.`sequence`, a.`gameTypeId` as gameType, a.`gamesPlayed` as GP, a.`gamesStarted` as GS, a.`goals` as G, 
                a.`assists` as A, a.`pim` as PIM, a.`wins` as W, a.`losses` as L, a.`otLosses` as OTL, a.`ties`, 
                a.`shotsAgainst` as SA, a.`goalsAgainst` as GA, a.`goalsAgainstAvg` as GAA, a.`savePctg` as SPCT, 
                a.`shutouts` as SO, a.`timeOnIceSeconds` as TOISEC from puckpandas_import.goalie_season_import as a 
                join puckpandas.leagues as b on a.leagueAbbrev = b.leagueAbbrev left join (select g.seasonId, t.teamId, 
                t.fullName, count(gameId) as games from puckpandas.game_results as g join puckpandas.teams as t on 
                g.teamId = t.teamId where t.teamId between 1 and 99 and g.gameType = 2 group by g.seasonId, 
                t.teamId) as b on a.season = b.seasonId and a.`teamName.default` = b.fullName"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.goalie_seasons"""

        if season_id != 0:
            sql = """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select id, playerId, seasonId, leagueId, teamName, teamId, sequence, gameType, GP, GS, G, A, PIM, W, 
        L, OTL, ties, SA, GA, GAA, SPCT, SO, TOISEC from puckpandas.goalie_seasons"""

        goalie_seasons_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_seasons_df.size > 0:
            goalie_seasons_df = goalie_seasons_df.reindex(columns=self.table_columns)
            goalie_seasons_df.infer_objects().fillna('', inplace=True)
            goalie_seasons_df.drop_duplicates(inplace=True)
            self.goalie_seasons_df = goalie_seasons_df

        return self.goalie_seasons_df
