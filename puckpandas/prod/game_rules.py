import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GameRules:
    def __init__(self):
        self.table_columns = ['gameId','neutralSite','awayTeamSplitSquad','homeTeamSplitSquad','maxRegulationPeriods',
                              'maxPeriods','regPeriods']
        self.game_rules_df = pd.DataFrame()
        self.query_db()
        self.game_rules_df = self.game_rules_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_rules_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_rules (gameId, neutralSite, awayTeamSplitSquad, homeTeamSplitSquad, " \
                  "maxRegulationPeriods, maxPeriods, regPeriods) select a.gameId, a.neutralSite, " \
                  "a.awayTeamSplitSquad, a.homeTeamSplitSquad, b.`periodDescriptor.maxRegulationPeriods` as " \
                  "maxRegulationPeriods, b.maxPeriods, b.regPeriods from puckpandas_import.games_import as a join " \
                  "puckpandas_import.game_center_import as b on a.gameId = b.gameId where " \
                  "a.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_rules"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select gameId, neutralSite, awayTeamSplitSquad, homeTeamSplitSquad, maxRegulationPeriods, maxPeriods, " \
              "regPeriods from puckpandas.game_rules"
        game_rules_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_rules_df.size > 0:
            game_rules_df = game_rules_df.reindex(columns=self.table_columns)
            game_rules_df.infer_objects().fillna('', inplace=True)
            game_rules_df.drop_duplicates(inplace=True)
            self.game_rules_df = game_rules_df

        return self.game_rules_df
