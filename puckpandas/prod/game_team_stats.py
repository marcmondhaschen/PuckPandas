import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameTeamStats:
    def __init__(self):
        self.table_columns = ['gameId','teamId','sog','faceoffWinningPctg','powerPlay','powerPlayPctg','pim','hits',
                              'blockedShots','giveaways','takeaways']
        self.game_team_stats_df = pd.DataFrame()
        self.query_db()
        self.game_team_stats_df = self.game_team_stats_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_team_stats_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_team_stats (gameId, teamId, sog, faceoffWinningPctg, powerPlay, 
                powerPlayPctg, pim, hits, blockedShots, giveaways, takeaways) select a.gameId, b.awayTeam as teamId, 
                sum(case when a.category = 'sog' then a.awayValue else '' end) as sog, sum(case when a.category = 
                'faceoffWinningPctg' then a.awayValue else '' end) as faceoffWinningPctg, e.awayValue as powerPlay, 
                sum(case when a.category = 'powerPlayPctg' then a.awayValue else '' end) as powerPlayPctg, sum(case 
                when a.category = 'pim' then a.awayValue else '' end) as pim, sum(case when a.category = 'hits' then 
                a.awayValue else '' end) as hits, sum(case when a.category = 'blockedShots' then a.awayValue else '' 
                end) as blockedShots, sum(case when a.category = 'giveaways' then a.awayValue else '' end) as 
                giveaways, sum(case when a.category = 'takeaways' then a.awayValue else '' end) as takeaways from 
                puckpandas_import.team_game_stats_import as a join puckpandas_import.games_import as b on a.gameId = 
                b.gameId join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue from 
                puckpandas_import.team_game_stats_import as c join puckpandas_import.games_import as d on c.gameId = 
                d.gameId where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.awayTeam = e.awayTeam where 
                b.seasonId = @current_season group by a.gameId, b.awayTeam unionselect a.gameId, b.homeTeam as teamId, 
                sum(case when a.category = 'sog' then a.homeValue else '' end) as sog, sum(case when a.category = 
                'faceoffWinningPctg' then a.homeValue else '' end) as faceoffWinningPctg, e.homeValue as powerPlay, 
                sum(case when a.category = 'powerPlayPctg' then a.homeValue else '' end) as powerPlayPctg, sum(case 
                when a.category = 'pim' then a.homeValue else '' end) as pim, sum(case when a.category = 'hits' then 
                a.homeValue else '' end) as hits, sum(case when a.category = 'blockedShots' then a.homeValue else '' 
                end) as blockedShots, sum(case when a.category = 'giveaways' then a.homeValue else '' end) as 
                giveaways, sum(case when a.category = 'takeaways' then a.homeValue else '' end) as takeaways from 
                puckpandas_import.team_game_stats_import as a join puckpandas_import.games_import as b on a.gameId = 
                b.gameId join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue from 
                puckpandas_import.team_game_stats_import as c join puckpandas_import.games_import as d on c.gameId = 
                d.gameId where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.homeTeam = e.homeTeam where 
                b.seasonId = """ + str(season_id) + """ group by a.gameId, b.homeTeam"""
            else:
                sql = """insert into puckpandas.game_team_stats (gameId, teamId, sog, faceoffWinningPctg, powerPlay, 
                powerPlayPctg, pim, hits, blockedShots, giveaways, takeaways) select a.gameId, b.awayTeam as teamId, 
                sum(case when a.category = 'sog' then a.awayValue else '' end) as sog, sum(case when a.category = 
                'faceoffWinningPctg' then a.awayValue else '' end) as faceoffWinningPctg, e.awayValue as powerPlay, 
                sum(case when a.category = 'powerPlayPctg' then a.awayValue else '' end) as powerPlayPctg, sum(case 
                when a.category = 'pim' then a.awayValue else '' end) as pim, sum(case when a.category = 'hits' then 
                a.awayValue else '' end) as hits, sum(case when a.category = 'blockedShots' then a.awayValue else '' 
                end) as blockedShots, sum(case when a.category = 'giveaways' then a.awayValue else '' end) as 
                giveaways, sum(case when a.category = 'takeaways' then a.awayValue else '' end) as takeaways from 
                puckpandas_import.team_game_stats_import as a join puckpandas_import.games_import as b on a.gameId = 
                b.gameId join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue from 
                puckpandas_import.team_game_stats_import as c join puckpandas_import.games_import as d on c.gameId = 
                d.gameId where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.awayTeam = e.awayTeam where 
                b.seasonId = @current_season group by a.gameId, b.awayTeam unionselect a.gameId, b.homeTeam as teamId, 
                sum(case when a.category = 'sog' then a.homeValue else '' end) as sog, sum(case when a.category = 
                'faceoffWinningPctg' then a.homeValue else '' end) as faceoffWinningPctg, e.homeValue as powerPlay, 
                sum(case when a.category = 'powerPlayPctg' then a.homeValue else '' end) as powerPlayPctg, sum(case 
                when a.category = 'pim' then a.homeValue else '' end) as pim, sum(case when a.category = 'hits' then 
                a.homeValue else '' end) as hits, sum(case when a.category = 'blockedShots' then a.homeValue else '' 
                end) as blockedShots, sum(case when a.category = 'giveaways' then a.homeValue else '' end) as 
                giveaways, sum(case when a.category = 'takeaways' then a.homeValue else '' end) as takeaways from 
                puckpandas_import.team_game_stats_import as a join puckpandas_import.games_import as b on a.gameId = 
                b.gameId join (select c.gameId, d.awayTeam, c.awayValue, d.homeTeam, c.homeValue from 
                puckpandas_import.team_game_stats_import as c join puckpandas_import.games_import as d on c.gameId = 
                d.gameId where c.category = 'powerPlay') as e on b.gameId = e.gameId and b.homeTeam = e.homeTeam group 
                by a.gameId, b.homeTeam"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_team_stats"""

        if season_id != 0:
            sql += """ where season_id = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select gameId, teamId, sog, faceoffWinningPctg, powerPlay, powerPlayPctg, pim, hits, blockedShots, 
        giveaways, takeaways from puckpandas.game_team_stats"""

        game_team_stats_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_team_stats_df.size > 0:
            game_team_stats_df = game_team_stats_df.reindex(columns=self.table_columns)
            game_team_stats_df.infer_objects().fillna('', inplace=True)
            game_team_stats_df.drop_duplicates(inplace=True)
            self.game_team_stats_df = game_team_stats_df

        return self.game_team_stats_df
