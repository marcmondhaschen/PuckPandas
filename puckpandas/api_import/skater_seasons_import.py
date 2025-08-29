import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class SkaterSeasonsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'goals', 'leagueAbbrev', 'pim',
                              'points', 'season', 'sequence', 'teamName.default', 'teamCommonName.default',
                              'teamPlaceNameWithPreposition.default', 'plusMinus', 'avgToi', 'faceoffWinningPctg',
                              'gameWinningGoals', 'otGoals', 'powerPlayGoals', 'powerPlayPoints', 'shootingPctg',
                              'shorthandedGoals', 'shorthandedPoints', 'shots']
        self.skater_season_df = pd.DataFrame()
        self.skater_season_df = self.skater_season_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_totals_found = 0
        if self.json != {}:
            season_totals_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.skater_season_import (playerId, assists, gameTypeId, gamesPlayed, " \
                  "goals, leagueAbbrev, pim, points, season, sequence, `teamName.default`, plusMinus, avgToi, " \
                  "faceoffWinningPctg, gameWinningGoals, otGoals, powerPlayGoals, powerPlayPoints, shootingPctg, " \
                  "shorthandedGoals, shorthandedPoints, shots, `teamCommonName.default`, " \
                  "`teamPlaceNameWithPreposition.default`) values (:playerId, :assists, :gameTypeId, :gamesPlayed, " \
                  ":goals, :leagueAbbrev, :pim, :points, :season, :sequence, :teamNamedefault, :plusMinus, :avgToi, " \
                  ":faceoffWinningPctg, :gameWinningGoals, :otGoals, :powerPlayGoals, :powerPlayPoints, " \
                  ":shootingPctg, :shorthandedGoals, :shorthandedPoints, :shots, :teamCommonNamedefault, " \
                  ":teamPlaceNameWithPrepositiondefault)"
            skater_season_transform_df = self.skater_season_df
            skater_season_transform_df.columns = skater_season_transform_df.columns.str.replace('.', '')
            params = skater_season_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.PlayerImportLog(player_id=self.player_id, season_totals_found=season_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.skater_season_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select playerId, assists, gameTypeId, gamesPlayed, goals, leagueAbbrev, pim, points, season, " \
              "sequence, `teamName.default`, plusMinus, avgToi, faceoffWinningPctg, gameWinningGoals, otGoals, " \
              "powerPlayGoals, powerPlayPoints, shootingPctg, shorthandedGoals, shorthandedPoints, shots, " \
              "`teamCommonName.default`, `teamPlaceNameWithPreposition.default` from " \
              "puckpandas_import.skater_season_import where playerId = " + str(self.player_id)
        skater_season_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_season_df.size > 0:
            skater_season_df = skater_season_df.reindex(columns=self.table_columns)
            skater_season_df.infer_objects().fillna('', inplace=True)
            self.skater_season_df = skater_season_df

        return True

    def query_api(self):
        skater_season_df = pd.json_normalize(self.json)
        skater_season_df.insert(0, 'playerId', self.player_id)

        if skater_season_df.size > 0:
            skater_season_df = skater_season_df.reindex(columns=self.table_columns)
            skater_season_df.fillna(0, inplace=True)
            self.skater_season_df = skater_season_df

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
