import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class GameScores:
    def __init__(self):
        self.table_columns = ['gameId', 'periodType', 'gameOutcome', 'awayTeam', 'awayScore', 'awayLineScore',
                              'awaySOG', 'homeTeam', 'homeScore', 'homeLineScore', 'homeSOG']
        self.game_scores_df = pd.DataFrame()
        self.query_db()
        self.game_scores_df = self.game_scores_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_scores_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_scores (gameId, periodType, gameOutcome, awayTeam, awayScore, " \
                  "awayLineScore, awaySOG, homeTeam, homeScore, homeLineScore, homeSOG) select a.gameId, " \
                  "a.periodType, a.gameOutcome, a.awayTeam, a.awayTeamScore as awayScore, c.`linescore.totals.away` " \
                  "as awayLineScore, b.`awayTeam.sog` as awaySOG, a.homeTeam, a.homeTeamScore as homeScore, " \
                  "c.`linescore.totals.home` as homeLineScore, b.`homeTeam.sog` as homeSOG from " \
                  "puckpandas_import.games_import as a join puckpandas_import.game_center_import as b on " \
                  "a.gameId = b.gameId join puckpandas_import.game_center_right_rail_import as c on a.gameId = " \
                  "c.gameId where a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_scores"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select gameId, periodType, gameOutcome, awayTeam, awayScore, awayLineScore, awaySOG, homeTeam, " \
              "homeScore, homeLineScore, homeSOG from puckpandas.game_scores"
        game_scores_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_scores_df.size > 0:
            game_scores_df = game_scores_df.reindex(columns=self.table_columns)
            game_scores_df.infer_objects().fillna('', inplace=True)
            game_scores_df.drop_duplicates(inplace=True)
            self.game_scores_df = game_scores_df

        return self.game_scores_df
