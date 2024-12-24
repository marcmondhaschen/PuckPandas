import pandas as pd
import nhlpd


class SkaterCareerTotalsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.skater_career_totals_df = pd.DataFrame(columns=['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals',
                                                    'regularSeason.assists', 'regularSeason.pim',
                                                    'regularSeason.points', 'regularSeason.plusMinus',
                                                    'regularSeason.powerPlayGoals', 'regularSeason.powerPlayPoints',
                                                    'regularSeason.shorthandedPoints', 'regularSeason.gameWinningGoals',
                                                    'regularSeason.otGoals', 'regularSeason.shots',
                                                    'regularSeason.shootingPctg', 'regularSeason.faceoffWinningPctg',
                                                    'regularSeason.avgToi', 'regularSeason.shorthandedGoals',
                                                    'playoffs.gamesPlayed', 'playoffs.goals', 'playoffs.assists',
                                                    'playoffs.pim', 'playoffs.points', 'playoffs.plusMinus',
                                                    'playoffs.powerPlayGoals', 'playoffs.powerPlayPoints',
                                                    'playoffs.shorthandedPoints', 'playoffs.gameWinningGoals',
                                                    'playoffs.otGoals', 'playoffs.shots', 'playoffs.shootingPctg',
                                                    'playoffs.faceoffWinningPctg', 'playoffs.avgToi',
                                                    'playoffs.shorthandedGoals'])

    def update_db(self):
        cursor, db = nhlpd.db_import_login()

        for index, row in self.skater_career_totals_df.iterrows():
            sql = "insert into skater_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
                  "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, `regularSeason.points`, " \
                  "`regularSeason.plusMinus`, `regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, " \
                  "`regularSeason.shorthandedPoints`, `regularSeason.gameWinningGoals`, `regularSeason.otGoals`, " \
                  "`regularSeason.shots`, `regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, " \
                  "`regularSeason.avgToi`, `regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, " \
                  "`playoffs.goals`, `playoffs.assists`, `playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, " \
                  "`playoffs.powerPlayGoals`, `playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, " \
                  "`playoffs.gameWinningGoals`, `playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, " \
                  "`playoffs.faceoffWinningPctg`, `playoffs.avgToi`, `playoffs.shorthandedGoals`) values (%s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['regularSeason.gamesPlayed'], row['regularSeason.goals'],
                    row['regularSeason.assists'], row['regularSeason.pim'], row['regularSeason.points'],
                    row['regularSeason.plusMinus'], row['regularSeason.powerPlayGoals'],
                    row['regularSeason.powerPlayPoints'], row['regularSeason.shorthandedPoints'],
                    row['regularSeason.gameWinningGoals'], row['regularSeason.otGoals'], row['regularSeason.shots'],
                    row['regularSeason.shootingPctg'], row['regularSeason.faceoffWinningPctg'],
                    row['regularSeason.avgToi'], row['regularSeason.shorthandedGoals'], row['playoffs.gamesPlayed'],
                    row['playoffs.goals'], row['playoffs.assists'], row['playoffs.pim'], row['playoffs.points'],
                    row['playoffs.plusMinus'], row['playoffs.powerPlayGoals'], row['playoffs.powerPlayPoints'],
                    row['playoffs.shorthandedPoints'], row['playoffs.gameWinningGoals'], row['playoffs.otGoals'],
                    row['playoffs.shots'], row['playoffs.shootingPctg'], row['playoffs.faceoffWinningPctg'],
                    row['playoffs.avgToi'], row['playoffs.shorthandedGoals']])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from skater_career_totals_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = ("select playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`, `regularSeason.assists`, "
               "`regularSeason.pim`, `regularSeason.points`, `regularSeason.plusMinus`, "
               "`regularSeason.powerPlayGoals`, `regularSeason.powerPlayPoints`, `regularSeason.shorthandedPoints`, "
               "`regularSeason.gameWinningGoals`, `regularSeason.otGoals`, `regularSeason.shots`, "
               "`regularSeason.shootingPctg`, `regularSeason.faceoffWinningPctg`, `regularSeason.avgToi`, "
               "`regularSeason.shorthandedGoals`, `playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, "
               "`playoffs.pim`, `playoffs.points`, `playoffs.plusMinus`, `playoffs.powerPlayGoals`, "
               "`playoffs.powerPlayPoints`, `playoffs.shorthandedPoints`, `playoffs.gameWinningGoals`, "
               "`playoffs.otGoals`, `playoffs.shots`, `playoffs.shootingPctg`, `playoffs.faceoffWinningPctg`, "
               "`playoffs.avgToi`, `playoffs.shorthandedGoals` from skater_career_totals_import where playerId = "
               "") + str(self.player_id)
        skater_career_totals_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.skater_career_totals_df = self.skater_career_totals_df.head(0)
        self.skater_career_totals_df = pd.concat([self.skater_career_totals_df, skater_career_totals_df ])
        self.skater_career_totals_df.fillna('', inplace=True)

        return True

    def query_nhl(self):
        skater_career_totals_df = pd.json_normalize(self.json)
        skater_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        skater_career_totals_df.insert(0, 'playerId', self.player_id)

        self.skater_career_totals_df = skater_career_totals_df.head(0)
        self.skater_career_totals_df = pd.concat([self.skater_career_totals_df, skater_career_totals_df])
        self.skater_career_totals_df.fillna('', inplace=True)

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
        self.skater_season_df = pd.DataFrame(columns=['playerId', 'assists', 'gameTypeId', 'gamesPlayed', 'goals',
                                                      'leagueAbbrev', 'pim', 'points', 'season', 'sequence',
                                                      'teamName.default', 'gameWinningGoals', 'plusMinus',
                                                      'powerPlayGoals', 'shorthandedGoals', 'shots',
                                                      'faceoffWinningPctg'])

    def update_db(self):
        cursor, db = nhlpd.db_import_login()

        for index, row in self.skater_season_df.iterrows():
            sql = "insert into skater_season_import (playerId, assists, gameTypeId, gamesPlayed, goals, " \
                  "leagueAbbrev, pim, points, season, sequence, `teamName.default`, gameWinningGoals, plusMinus, " \
                  "powerPlayGoals, shorthandedGoals, shots, faceoffWinningPctg) values (%s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['assists'], row['gameTypeId'], row['gamesPlayed'], row['goals'],
                    row['leagueAbbrev'], row['pim'], row['points'], row['season'], row['sequence'],
                    row['teamName.default'], row['gameWinningGoals'], row['plusMinus'], row['powerPlayGoals'],
                    row['shorthandedGoals'], row['shots'], row['faceoffWinningPctg']])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from skater_season_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "select playerId, assists, gameTypeId, gamesPlayed, goals, leagueAbbrev, pim, points, season, " \
              "sequence, `teamName.default`, gameWinningGoals, plusMinus, powerPlayGoals, shorthandedGoals, " \
              "shots, faceoffWinningPctg from skater_career_totals_import where playerId = " + str(self.player_id)
        skater_season_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.skater_season_df = self.skater_season_df.head(0)
        self.skater_season_df = pd.concat([self.skater_season_df, skater_season_df])
        self.skater_season_df.fillna('', inplace=True)

        return True

    def query_nhl(self):
        skater_season_df = pd.json_normalize(self.json)
        skater_season_df.insert(0, 'playerId', self.player_id)

        self.skater_season_df = self.skater_season_df.hero(0)
        self.skater_season_df = pd.concat([self.skater_season_df, skater_season_df])
        self.skater_season_df.fillna('', inplace=True)

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
        self.goalie_career_totals_df = pd.DataFrame(columns=['playerId', 'regularSeason.gamesPlayed',
                                                             'regularSeason.goals', 'regularSeason.assists',
                                                             'regularSeason.pim', 'regularSeason.gamesStarted',
                                                             'regularSeason.points', 'regularSeason.wins',
                                                             'regularSeason.losses', 'regularSeason.otLosses',
                                                             'regularSeason.shotsAgainst', 'regularSeason.goalsAgainst',
                                                             'regularSeason.goalsAgainstAvg', 'regularSeason.savePctg',
                                                             'regularSeason.shutouts', 'regularSeason.timeOnIce',
                                                             'regularSeason.timeOnIceMinutes',
                                                             'regularSeason.timeOnIceSeconds', 'playoffs.gamesPlayed',
                                                             'playoffs.goals', 'playoffs.assists', 'playoffs.pim',
                                                             'playoffs.gamesStarted', 'playoffs.points',
                                                             'playoffs.wins', 'playoffs.losses', 'playoffs.otLosses',
                                                             'playoffs.shotsAgainst', 'playoffs.goalsAgainst',
                                                             'playoffs.goalsAgainstAvg', 'playoffs.savePctg',
                                                             'playoffs.shutouts', 'playoffs.timeOnIce',
                                                             'playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds'])

    def update_db(self):
        cursor, db = nhlpd.db_import_login()

        for index, row in self.goalie_career_totals_df.iterrows():
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
                  "`playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, `playoffs.timeOnIceSeconds`) values (%s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['regularSeason.gamesPlayed'], row['regularSeason.goals'],
                    row['regularSeason.assists'], row['regularSeason.pim'], row['regularSeason.gamesStarted'],
                    row['regularSeason.points'], row['regularSeason.wins'], row['regularSeason.losses'],
                    row['regularSeason.otLosses'], row['regularSeason.shotsAgainst'], row['regularSeason.goalsAgainst'],
                    row['regularSeason.goalsAgainstAvg'], row['regularSeason.savePctg'], row['regularSeason.shutouts'],
                    row['regularSeason.timeOnIce'], row['regularSeason.timeOnIceMinutes'],
                    row['regularSeason.timeOnIceSeconds'], row['playoffs.gamesPlayed'], row['playoffs.goals'],
                    row['playoffs.assists'], row['playoffs.pim'], row['playoffs.gamesStarted'], row['playoffs.points'],
                    row['playoffs.wins'], row['playoffs.losses'], row['playoffs.otLosses'],
                    row['playoffs.shotsAgainst'], row['playoffs.goalsAgainst'], row['playoffs.goalsAgainstAvg'],
                    row['playoffs.savePctg'], row['playoffs.shutouts'], row['playoffs.timeOnIce'],
                    row['playoffs.timeOnIceMinutes'], row['playoffs.timeOnIceSeconds']])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from goalie_career_totals_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
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
        goalie_career_totals_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.goalie_career_totals_df = self.goalie_career_totals_df.head(0)
        self.goalie_career_totals_df = pd.concat([self.goalie_career_totals_df, goalie_career_totals_df])
        self.goalie_career_totals_df.fillna('', inplace=True)

        return True

    def query_nhl(self):
        goalie_career_totals_df = pd.json_normalize(self.json)
        goalie_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_career_totals_df.insert(0, 'playerId', self.player_id)

        self.goalie_career_totals_df = self.goalie_career_totals_df.head(0)
        self.goalie_career_totals_df = pd.concat([self.goalie_career_totals_df, goalie_career_totals_df])
        self.goalie_career_totals_df.fillna('', inplace=True)

        if self.goalie_career_totals_df.loc[0, 'regularSeason.timeOnIce'] != 0:
            self.goalie_career_totals_df[['regularSeason.timeOnIceMinutes', 'regularSeason.timeOnIceSeconds']] = \
                self.goalie_career_totals_df['regularSeason.timeOnIce'].str.split(":", expand=True)
            self.goalie_career_totals_df['regularSeason.timeOnIceSeconds'] = \
                int(self.goalie_career_totals_df['regularSeason.timeOnIceMinutes'].iloc[0]) * 60 + \
                int(self.goalie_career_totals_df['regularSeason.timeOnIceSeconds'].iloc[0])
        if self.goalie_career_totals_df.loc[0, 'playoffs.timeOnIce'] != 0:
            self.goalie_career_totals_df[['playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds']] = \
                self.goalie_career_totals_df['playoffs.timeOnIce'].str.split(":", expand=True)
            self.goalie_career_totals_df['playoffs.timeOnIceSeconds'] = \
                int(self.goalie_career_totals_df['playoffs.timeOnIceMinutes'].iloc[0]) * 60 + \
                int(self.goalie_career_totals_df['playoffs.timeOnIceSeconds'].iloc[0])

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
        self.goalie_season_df = pd.DataFrame(columns=['playerId', 'gameTypeId', 'gamesPlayed', 'goalsAgainst',
                                                      'goalsAgainstAvg', 'leagueAbbrev', 'losses', 'season', 'sequence',
                                                      'shutouts', 'ties', 'timeOnIce', 'timeOnIceMinutes',
                                                      'timeOnIceSeconds', 'wins', 'teamName.default', 'savePctg',
                                                      'shotsAgainst', 'otLosses', 'assists', 'gamesStarted', 'goals',
                                                      'pim'])

    def update_db(self):
        cursor, db = nhlpd.db_import_login()

        for index, row in self.goalie_season_df.iterrows():
            sql = "insert into goalie_season_import (playerId, gameTypeId, gamesPlayed, goalsAgainst, " \
                  "goalsAgainstAvg, leagueAbbrev, losses, season, sequence, shutouts, ties, timeOnIce, " \
                  "timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, savePctg, shotsAgainst, " \
                  "otLosses, assists, gamesStarted, goals, pim) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = ([row['playerId'], row['gameTypeId'], row['gamesPlayed'], row['goalsAgainst'], row['goalsAgainstAvg'],
                    row['leagueAbbrev'], row['losses'], row['season'], row['sequence'], row['shutouts'], row['ties'],
                    row['timeOnIce'], row['timeOnIceMinutes'], row['timeOnIceSeconds'], row['wins'],
                    row['teamName.default'], row['savePctg'], row['shotsAgainst'], row['otLosses'], row['assists'],
                    row['gamesStarted'], row['goals'], row['pim']])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from goalie_season_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = ("select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, season, "
               "sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, `teamName.default`, "
               "savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, pim from goalie_season_import where "
               "playerId = ") + str(self.player_id)
        goalie_season_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.goalie_season_df = self.goalie_season_df.head(0)
        self.goalie_season_df = pd.concat([self.goalie_season_df, goalie_season_df])
        self.goalie_season_df.fillna('', inplace=True)

        return True

    def query_nhl(self):
        goalie_season_df = pd.json_normalize(self.json)
        goalie_season_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_season_df.insert(0, 'playerId', self.player_id)

        self.goalie_season_df = self.goalie_season_df.head(0)
        self.goalie_season_df = pd.concat([self.goalie_season_df, goalie_season_df])
        self.goalie_season_df.fillna('', inplace=True)

        if not self.goalie_season_df.empty:
            self.goalie_season_df = self.goalie_season_df.fillna(0)
            self.goalie_season_df.loc[self.goalie_season_df.timeOnIce == '', 'timeOnIce'] = '0:00'
            self.goalie_season_df.loc[self.goalie_season_df.timeOnIce == 0, 'timeOnIce'] = '0:00'
            self.goalie_season_df[['timeOnIceMinutes', 'timeOnIceSeconds']] = \
                self.goalie_season_df['timeOnIce'].str.split(":", expand=True)
            self.goalie_season_df['timeOnIceSeconds'] = \
                self.goalie_season_df['timeOnIceMinutes'].astype(int) * 60 + \
                self.goalie_season_df['timeOnIceSeconds'].astype(int)

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
        self.player_awards_df = pd.DataFrame(columns=['playerId', 'seasonId', 'trophy.default'])

    def update_db(self):
        cursor, db = nhlpd.db_import_login()

        for index, row in self.player_awards_df.iterrows():
            sql = 'insert into player_award_import (playerId, seasonId, `trophy.default`) values (%s, %s, %s)'
            val = [row['playerId'], row['seasonId'], row['trophy.default']]
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from player_award_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "select playerId, gameTypeId, gamesPlayed, goalsAgainst, goalsAgainstAvg, leagueAbbrev, losses, " \
                     "season, sequence, shutouts, ties, timeOnIce, timeOnIceMinutes, timeOnIceSeconds, wins, " \
                     "`teamName.default`, savePctg, shotsAgainst, otLosses, assists, gamesStarted, goals, " \
                     "pim from goalie_season_import where playerId = " + str(self.player_id)
        player_awards_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.player_awards_df = self.player_awards_df.head(0)
        self.player_awards_df = pd.concat([self.player_awards_df, player_awards_df])
        self.player_awards_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def query_nhl(self):
        player_awards_df = pd.json_normalize(self.json)
        player_awards_df.rename(columns={"id": "playerId"}, inplace=True)
        player_awards_df.insert(0, 'playerId', self.player_id)

        self.player_awards_df = self.player_awards_df.head(0)
        self.player_awards_df = pd.concat([self.player_awards_df, player_awards_df])
        self.player_awards_df.fillna('', inplace=True)

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
        self.player_bios_df = pd.DataFrame(columns=['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev',
                                           'sweaterNumber', 'position', 'heightInInches', 'heightInCentimeters',
                                           'weightInPounds', 'weightInKilograms', 'birthDate', 'birthCountry',
                                           'shootsCatches', 'inTop100AllTime', 'inHHOF', 'firstName.default',
                                           'lastName.default', 'birthCity.default', 'birthStateProvince.default',
                                           'draftDetails.year', 'draftDetails.teamAbbrev', 'draftDetails.round',
                                           'draftDetails.pickInRound', 'draftDetails.overallPick'])
        self.position = ''
        self.goalie_seasons = GoalieSeasonImport(self.player_id)
        self.goalie_career_totals = GoalieCareerTotalsImport(self.player_id)
        self.skater_seasons = SkaterSeasonImport(self.player_id)
        self.skater_career_totals = SkaterCareerTotalsImport(self.player_id)
        self.player_awards = PlayerAwardsImport(self.player_id)

    def update_db(self):
        if self.player_bios_df.size > 0:
            row = self.player_bios_df.iloc[0]
            row = row.fillna('')

            cursor, db = nhlpd.db_import_login()

            sql = "insert into player_bios_import (playerId, isActive, currentTeamId, currentTeamAbbrev, " \
                  "sweaterNumber, position, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, " \
                  "birthDate, birthCountry, shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, " \
                  "`lastName.default`, `birthCity.default`, `birthStateProvince.default`, `draftDetails.year`, " \
                  "`draftDetails.teamAbbrev`, `draftDetails.round`, `draftDetails.pickInRound`, " \
                  "`draftDetails.overallPick`) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row['playerId'], row['isActive'], row['currentTeamId'], row['currentTeamAbbrev'],
                   row['sweaterNumber'], row['position'], row['heightInInches'], row['heightInCentimeters'],
                   row['weightInPounds'], row['weightInKilograms'], row['birthDate'], row['birthCountry'],
                   row['shootsCatches'], row['inTop100AllTime'], row['inHHOF'], row['firstName.default'],
                   row['lastName.default'], row['birthCity.default'], row['birthStateProvince.default'],
                   row['draftDetails.year'], row['draftDetails.teamAbbrev'], row['draftDetails.round'],
                   row['draftDetails.pickInRound'], row['draftDetails.overallPick'])
            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

            self.goalie_seasons.update_db()
            self.goalie_career_totals.update_db()
            self.skater_seasons.update_db()
            self.skater_career_totals.update_db()
            self.player_awards.update_db()

        return True

    def clear_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from player_bios_import where playerId = " + str(self.player_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        self.goalie_seasons.clear_db()
        self.goalie_career_totals.clear_db()
        self.skater_seasons.clear_db()
        self.skater_career_totals.clear_db()
        self.player_awards.clear_db()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "select id, playerId, isActive, currentTeamId, currentTeamAbbrev, sweaterNumber, position, " \
              "heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, birthDate, birthCountry, " \
              "shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, `lastName.default`, `birthCity.default`, " \
              "`birthStateProvince.default`, `draftDetails.year`, `draftDetails.teamAbbrev`, `draftDetails.round`, " \
              "`draftDetails.pickInRound`, `draftDetails.overallPick` from player_bios_import where " \
              "playerId = " + str(self.player_id)
        player_bios_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        player_bios_df.fillna('', inplace=True)

        self.player_bios_df = self.player_bios_df.head(0)
        self.player_bios_df = pd.concat([self.player_bios_df, player_bios_df])
        self.player_bios_df.fillna('', inplace=True)

        self.position = self.player_bios_df.at[0, 'position']

        self.goalie_seasons.query_db()
        self.goalie_career_totals.query_db()
        self.skater_seasons.query_db()
        self.skater_career_totals.query_db()
        self.player_awards.query_db()

        return True

    def query_nhl(self):
        url_prefix = 'https://api-web.nhle.com/v1/player/'
        url_suffix = '/landing'
        url_string = "{}{}{}".format(url_prefix, self.player_id, url_suffix)
        self.json = nhlpd.fetch_json_data(url_string)

        self.player_bios_df = self.player_bios_df.head(0)
        player_bios_df = pd.json_normalize(self.json)
        self.player_bios_df = pd.concat([self.player_bios_df, player_bios_df])
        self.player_bios_df.fillna('', inplace=True)

        self.position = self.player_bios_df.at[0, 'position']

        if 'careerTotals' in self.json:
            if self.position == 'G':
                self.goalie_career_totals.json = self.json['careerTotals']
                self.goalie_career_totals.query_nhl()
            else:
                self.skater_career_totals.json = self.json['careerTotals']
                self.skater_career_totals.query_nhl()

        if 'seasonTotals' in self.json:
            if self.position == 'G':
                self.goalie_seasons.json = self.json['seasonTotals']
                self.goalie_seasons.query_nhl()
            else:
                self.skater_seasons.json = self.json['seasonTotals']
                self.skater_seasons.query_nhl()

        if 'awards' in self.json:
            self.player_awards.json = self.json['awards']
            self.player_awards.query_nhl()

        return True

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()

        return True
