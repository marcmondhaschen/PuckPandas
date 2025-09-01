import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameCoaches:
    def __init__(self):
        self.table_columns = ['gameCoachId','gameId','teamId','coachId','home','away']
        self.game_coaches_df = pd.DataFrame()
        self.query_db()
        self.game_coaches_df = self.game_coaches_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_coaches_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into `puckpandas`.`game_coaches` (gameId, teamId, coachId, home, away) select a.gameId, " \
                  "a.awayTeam as teamId, c.coachId, 1 as away, 0 as home  from `puckpandas_import`.`games_import` " \
                  "as a  join `puckpandas_import`.`game_center_right_rail_import` as b on a.gameId = b.gameId join " \
                  "`puckpandas`.`coaches` as c on b.`gameInfo.awayTeam.headCoach.default` = c.coachName where " \
                  "a.seasonId = " + str(self.current_season) + " union select a.gameId, a.homeTeam as teamId, " \
                  "c.coachId, 0 as away, 1 as home from puckpandas_import.games_import as a  join " \
                  "puckpandas_import.game_center_right_rail_import as b on a.gameId = b.gameId join " \
                  "puckpandas.coaches as c on b.`gameInfo.homeTeam.headCoach.default` = c.coachName where " \
                  "a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_coaches"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select gameCoachId, gameId, teamId, coachId, home, away from puckpandas.game_coaches"
        game_coaches_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_coaches_df.size > 0:
            game_coaches_df = game_coaches_df.reindex(columns=self.table_columns)
            game_coaches_df.infer_objects().fillna('', inplace=True)
            game_coaches_df.drop_duplicates(inplace=True)
            self.game_coaches_df = game_coaches_df

        return self.game_coaches_df
