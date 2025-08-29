import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class SkaterCareerTotalsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals', 'regularSeason.assists',
                              'regularSeason.pim', 'regularSeason.points', 'regularSeason.plusMinus',
                              'regularSeason.powerPlayGoals', 'regularSeason.powerPlayPoints',
                              'regularSeason.shorthandedPoints', 'regularSeason.gameWinningGoals',
                              'regularSeason.otGoals', 'regularSeason.shots', 'regularSeason.shootingPctg',
                              'regularSeason.faceoffWinningPctg', 'regularSeason.avgToi',
                              'regularSeason.shorthandedGoals', 'playoffs.gamesPlayed', 'playoffs.goals',
                              'playoffs.assists', 'playoffs.pim', 'playoffs.points', 'playoffs.plusMinus',
                              'playoffs.powerPlayGoals', 'playoffs.powerPlayPoints', 'playoffs.shorthandedPoints',
                              'playoffs.gameWinningGoals', 'playoffs.otGoals', 'playoffs.shots',
                              'playoffs.shootingPctg', 'playoffs.faceoffWinningPctg', 'playoffs.avgToi',
                              'playoffs.shorthandedGoals']
        self.skater_career_totals_df = pd.DataFrame()
        self.skater_career_totals_df = self.skater_career_totals_df.reindex(columns=self.table_columns)

    def update_db(self):
        career_totals_found = 0
        if self.json != {}:
            career_totals_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.skater_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
                  "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, `regularSeason.points`, " \
                  "`regularSeason.plusMinus`, `regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, " \
                  "`regularSeason.shorthandedPoints`, `regularSeason.gameWinningGoals`, `regularSeason.otGoals`, " \
                  "`regularSeason.shots`, `regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, " \
                  "`regularSeason.avgToi`, `regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, " \
                  "`playoffs.goals`, `playoffs.assists`, `playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, " \
                  "`playoffs.powerPlayGoals`, `playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, " \
                  "`playoffs.gameWinningGoals`, `playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, " \
                  "`playoffs.faceoffWinningPctg`, `playoffs.avgToi`, `playoffs.shorthandedGoals`) values " \
                  "(:playerId, :regularSeasongamesPlayed, :regularSeasongoals, :regularSeasonassists, " \
                  ":regularSeasonpim, :regularSeasonpoints, :regularSeasonplusMinus, " \
                  ":regularSeasonpowerPlayGoals, :regularSeasonpowerPlayPoints, :regularSeasonshorthandedPoints, " \
                  ":regularSeasongameWinningGoals, :regularSeasonotGoals, :regularSeasonshots, " \
                  ":regularSeasonshootingPctg, :regularSeasonfaceoffWinningPctg, :regularSeasonavgToi, " \
                  ":regularSeasonshorthandedGoals, :playoffsgamesPlayed, :playoffsgoals, :playoffsassists, " \
                  ":playoffspim, :playoffspoints, :playoffsplusMinus, :playoffspowerPlayGoals, " \
                  ":playoffspowerPlayPoints, :playoffsshorthandedPoints, :playoffsgameWinningGoals, " \
                  ":playoffsotGoals, :playoffsshots, :playoffsshootingPctg, :playoffsfaceoffWinningPctg, " \
                  ":playoffsavgToi, :playoffsshorthandedGoals)"
            skater_career_transform_df = self.skater_career_totals_df
            skater_career_transform_df.columns = skater_career_transform_df.columns.str.replace('.','')
            params = skater_career_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.PlayerImportLog(player_id=self.player_id, career_totals_found=career_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.skater_career_totals_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`, `regularSeason.assists`, " \
              "`regularSeason.pim`, `regularSeason.points`, `regularSeason.plusMinus`, " \
              "`regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, `regularSeason.shorthandedPoints`, " \
              "`regularSeason.gameWinningGoals`, `regularSeason.otGoals`, `regularSeason.shots`, " \
              "`regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, `regularSeason.avgToi`, " \
              "`regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, " \
              "`playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, `playoffs.powerPlayGoals`, " \
              "`playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, `playoffs.gameWinningGoals`, " \
              "`playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, `playoffs.faceoffWinningPctg`, " \
              "`playoffs.avgToi`, `playoffs.shorthandedGoals` from puckpandas_import.skater_career_totals_import " \
              "where playerId = " + str(self.player_id)
        skater_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_career_totals_df.size > 0:
            skater_career_totals_df = skater_career_totals_df.reindex(columns=self.table_columns)
            skater_career_totals_df.infer_objects().fillna('', inplace=True)
            self.skater_career_totals_df = skater_career_totals_df

        return True

    def query_api(self):
        skater_career_totals_df = pd.json_normalize(self.json)
        skater_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        skater_career_totals_df.insert(0, 'playerId', self.player_id)

        if skater_career_totals_df.size > 0:
            skater_career_totals_df = skater_career_totals_df.reindex(columns=self.table_columns)
            skater_career_totals_df.fillna(0, inplace=True)
            self.skater_career_totals_df = skater_career_totals_df


        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
