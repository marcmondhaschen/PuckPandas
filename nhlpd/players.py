import pandas as pd
import nhlpd
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
            engine = nhlpd.dba_import_login()
            sql = "insert into skater_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
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

        log = nhlpd.PlayerImportLog(player_id=self.player_id, career_totals_found=career_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from skater_career_totals_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`, `regularSeason.assists`, " \
              "`regularSeason.pim`, `regularSeason.points`, `regularSeason.plusMinus`, " \
              "`regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, `regularSeason.shorthandedPoints`, " \
              "`regularSeason.gameWinningGoals`, `regularSeason.otGoals`, `regularSeason.shots`, " \
              "`regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, `regularSeason.avgToi`, " \
              "`regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, " \
              "`playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, `playoffs.powerPlayGoals`, " \
              "`playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, `playoffs.gameWinningGoals`, " \
              "`playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, `playoffs.faceoffWinningPctg`, " \
              "`playoffs.avgToi`, `playoffs.shorthandedGoals` from skater_career_totals_import where playerId = " \
              + str(self.player_id)
        skater_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_career_totals_df.size > 0:
            skater_career_totals_df = skater_career_totals_df.reindex(columns=self.table_columns)
            skater_career_totals_df.infer_objects().fillna('', inplace=True)
            self.skater_career_totals_df = skater_career_totals_df

        return True

    def query_nhl(self):
        skater_career_totals_df = pd.json_normalize(self.json)
        skater_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        skater_career_totals_df.insert(0, 'playerId', self.player_id)

        if skater_career_totals_df.size > 0:
            skater_career_totals_df = skater_career_totals_df.reindex(columns=self.table_columns)
            skater_career_totals_df.fillna(0, inplace=True)
            self.skater_career_totals_df = skater_career_totals_df


        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class SkaterSeasonImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'goals', 'leagueAbbrev', 'pim',
                              'points', 'season', 'sequence', 'teamName.default', 'gameWinningGoals', 'plusMinus',
                              'powerPlayGoals', 'shorthandedGoals', 'shots', 'faceoffWinningPctg']
        self.skater_season_df = pd.DataFrame()
        self.skater_season_df = self.skater_season_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_totals_found = 0
        if self.json != {}:
            season_totals_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into skater_season_import (playerId, assists, gameTypeId, gamesPlayed, goals, " \
                  "leagueAbbrev, pim, points, season, sequence, `teamName.default`, gameWinningGoals, plusMinus, " \
                  "powerPlayGoals, shorthandedGoals, shots, faceoffWinningPctg) values (:playerId, :assists, " \
                  ":gameTypeId, :gamesPlayed, :goals, :leagueAbbrev, :pim, :points, :season, :sequence, " \
                  ":teamNamedefault, :gameWinningGoals, :plusMinus, :powerPlayGoals, :shorthandedGoals, " \
                  ":shots, :faceoffWinningPctg)"
            skater_season_transform_df = self.skater_season_df
            skater_season_transform_df.columns = skater_season_transform_df.columns.str.replace('.', '')
            params = skater_season_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.PlayerImportLog(player_id=self.player_id, season_totals_found=season_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from skater_season_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select playerId, assists, gameTypeId, gamesPlayed, goals, leagueAbbrev, pim, points, season, " \
              "sequence, `teamName.default`, gameWinningGoals, plusMinus, powerPlayGoals, shorthandedGoals, " \
              "shots, faceoffWinningPctg from skater_season_import where playerId = " + str(self.player_id)
        skater_season_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if skater_season_df.size > 0:
            skater_season_df = skater_season_df.reindex(columns=self.table_columns)
            skater_season_df.infer_objects().fillna('', inplace=True)
            self.skater_season_df = skater_season_df

        return True

    def query_nhl(self):
        skater_season_df = pd.json_normalize(self.json)
        skater_season_df.insert(0, 'playerId', self.player_id)

        if skater_season_df.size > 0:
            skater_season_df = skater_season_df.reindex(columns=self.table_columns)
            skater_season_df.fillna(0, inplace=True)
            self.skater_season_df = skater_season_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class GoalieCareerTotalsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals', 'regularSeason.assists',
                              'regularSeason.pim', 'regularSeason.gamesStarted', 'regularSeason.points',
                              'regularSeason.wins', 'regularSeason.losses', 'regularSeason.otLosses',
                              'regularSeason.shotsAgainst', 'regularSeason.goalsAgainst',
                              'regularSeason.goalsAgainstAvg', 'regularSeason.savePctg', 'regularSeason.shutouts',
                              'regularSeason.timeOnIce', 'regularSeason.timeOnIceMinutes',
                              'regularSeason.timeOnIceSeconds', 'playoffs.gamesPlayed', 'playoffs.goals',
                              'playoffs.assists', 'playoffs.pim', 'playoffs.gamesStarted', 'playoffs.points',
                              'playoffs.wins', 'playoffs.losses', 'playoffs.otLosses', 'playoffs.shotsAgainst',
                              'playoffs.goalsAgainst', 'playoffs.goalsAgainstAvg', 'playoffs.savePctg',
                              'playoffs.shutouts', 'playoffs.timeOnIce', 'playoffs.timeOnIceMinutes',
                              'playoffs.timeOnIceSeconds']
        self.goalie_career_df = pd.DataFrame()
        self.goalie_career_df = self.goalie_career_df.reindex(columns=self.table_columns)

    def update_db(self):
        career_totals_found = 0
        if self.json != {}:
            career_totals_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into goalie_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
                  "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, " \
                  "`regularSeason.gamesStarted`, `regularSeason.points`, `regularSeason.wins`, " \
                  "`regularSeason.losses`, `regularSeason.otLosses`, `regularSeason.shotsAgainst`, " \
                  "`regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, " \
                  "`regularSeason.savePctg`, `regularSeason.shutouts`, `regularSeason.timeOnIce`, " \
                  "`regularSeason.timeOnIceMinutes`, `regularSeason.timeOnIceSeconds`, `playoffs.gamesPlayed`, " \
                  "`playoffs.goals`, `playoffs.assists`, `playoffs.pim`, `playoffs.gamesStarted`, `playoffs.points`, " \
                  "`playoffs.wins`, `playoffs.losses`, `playoffs.otLosses`, `playoffs.shotsAgainst`, " \
                  "`playoffs.goalsAgainst`, `playoffs.goalsAgainstAvg`, `playoffs.savePctg`, `playoffs.shutouts`, " \
                  "`playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, `playoffs.timeOnIceSeconds`) values " \
                  "(playerId, :regularSeasongamesPlayed, :regularSeasongoals, :regularSeasonassists, " \
                  ":regularSeasonpim, :regularSeasongamesStarted, :regularSeasonpoints, :regularSeasonwins, " \
                  ":regularSeasonlosses, :regularSeasonotLosses, :regularSeasonshotsAgainst, " \
                  ":regularSeasongoalsAgainst, :regularSeasongoalsAgainstAvg, :regularSeasonsavePctg, " \
                  ":regularSeasonshutouts, :regularSeasontimeOnIce, :regularSeasontimeOnIceMinutes, " \
                  ":regularSeasontimeOnIceSeconds, :playoffsgamesPlayed, :playoffsgoals, :playoffsassists, " \
                  ":playoffspim, :playoffsgamesStarted, :playoffspoints, :playoffswins, :playoffslosses, " \
                  ":playoffsotLosses, :playoffsshotsAgainst, :playoffsgoalsAgainst, :playoffsgoalsAgainstAvg, " \
                  ":playoffssavePctg, :playoffsshutouts, :playoffstimeOnIce, :playoffstimeOnIceMinutes, " \
                  ":playoffstimeOnIceSeconds)"
            goalie_career_transform_df = self.goalie_career_df
            goalie_career_transform_df.columns = goalie_career_transform_df.columns.str.replace('.', '')
            params = goalie_career_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.PlayerImportLog(player_id=self.player_id, career_totals_found=career_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from goalie_career_totals_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql= "select playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`, `regularSeason.assists`, " \
              "`regularSeason.pim`, `regularSeason.gamesStarted`, `regularSeason.points`, `regularSeason.wins`, " \
              "`regularSeason.losses`, `regularSeason.otLosses`, `regularSeason.shotsAgainst`, " \
              "`regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, `regularSeason.savePctg`, " \
              "`regularSeason.shutouts`, `regularSeason.timeOnIce`, `regularSeason.timeOnIceMinutes`, " \
              "`regularSeason.timeOnIceSeconds`, `playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, " \
              "`playoffs.pim`, `playoffs.gamesStarted`, `playoffs.points`, `playoffs.wins`, `playoffs.losses`, " \
              "`playoffs.otLosses`, `playoffs.shotsAgainst`, `playoffs.goalsAgainst`, `playoffs.goalsAgainstAvg`, " \
              "`playoffs.savePctg`, `playoffs.shutouts`, `playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, " \
              "`playoffs.timeOnIceSeconds` from goalie_career_totals_import where playerId = " + str(self.player_id)
        goalie_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.infer_objects().fillna('', inplace=True)
            self.goalie_career_df = goalie_career_totals_df

        return True

    def query_nhl(self):
        goalie_career_totals_df = pd.json_normalize(self.json)
        goalie_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_career_totals_df.insert(0, 'playerId', self.player_id)

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.fillna(0, inplace=True)
            self.goalie_career_df = goalie_career_totals_df

        if self.goalie_career_df.loc[0, 'regularSeason.timeOnIce'] != 0:
            self.goalie_career_df[['regularSeason.timeOnIceMinutes', 'regularSeason.timeOnIceSeconds']] = (
                self.goalie_career_df['regularSeason.timeOnIce'].str.split(":", expand=True))
            self.goalie_career_df['regularSeason.timeOnIceSeconds'] = (
                    int(self.goalie_career_df['regularSeason.timeOnIceMinutes'].iloc[0]) * 60 +
                    int(self.goalie_career_df['regularSeason.timeOnIceSeconds'].iloc[0]))
        if self.goalie_career_df.loc[0, 'playoffs.timeOnIce'] != 0:
            self.goalie_career_df[['playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds']] = (
                self.goalie_career_df['playoffs.timeOnIce'].str.split(":", expand=True))
            self.goalie_career_df['playoffs.timeOnIceSeconds'] = (
                    int(self.goalie_career_df['playoffs.timeOnIceMinutes'].iloc[0]) * 60 +
                    int(self.goalie_career_df['playoffs.timeOnIceSeconds'].iloc[0]))

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class GoalieSeasonImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'gameTypeId', 'gamesPlayed', 'goalsAgainst', 'goalsAgainstAvg',
                              'leagueAbbrev', 'losses', 'season', 'sequence', 'shutouts', 'ties', 'timeOnIce',
                              'timeOnIceMinutes', 'timeOnIceSeconds', 'wins', 'teamName.default', 'savePctg',
                              'shotsAgainst', 'otLosses', 'assists', 'gamesStarted', 'goals', 'pim']
        self.goalie_season_df = pd.DataFrame()
        self.goalie_season_df = self.goalie_season_df.reindex(columns=self.table_columns)

    def update_db(self):
        season_totals_found = 0
        if self.json != {}:
            season_totals_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into goalie_season_import (playerId, gameTypeId, gamesPlayed, goalsAgainst, " \
                  "goalsAgainstAvg, leagueAbbrev, losses, season, sequence, shutouts, ties, timeOnIce, " \
                  "timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, savePctg, shotsAgainst, " \
                  "otLosses, assists, gamesStarted, goals, pim) values (:playerId, :gameTypeId, :gamesPlayed, " \
                  ":goalsAgainst, :goalsAgainstAvg, :leagueAbbrev, :losses, :season, :sequence, :shutouts, :ties, " \
                  ":timeOnIce, :timeOnIceMinutes, :timeOnIceSeconds, :wins, :teamNamedefault, :savePctg, " \
                  ":shotsAgainst, :otLosses, :assists, :gamesStarted, :goals, :pim)"
            goalie_season_transform_df = self.goalie_season_df
            goalie_season_transform_df.columns = goalie_season_transform_df.columns.str.replace('.', '')
            params = goalie_season_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.PlayerImportLog(player_id=self.player_id, season_totals_found=season_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from goalie_season_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, season, "\
              "sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, "\
              "savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, pim from goalie_season_import where "\
              "playerId = " + str(self.player_id)
        goalie_season_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_season_df.size > 0:
            goalie_season_df = goalie_season_df.reindex(columns=self.table_columns)
            goalie_season_df.infer_objects().fillna('', inplace=True)
            self.goalie_season_df = goalie_season_df

        return True

    def query_nhl(self):
        goalie_season_df = pd.json_normalize(self.json)
        goalie_season_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_season_df.insert(0, 'playerId', self.player_id)

        if goalie_season_df.size > 0:
            goalie_season_df = goalie_season_df.reindex(columns=self.table_columns)
            goalie_season_df.fillna(0, inplace=True)
            self.goalie_season_df = goalie_season_df

        if not self.goalie_season_df.empty:
            # self.goalie_season_df.loc[self.goalie_season_df.timeOnIce == '', 'timeOnIce'] = '0:00'
            self.goalie_season_df.loc[self.goalie_season_df.timeOnIce == 0, 'timeOnIce'] = '0:00'
            self.goalie_season_df[['timeOnIceMinutes', 'timeOnIceSeconds']] = (
                self.goalie_season_df['timeOnIce'].str.split(":", expand=True))
            self.goalie_season_df['timeOnIceSeconds'] = (self.goalie_season_df['timeOnIceMinutes'].astype(int) * 60 +
                                                         self.goalie_season_df['timeOnIceSeconds'].astype(int))

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class PlayerAwardsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'seasonId', 'trophy.default']
        self.player_awards_df = pd.DataFrame()
        self.player_awards_df = self.player_awards_df.reindex(columns=self.table_columns)

    def update_db(self):
        awards_found = 0
        if self.json != {}:
            awards_found = 1
            engine = nhlpd.dba_import_login()
            sql = "insert into player_award_import (playerId, seasonId, `trophy.default`) values " \
                  "(:playerId, :seasonId, :trophydefault)"
            player_awards_transform_df = self.player_awards_df
            player_awards_transform_df.columns = player_awards_transform_df.columns.str.replace('.', '')
            params = player_awards_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = nhlpd.PlayerImportLog(player_id=self.player_id, awards_found=awards_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from player_award_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, " \
                     "season, sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, " \
                     "`teamName.default`, savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, " \
                     "pim from goalie_season_import where playerId = " + str(self.player_id)
        player_awards_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_awards_df.size > 0:
            player_awards_df = player_awards_df.reindex(columns=self.table_columns)
            player_awards_df.infer_objects().fillna('', inplace=True)
            self.player_awards_df = player_awards_df

        return True

    def query_nhl(self):
        player_awards_df = pd.json_normalize(self.json, record_path=["seasons"], meta=[["trophy", "default"]])
        player_awards_df.insert(0, 'playerId', self.player_id)

        if player_awards_df.size > 0:
            player_awards_df = player_awards_df.reindex(columns=self.table_columns)
            player_awards_df.infer_objects().fillna('', inplace=True)
            self.player_awards_df = player_awards_df

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True


class PlayersImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'sweaterNumber', 'position',
                              'heightInInches', 'heightInCentimeters', 'weightInPounds', 'weightInKilograms',
                              'birthDate', 'birthCountry', 'shootsCatches', 'inTop100AllTime', 'inHHOF',
                              'firstName.default', 'lastName.default', 'birthCity.default',
                              'birthStateProvince.default', 'draftDetails.year', 'draftDetails.teamAbbrev',
                              'draftDetails.round', 'draftDetails.pickInRound', 'draftDetails.overallPick']
        self.player_bios_df = pd.DataFrame()
        self.position = ''
        self.goalie_seasons = GoalieSeasonImport(player_id)
        self.goalie_career_totals = GoalieCareerTotalsImport(player_id)
        self.skater_seasons = SkaterSeasonImport(player_id)
        self.skater_career_totals = SkaterCareerTotalsImport(player_id)
        self.player_awards = PlayerAwardsImport(player_id)
        self.query_db()
        self.player_bios_df = self.player_bios_df.reindex(columns=self.table_columns)

    def update_db(self):
        player_found = 0
        if self.json != {}:
            player_found = 1

            engine = nhlpd.dba_import_login()
            sql = "insert into player_bios_import (playerId, isActive, currentTeamId, currentTeamAbbrev, " \
                  "sweaterNumber, position, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, " \
                  "birthDate, birthCountry, shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, " \
                  "`lastName.default`, `birthCity.default`, `birthStateProvince.default`, `draftDetails.year`, " \
                  "`draftDetails.teamAbbrev`, `draftDetails.round`, `draftDetails.pickInRound`, " \
                  "`draftDetails.overallPick`) values (:playerId, :isActive, :currentTeamId, :currentTeamAbbrev, " \
                  ":sweaterNumber, :position, :heightInInches, :heightInCentimeters, :weightInPounds, " \
                  ":weightInKilograms, :birthDate, :birthCountry, :shootsCatches, :inTop100AllTime, :inHHOF, " \
                  ":firstNamedefault, :lastNamedefault, :birthCitydefault, :birthStateProvincedefault, " \
                  ":draftDetailsyear, :draftDetailsteamAbbrev, :draftDetailsround, :draftDetailspickInRound, " \
                  ":draftDetailsoverallPick)"
            player_transform_df = self.player_bios_df
            player_transform_df.columns = player_transform_df.columns.str.replace('.', '')
            player_transform_df.fillna(0, inplace=True)
            params = player_transform_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

            if self.position == 'G':
                self.goalie_seasons.update_db()
                self.goalie_career_totals.update_db()
            else:
                self.skater_seasons.update_db()
                self.skater_career_totals.update_db()
            self.player_awards.update_db()

        log = nhlpd.PlayerImportLog(player_id=self.player_id, player_found=player_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = nhlpd.dba_import_login()
        sql = "delete from player_bios_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        if self.position == 'G':
            self.goalie_seasons.clear_db()
            self.goalie_career_totals.clear_db()
        else:
            self.skater_seasons.clear_db()
            self.skater_career_totals.clear_db()
        self.player_awards.clear_db()

        return True

    def query_db(self):
        engine = nhlpd.dba_import_login()
        sql = "select id, playerId, isActive, currentTeamId, currentTeamAbbrev, sweaterNumber, position, " \
              "heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, birthDate, birthCountry, " \
              "shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, `lastName.default`, `birthCity.default`, " \
              "`birthStateProvince.default`, `draftDetails.year`, `draftDetails.teamAbbrev`, `draftDetails.round`, " \
              "`draftDetails.pickInRound`, `draftDetails.overallPick` from player_bios_import where " \
              "playerId = " + str(self.player_id)
        player_bios_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_bios_df.size > 0:
            player_bios_df = player_bios_df.reindex(columns=self.table_columns)
            player_bios_df.infer_objects().fillna('', inplace=True)
            self.player_bios_df = player_bios_df
            self.position = self.player_bios_df.at[0, 'position']

        if self.position == 'G':
            self.goalie_seasons.query_db()
            self.goalie_career_totals.query_db()
        else:
            self.skater_seasons.query_db()
            self.skater_career_totals.query_db()
        self.player_awards.query_db()

        return True

    def query_nhl(self):
        url_prefix = 'https://api-web.nhle.com/v1/player/'
        url_suffix = '/landing'
        url_string = "{}{}{}".format(url_prefix, self.player_id, url_suffix)
        self.json = nhlpd.fetch_json_data(url_string)
        player_bios_df = pd.json_normalize(self.json)

        if player_bios_df.size == 0:
            return False

        player_bios_df = player_bios_df.reindex(columns=self.table_columns)
        player_bios_df.fillna(0, inplace=True)
        self.player_bios_df = player_bios_df

        self.position = self.player_bios_df.at[0, 'position']

        if 'careerTotals' in self.json and len(self.json['careerTotals']) > 0:
            if self.position == 'G':
                self.goalie_career_totals.json = self.json['careerTotals']
                self.goalie_career_totals.query_nhl()
            else:
                self.skater_career_totals.json = self.json['careerTotals']
                self.skater_career_totals.query_nhl()

        if 'seasonTotals' in self.json and len(self.json['seasonTotals']) > 0:
            if self.position == 'G':
                self.goalie_seasons.json = self.json['seasonTotals']
                self.goalie_seasons.query_nhl()
            else:
                self.skater_seasons.json = self.json['seasonTotals']
                self.skater_seasons.query_nhl()

        if 'awards' in self.json and len(self.json['awards']) > 0:
            self.player_awards.json = self.json['awards']
            self.player_awards.query_nhl()

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True
