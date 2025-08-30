import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class GameResults:
    def __init__(self):
        self.table_columns = ['resultId', 'gameId', 'gameType', 'seasonId', 'teamId', 'opponentTeamId', 'teamWin',
                              'teamOT', 'teamLoss', 'awayGame', 'awayWin', 'awayOT', 'awayLoss', 'homeGame', 'homeWin',
                              'homeOT', 'homeLoss', 'tie', 'overtime', 'awayScore', 'homeScore', 'standingPoints']
        self.game_results_df = pd.DataFrame()
        self.query_db()
        self.game_results_df = self.game_results_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_results_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_results select concat(gameId, lpad(teamId, 2, 0)) as resultId, " \
                  "gameId, gameType, seasonId, teamId, opponentTeamId, teamWin, teamOT, teamLoss, awayGame, awayWin, " \
                  "awayOT, awayLoss, homeGame, homeWin, homeOT, homeLoss, tie, overtime, awayScore, homeScore, case " \
                  "when gameType = 2 and teamWin = 1 then 2 when gameType = 2 and overtime = 1 and teamWin = 0 then " \
                  "1 when gameType = 3 and teamWin = 1 then 1 else 0 end as standingPoints from (select gameId, " \
                  "gameType, seasonId, teamId, opponentTeamId, awayGame, homeGame, case when (awayGame = 1 and " \
                  "awayWin = 1) or (homeGame = 1 and homeWin = 1) then 1 else 0 end as teamWin, case when " \
                  "(awayGame = 1 and awayWin = 0 and overtime = 1) or (homeGame = 1 and homeWin = 0 and " \
                  "overtime = 1) then 1 else 0 end as teamOT, case when (awayGame = 1 and awayWin = 0 and " \
                  "overtime = 0) or (homeGame = 1 and homeWin = 0 and overtime = 0) then 1 else 0 end as teamLoss, " \
                  "case when awayGame = 1 and awayWin = 1 then 1 else 0 end as awayWin, case when awayGame = 1 and " \
                  "awayWin = 0 and overtime = 1 then 1 else 0 end as awayOT, case when awayGame = 1 and awayWin = 0 " \
                  "and overtime = 0 then 1 else 0 end as awayLoss, case when homeGame = 1 and homeWin = 1 then 1 " \
                  "else 0 end as homeWin, case when homeGame = 1 and homeWin = 0 and overtime = 1 then 1 else 0 end " \
                  "as homeOT, case when homeGame = 1 and homeWin = 0 and overtime = 0 then 1 else 0 end as homeLoss, " \
                  "tie, overtime, awayScore, homeScore from (select g.gameId, g.gameType, g.seasonId, g.awayTeam as " \
                  "teamId, g.homeTeam as opponentTeamId, 1 as awayGame, 0 as homeGame, case when s.awayScore > " \
                  "s.homeScore then 1 else 0 end as awayWin, case when s.awayScore < s.homeScore then 1 else 0 end " \
                  "as homeWin, case when s.awayScore = s.homeScore then 1 else 0 end as tie, s.awayScore, " \
                  "s.homeScore, case when s.periodType in ('OT', 'SO') then 1 else 0 end as overtime from " \
                  "puckpandas.games as g join puckpandas.game_scores as s on g.gameId = s.gameId join " \
                  "puckpandas.game_progress as p on g.gameId = p.gameId where g.gameType in (2, 3) and " \
                  "s.periodType in ('OT', 'REG', 'SO') and p.gameState in ('FINAL', 'OFF') and g.seasonId = " \
                  + str(self.current_season) + " union select g.gameId, g.gameType, g.seasonId, g.homeTeam as " \
                  "teamId, g.awayTeam as opponentTeamId, 0 as awayGame, 1 as homeGame, case when s.awayScore > " \
                  "s.homeScore then 1 else 0 end as awayWin, case when s.awayScore < s.homeScore then 1 else 0 end as "\
                  "homeWin, case when s.awayScore = s.homeScore then 1 else 0 end as tie, s.awayScore, s.homeScore, " \
                  "'case when s.periodType in ('OT', 'SO') then 1 else 0 end as overtime from puckpandas.games " \
                  "as g join puckpandas.game_scores as s on g.gameId = s.gameId join " \
                  "puckpandas.game_progress as p on g.gameId = p.gameId where g.gameType in (2, 3) and " \
                  "s.periodType in ('OT', 'REG', 'SO') and p.gameState in ('FINAL', 'OFF') and g.seasonId = " \
                  + str(self.current_season) + ") as a) as b"

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_results"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select resultId, gameId, gameType, seasonId, teamId, opponentTeamId, teamWin, teamOT, teamLoss, " \
              "awayGame, awayWin, awayOT, awayLoss, homeGame, homeWin, homeOT, homeLoss, tie, overtime, awayScore, " \
              "homeScore, standingPoints from puckpandas.game_results"
        game_results_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_results_df.size > 0:
            game_results_df = game_results_df.reindex(columns=self.table_columns)
            game_results_df.infer_objects().fillna('', inplace=True)
            game_results_df.drop_duplicates(inplace=True)
            self.game_results_df = game_results_df

        return self.game_results_df
