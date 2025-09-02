import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameSeries:
    def __init__(self):
        self.table_columns = ['gameId','seriesLetter','neededToWin','topSeedWins','bottomSeedWins',
                              'gameNumberOfSeries','awayTeam','awayTeamWins','homeTeam','homeTeamWins']
        self.game_series_df = pd.DataFrame()
        self.query_db()
        self.game_series_df = self.game_series_df.reindex(columns=self.table_columns)

    def update_db(self, season_id=0):
        if self.game_series_df.size > 0:
            engine = pp.dba_prod_login()

            if season_id != 0:
                sql = """insert into puckpandas.game_series (gameId, seriesLetter, neededToWin, topSeedWins, 
                bottomSeedWins, gameNumberOfSeries, awayTeam, awayTeamWins, homeTeam, homeTeamWins) select a.gameId, 
                case when a.`seriesStatus.seriesLetter` = '0' then '' else a.`seriesStatus.seriesLetter` end as 
                seriesLetter, a.`seriesStatus.neededToWin` as neededToWin, a.`seriesStatus.topSeedWins` as topSeedWins, 
                a.`seriesStatus.bottomSeedWins` as bottomSeedWins, a.`seriesStatus.gameNumberOfSeries` as 
                gameNumberOfSeries, a.awayTeam, b.`seasonSeriesWins.awayTeamWins` as awayTeamWins, a.homeTeam, 
                b.`seasonSeriesWins.homeTeamWins` as homeTeamWins from puckpandas_import.games_import as a join 
                puckpandas_import.game_center_right_rail_import as b on a.gameId = b.gameId where 
                a.seasonId = """ + str(season_id) + """ order by gameId"""
            else:
                sql = """insert into puckpandas.game_series (gameId, seriesLetter, neededToWin, topSeedWins, 
                bottomSeedWins, gameNumberOfSeries, awayTeam, awayTeamWins, homeTeam, homeTeamWins) select a.gameId, 
                case when a.`seriesStatus.seriesLetter` = '0' then '' else a.`seriesStatus.seriesLetter` end as 
                seriesLetter, a.`seriesStatus.neededToWin` as neededToWin, a.`seriesStatus.topSeedWins` as topSeedWins, 
                a.`seriesStatus.bottomSeedWins` as bottomSeedWins, a.`seriesStatus.gameNumberOfSeries` as 
                gameNumberOfSeries, a.awayTeam, b.`seasonSeriesWins.awayTeamWins` as awayTeamWins, a.homeTeam, 
                b.`seasonSeriesWins.homeTeamWins` as homeTeamWins from puckpandas_import.games_import as a join 
                puckpandas_import.game_center_right_rail_import as b on a.gameId = b.gameId"""

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db(season_id=0):
        engine = pp.dba_prod_login()
        sql = """delete from puckpandas.game_series"""

        if season_id != 0:
            sql += """ where seasonId = """ + str(season_id)

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = """select gameId, seriesLetter, neededToWin, topSeedWins, bottomSeedWins, gameNumberOfSeries, awayTeam, 
        awayTeamWins, homeTeam, homeTeamWins from puckpandas.game_series"""

        game_series_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_series_df.size > 0:
            game_series_df = game_series_df.reindex(columns=self.table_columns)
            game_series_df.infer_objects().fillna('', inplace=True)
            game_series_df.drop_duplicates(inplace=True)
            self.game_series_df = game_series_df

        return self.game_series_df
