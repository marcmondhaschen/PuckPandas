import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameGoals:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','reason','shotType','goalieInNetId',
                              'scoringPlayerId','scoringPlayerTotal','assist1PlayerId','assist1PlayerTotal',
                              'assist2PlayerId','assist2PlayerTotal','awayScore','homeScore']
        self.game_goals_df = pd.DataFrame()
        self.query_db()
        self.game_goals_df = self.game_goals_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_goals_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_goals (playId, gameId, eventId, sortOrder, reason, shotType, " \
                  "goalieInNetId, scoringPlayerId, scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, " \
                  "assist2PlayerId, assist2PlayerTotal, awayScore, homeScore) select a.playId, b.gameId, b.eventId, " \
                  "b.sortOrder, b.`details.reason` as reason, b.`details.shotType` as shotType, " \
                  "b.`details.goalieInNetId` as goalieInNetId, b.`details.scoringPlayerId` as scoringPlayerId, " \
                  "b.`details.scoringPlayerTotal` as scoringPlayerTotal, b.`details.assist1PlayerId` as " \
                  "assist1PlayerId, b.`details.assist1PlayerTotal` as assist1PlayerTotal, b.`details.assist2PlayerId` "\
                  "as assist2PlayerId, b.`details.assist2PlayerTotal` as assist2PlayerTotal, b.`details.awayScore` " \
                  "as awayScore, b.`details.homeScore` as homeScore from puckpandas.plays as a join " \
                  "puckpandas_import.games_import as g on a.gameId = g.gameId join puckpandas_import.plays_import as " \
                  "b on a.gameId = b.gameId and a.eventId = b.eventId where b.typeCode = '505' and " \
                  "g.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_goals"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playId, gameId, eventId, sortOrder, reason, shotType, goalieInNetId, scoringPlayerId, " \
              "scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, assist2PlayerId, assist2PlayerTotal, " \
              "awayScore, homeScore from puckpandas.game_goals"
        game_goals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_goals_df.size > 0:
            game_goals_df = game_goals_df.reindex(columns=self.table_columns)
            game_goals_df.infer_objects().fillna('', inplace=True)
            game_goals_df.drop_duplicates(inplace=True)
            self.game_goals_df = game_goals_df

        return self.game_goals_df
