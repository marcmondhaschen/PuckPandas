import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class ScratchesImport:
    def __init__(self, game_id):
        self.scratches_df = pd.DataFrame(columns=['gameId', 'playerId', 'firstName.default', 'lastName.default'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.scratches_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.scratches_df.iterrows():
                sql = "insert into scratches_import (gameId, playerId, `firstName.default`, `lastName.default`) " \
                      "values (%s, %s, %s, %s)"
                val = (row['gameId'], row['playerId'], row['firstName.default'], row['lastName.default'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from scratches_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, playerId, `firstName.default`, `lastName.default` from scratches_import where " \
              "gameId = " + str(self.game_id)
        scratches_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.scratches_df = self.scratches_df.head(0)
        self.scratches_df = pd.concat([self.scratches_df, scratches_df])
        self.scratches_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        scratches_df = pd.json_normalize(self.json)
        scratches_df.insert(0, 'gameId', self.game_id)
        scratches_df.rename(columns={"id": "playerId"}, inplace=True)

        self.scratches_df = self.scratches_df.head(0)
        self.scratches_df = pd.concat([self.scratches_df, scratches_df])
        self.scratches_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class LinesmenImport:
    def __init__(self, game_id):
        self.linesmen_df = pd.DataFrame(columns=['gameId', 'default'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.linesmen_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.linesmen_df.iterrows():
                sql = "insert into linesmen_import (gameId, `default`) values (%s, %s)"
                val = (row['gameId'], row['default'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from linesmen_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, `default` from linesmen_import where gameId = " + str(self.game_id)
        linesmen_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.linesmen_df = self.linesmen_df.head(0)
        self.linesmen_df = pd.concat([self.linesmen_df, linesmen_df])
        self.linesmen_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        linesmen_df = pd.json_normalize(self.json)
        linesmen_df.insert(0, 'gameId', self.game_id)

        self.linesmen_df = self.linesmen_df.head(0)
        self.linesmen_df = pd.concat([self.linesmen_df, linesmen_df])
        self.linesmen_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class RefereesImport:
    def __init__(self, game_id):
        self.referees_df = pd.DataFrame(columns=['gameId', 'default'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.referees_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.referees_df.iterrows():
                sql = "insert into referees_import (gameId, `default`) values (%s, %s)"
                val = (row['gameId'], row['default'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from referees_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, `default` from referees_import where gameId = " + str(self.game_id)
        referees_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.referees_df = self.referees_df.head(0)
        self.referees_df = pd.concat([self.referees_df,  referees_df])
        self.referees_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        referees_df = pd.json_normalize(self.json)
        referees_df.insert(0, 'gameId', self.game_id)

        self.referees_df = self.referees_df.head(0)
        self.referees_df = pd.concat([self.referees_df, referees_df])
        self.referees_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class SeasonSeriesImport:
    def __init__(self, game_id):
        self.season_series_df = pd.DataFrame(columns=['gameId', 'seriesNumber', 'refGameId'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.season_series_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.season_series_df.iterrows():
                sql = 'insert into season_series_import (gameId, seriesNumber, refGameId) values (%s, %s, %s)'
                val = (row['gameId'], row['seriesNumber'], row['refGameId'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from season_series_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, seriesNumber, refGameId from season_series_import where gameId = " + str(self.game_id)
        season_series_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.season_series_df = self.season_series_df.head(0)
        self.season_series_df = pd.concat([self.season_series_df, season_series_df])
        self.season_series_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        season_series_df = pd.json_normalize(self.json)
        # noinspection PyTypeChecker
        season_series_df.insert(0, 'seriesNumber', range(len(season_series_df)))
        season_series_df.insert(0, 'gameId', self.game_id)
        season_series_df.rename(columns={"id": "refGameId"}, inplace=True)

        self.season_series_df = self.season_series_df.head(0)
        self.season_series_df = pd.concat([self.season_series_df, season_series_df])
        self.season_series_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class TeamGameStatsImport:
    def __init__(self, game_id):
        self.team_game_stats_df = pd.DataFrame(columns=['gameId', 'category', 'awayValue', 'homeValue'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.team_game_stats_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.team_game_stats_df.iterrows():
                sql = "insert into team_game_stats_import (gameId, category, awayValue, homeValue) values (%s, %s, " \
                      "%s, %s)"
                val = (row['gameId'], row['category'], row['awayValue'], row['homeValue'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from team_game_stats_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, category, awayValue, homeValue from team_game_stats_import where gameId = " + \
              str(self.game_id)
        team_game_stats_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.team_game_stats_df = self.team_game_stats_df.head(0)
        self.team_game_stats_df = pd.concat([self.team_game_stats_df, team_game_stats_df])
        self.team_game_stats_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        team_game_stats_df = pd.json_normalize(self.json)
        team_game_stats_df.insert(0, 'gameId', self.game_id)

        self.team_game_stats_df = self.team_game_stats_df.head(0)
        self.team_game_stats_df = pd.concat([self.team_game_stats_df, team_game_stats_df])
        self.team_game_stats_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class RosterSpotsImport:
    def __init__(self, game_id):
        self.roster_spots_df = pd.DataFrame(columns=['gameId', 'teamId', 'playerId', 'sweaterNumber', 'positionCode',
                                                     'headshot', 'firstName', 'lastName'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        cursor, db = db_import_login()

        for index, row in self.roster_spots_df.iterrows():
            sql = "insert into roster_spots_import (gameId, teamId, playerId, sweaterNumber, positionCode, headshot," \
                  "`firstName`,`lastName`) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row['gameId'], row['teamId'], row['playerId'], row['sweaterNumber'], row['positionCode'],
                   row['headshot'], row['firstName.default'], row['lastName.default'])
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from roster_spots_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, teamId, playerId, sweaterNumber, positionCode, headshot, `firstName`, `lastName` from " \
              "roster_spots_import where gameId = " + str(self.game_id)
        roster_spots_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.roster_spots_df = self.roster_spots_df.head(0)
        self.roster_spots_df = pd.concat([self.roster_spots_df, roster_spots_df])
        self.roster_spots_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        roster_spots_df = pd.json_normalize(self.json)
        roster_spots_df.insert(0, 'gameId', self.game_id)

        self.roster_spots_df = self.roster_spots_df.head(0)
        self.roster_spots_df = pd.concat([self.roster_spots_df, roster_spots_df])
        self.roster_spots_df = roster_spots_df.fillna('')

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class PlaysImport:
    def __init__(self, game_id):
        self.plays_df = pd.DataFrame(columns=['gameId', 'eventId', 'timeInPeriod', 'timeRemaining', 'situationCode',
                                              'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
                                              'periodDescriptor.number', 'periodDescriptor.periodType',
                                              'details.eventOwnerTeamId', 'details.losingPlayerId',
                                              'details.winningPlayerId', 'details.xCoord', 'details.yCoord',
                                              'details.zoneCode', 'details.shotType', 'details.shootingPlayerId',
                                              'details.goalieInNetId', 'details.awaySOG', 'details.homeSOG',
                                              'details.reason', 'details.playerId', 'details.hittingPlayerId',
                                              'details.hitteePlayerId', 'details.scoringPlayerId',
                                              'details.scoringPlayerTotal', 'details.assist1PlayerId',
                                              'details.assist1PlayerTotal', 'details.assist2PlayerId',
                                              'details.assist2PlayerTotal', 'details.awayScore', 'details.homeScore',
                                              'details.blockingPlayerId', 'details.secondaryReason', 'details.typeCode',
                                              'details.descKey', 'details.duration', 'details.committedByPlayerId',
                                              'details.drawnByPlayerId'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.plays_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.plays_df.iterrows():
                sql = "insert into plays_import (gameId, eventId, period, periodType, timeInPeriod, timeRemaining, " \
                      "situationCode, typeCode, typeDescKey, sortOrder, eventOwnerTeamId, losingPlayerId,  " \
                      "winningPlayerId, xCoord, yCoord, zoneCode, reason, hittingPlayerId, hitteePlayerId, " \
                      "shotType, shootingPlayerId, goalieInNetId, awaySOG, homeSOG, playerId, blockingPlayerId, " \
                      "secondaryReason, detailTypeCode, detailDescKey, detailDuration, detailCommittedByPlayerId, " \
                      "detailDrawnByPlayerId, scoringPlayerId, scoringPlayerTotal, assist1PlayerId, " \
                      "assist1PlayerTotal, assist2PlayerId, assist2PlayerTotal, awayScore, homeScore) values " \
                      "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                      "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (row['gameId'], row['eventId'], row['periodDescriptor.number'],
                       row['periodDescriptor.periodType'],
                       row['timeInPeriod'], row['timeRemaining'], row['situationCode'], row['typeCode'],
                       row['typeDescKey'], row['sortOrder'], row['details.eventOwnerTeamId'],
                       row['details.losingPlayerId'], row['details.winningPlayerId'], row['details.xCoord'],
                       row['details.yCoord'], row['details.zoneCode'], row['details.reason'],
                       row['details.hittingPlayerId'], row['details.hitteePlayerId'], row['details.shotType'],
                       row['details.shootingPlayerId'], row['details.goalieInNetId'], row['details.awaySOG'],
                       row['details.homeSOG'], row['details.playerId'], row['details.blockingPlayerId'],
                       row['details.secondaryReason'], row['details.typeCode'], row['details.descKey'],
                       row['details.duration'], row['details.committedByPlayerId'], row['details.drawnByPlayerId'],
                       row['details.scoringPlayerId'], row['details.scoringPlayerTotal'],
                       row['details.assist1PlayerId'], row['details.assist1PlayerTotal'],
                       row['details.assist2PlayerId'], row['details.assist2PlayerTotal'], row['details.awayScore'],
                       row['details.homeScore'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from plays_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, eventId, period, periodType, timeInPeriod, timeRemaining, situationCode, typeCode, "\
              "typeDescKey, sortOrder, eventOwnerTeamId, losingPlayerId,  winningPlayerId, xCoord, yCoord, "\
              "zoneCode, reason, hittingPlayerId, hitteePlayerId, shotType, shootingPlayerId, goalieInNetId, "\
              "awaySOG, homeSOG, playerId, blockingPlayerId, secondaryReason, detailTypeCode, detailDescKey, "\
              "detailDuration, detailCommittedByPlayerId, detailDrawnByPlayerId, scoringPlayerId, "\
              "scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, assist2PlayerId, assist2PlayerTotal, "\
              "awayScore, homeScore from plays_import where gameId = " + str(self.game_id)
        plays_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.plays_df = self.plays_df.head(0)
        self.plays_df = pd.concat([self.plays_df, plays_df])
        self.plays_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        plays_df = pd.json_normalize(self.json)
        plays_df.insert(0, 'gameId', self.game_id)

        self.plays_df = self.plays_df.head(0)
        self.plays_df = pd.concat([self.plays_df, plays_df])
        self.plays_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class TvBroadcastsImport:
    def __init__(self, game_id):
        self.tv_broadcasts_df = pd.DataFrame(columns=['gameId', 'broadcastId', 'market', 'countryCode', 'network',
                                             'sequenceNumber'])
        self.game_id = game_id
        self.json = {}

    def updateDB(self):
        if len(self.tv_broadcasts_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.tv_broadcasts_df.iterrows():
                sql = "insert into tv_broadcasts_import (gameId, broadcastId, market, countryCode, network, " \
                      "sequenceNumber) values (%s, %s, %s, %s, %s, %s)"
                val = (row['gameId'], row['broadcastId'], row['market'], row['countryCode'], row['network'],
                       row['sequenceNumber'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from tv_broadcasts_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = db_import_login()
        sql = "select gameId, broadcastId, market, countryCode, network, sequenceNumber from tv_broadcasts_import " \
              "where gameId = " + str(self.game_id)
        tv_broadcasts_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.tv_broadcasts_df = self.tv_broadcasts_df.head(0)
        self.tv_broadcasts_df = pd.concat([self.tv_broadcasts_df, tv_broadcasts_df])
        self.tv_broadcasts_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        tv_broadcasts_df = pd.json_normalize(self.json)
        tv_broadcasts_df.rename(columns={"id": "broadcastId"}, inplace=True)
        tv_broadcasts_df.insert(0, 'gameId', self.game_id)

        self.tv_broadcasts_df = self.tv_broadcasts_df.head(0)
        self.tv_broadcasts_df = pd.concat([self.tv_broadcasts_df, tv_broadcasts_df])
        self.tv_broadcasts_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class GameCenterImport:
    def __init__(self, game_id):
        self.game_center_pbp_df = pd.DataFrame(columns=['gameId', 'season', 'gameType', 'limitedScoring', 'gameDate',
                                                        'venue.default', 'venueLocation.default', 'startTimeUTC',
                                                        'easternUTCOffset', 'venueUTCOffset', 'gameState',
                                                        'gameScheduleState', 'periodDescriptor.number',
                                                        'periodDescriptor.periodType',
                                                        'periodDescriptor.maxRegulationPeriods', 'awayTeam.id',
                                                        'awayTeam.name.default', 'awayTeam.abbrev', 'awayTeam.score',
                                                        'awayTeam.sog', 'awayTeam.logo', 'awayTeam.placename.default',
                                                        'awayTeam.placenameWithPreposition.default', 'homeTeam.id',
                                                        'homeTeam.name.default', 'homeTeam.abbrev', 'homeTeam.score',
                                                        'homeTeam.sog', 'homeTeam.logo', 'homeTeam.placename.default',
                                                        'homeTeam.placenameWithPreposition.default', 'shootoutInuse',
                                                        'otInUse', 'clock.timeRemaining', 'clock.secondsRemaining',
                                                        'clock.running', 'clock.inIntermission', 'displayPeriod',
                                                        'gameOutcome.lastPeriodType', 'gameVideo.threeMinRecap',
                                                        'regPeriods', 'summary.awayTeamWins', 'summary.homeTeamWins',
                                                        'summary.neededToWin', 'summary.linescore.totals.away',
                                                        'summary.linescore.totals.home',
                                                        'summary.gameReports.gameSummary',
                                                        'summary.gameReports.eventSummary',
                                                        'summary.gameReports.playByPlay',
                                                        'summary.gameReports.faceoffSummary',
                                                        'summary.gameReports.faceoffComparison',
                                                        'summary.gameReports.rosters',
                                                        'summary.gameReports.shotSummary',
                                                        'summary.gameReports.shiftChart', 'summary.gameReports.toiAway',
                                                        'summary.gameReports.toiHome',
                                                        'summary.awayTeam.gameInfo.headCoach.default',
                                                        'summary.homeTeam.gameInfo.headCoach.default'])
        self.game_center_rr_df = pd.DataFrame(columns=['gameId', 'seasonSeriesWins.awayTeamWins',
                                                       'seasonSeriesWins.homeTeamWins', 'seasonSeriesWins.neededToWin',
                                                       'gameInfo.awayTeam.headCoach.default',
                                                       'gameInfo.homeTeam.headCoach.default', 'gameVideo.threeMinRecap',
                                                       'linescore.totals.away', 'linescore.totals.home'])
        self.game_id = game_id
        self.pbp_json = {}
        self.rr_json = {}

        self.tv_broadcasts = TvBroadcastsImport(game_id=game_id)
        self.play_by_play = PlaysImport(game_id=game_id)
        self.roster_spots = RosterSpotsImport(game_id=game_id)
        self.team_game_stats = TeamGameStatsImport(game_id=game_id)
        self.season_series = SeasonSeriesImport(game_id=game_id)
        self.referees = RefereesImport(game_id=game_id)
        self.linesmen = LinesmenImport(game_id=game_id)
        self.scratches = ScratchesImport(game_id=game_id)

    def updateDB(self):
        if len(self.game_center_pbp_df.index) > 0:
            row = self.game_center_pbp_df.iloc[0]
            row = row.fillna('')

            cursor, db = db_import_login()

            sql = "insert into game_center_import (gameId, season, gameType, limitedScoring, gameDate, " \
                  "`venue.default`, `venueLocation.default`, startTimeUTC, easternUTCOffset, venueUTCOffset, " \
                  "gameState, gameScheduleState, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
                  "`periodDescriptor.maxRegulationPeriods`, `awayTeam.id`, `awayTeam.name.default`, " \
                  "`awayTeam.abbrev`, `awayTeam.score`, `awayTeam.sog`, `awayTeam.logo`, " \
                  "`awayTeam.placename.default`, `awayTeam.placenameWithPreposition.default`, `homeTeam.id`, " \
                  "`homeTeam.name.default`, `homeTeam.abbrev`, `homeTeam.score`, `homeTeam.sog`, " \
                  "`homeTeam.logo`, `homeTeam.placename.default`, `homeTeam.placenameWithPreposition.default`, " \
                  "shootoutInuse, otInUse, `clock.timeRemaining`, `clock.secondsRemaining`, `clock.running`, " \
                  "`clock.inIntermission`, displayPeriod, `gameOutcome.lastPeriodType`, " \
                  "`gameVideo.threeMinRecap`, regPeriods, `summary.awayTeamWins`, `summary.homeTeamWins`, " \
                  "`summary.neededToWin`, `summary.linescore.totals.away`, `summary.linescore.totals.home`, " \
                  "`summary.gameReports.gameSummary`, `summary.gameReports.eventSummary`, " \
                  "`summary.gameReports.playByPlay`, `summary.gameReports.faceoffSummary`, " \
                  "`summary.gameReports.faceoffComparison`, `summary.gameReports.rosters`, " \
                  "`summary.gameReports.shotSummary`, `summary.gameReports.shiftChart`, " \
                  "`summary.gameReports.toiAway`, `summary.gameReports.toiHome`, " \
                  "`summary.awayTeam.gameInfo.headCoach.default`, `summary.homeTeam.gameInfo.headCoach.default`) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row['gameId'], row['season'], row['gameType'], row['limitedScoring'], row['gameDate'],
                   row['venue.default'], row['venueLocation.default'], row['startTimeUTC'],
                   row['easternUTCOffset'], row['venueUTCOffset'], row['gameState'], row['gameScheduleState'],
                   row['periodDescriptor.number'], row['periodDescriptor.periodType'],
                   row['periodDescriptor.maxRegulationPeriods'], row['awayTeam.id'],
                   row['awayTeam.name.default'], row['awayTeam.abbrev'], row['awayTeam.score'],
                   row['awayTeam.sog'], row['awayTeam.logo'], row['awayTeam.placename.default'],
                   row['awayTeam.placenameWithPreposition.default'], row['homeTeam.id'],
                   row['homeTeam.name.default'], row['homeTeam.abbrev'], row['homeTeam.score'],
                   row['homeTeam.sog'], row['homeTeam.logo'], row['homeTeam.placename.default'],
                   row['homeTeam.placenameWithPreposition.default'], row['shootoutInuse'], row['otInUse'],
                   row['clock.timeRemaining'], row['clock.secondsRemaining'], row['clock.running'],
                   row['clock.inIntermission'], row['displayPeriod'], row['gameOutcome.lastPeriodType'],
                   row['gameVideo.threeMinRecap'], row['regPeriods'], row['summary.awayTeamWins'],
                   row['summary.homeTeamWins'], row['summary.neededToWin'], row['summary.linescore.totals.away'],
                   row['summary.linescore.totals.home'], row['summary.gameReports.gameSummary'],
                   row['summary.gameReports.eventSummary'], row['summary.gameReports.playByPlay'],
                   row['summary.gameReports.faceoffSummary'], row['summary.gameReports.faceoffComparison'],
                   row['summary.gameReports.rosters'], row['summary.gameReports.shotSummary'],
                   row['summary.gameReports.shiftChart'], row['summary.gameReports.toiAway'],
                   row['summary.gameReports.toiHome'], row['summary.awayTeam.gameInfo.headCoach.default'],
                   row['summary.homeTeam.gameInfo.headCoach.default'])

            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        if len(self.game_center_rr_df.index) > 0:
            row = self.game_center_rr_df.iloc[0]
            row = row.fillna('')

            cursor, db = db_import_login()

            sql = "insert into game_center_right_rail_import (gameId, `seasonSeriesWins.awayTeamWins`, " \
                  "`seasonSeriesWins.homeTeamWins`, `seasonSeriesWins.neededToWin`, " \
                  "`gameInfo.awayTeam.headCoach.default`, `gameInfo.homeTeam.headCoach.default`, " \
                  "`gameVideo.threeMinRecap`, `linescore.totals.away`, `linescore.totals.home`) " \
                  "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (row['gameId'], row['seasonSeriesWins.awayTeamWins'], row['seasonSeriesWins.homeTeamWins'],
                   row['seasonSeriesWins.neededToWin'], row['gameInfo.awayTeam.headCoach.default'],
                   row['gameInfo.homeTeam.headCoach.default'], row['gameVideo.threeMinRecap'],
                   row['linescore.totals.away'], row['linescore.totals.home'])

            cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        self.tv_broadcasts.updateDB()
        self.play_by_play.updateDB()
        self.roster_spots.updateDB()
        self.team_game_stats.updateDB()
        self.season_series.updateDB()
        self.referees.updateDB()
        self.linesmen.updateDB()
        self.scratches.updateDB()

        return True

    def clearDB(self):
        cursor, db = db_import_login()
        sql = "delete from game_center_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        sql = "delete from game_center_right_rail_import where gameId = " + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        self.tv_broadcasts.clearDB()
        self.play_by_play.clearDB()
        self.roster_spots.clearDB()
        self.team_game_stats.clearDB()
        self.season_series.clearDB()
        self.referees.clearDB()
        self.linesmen.clearDB()
        self.scratches.clearDB()

        return True

    def queryDB(self):
        cursor, db = db_import_login()

        pbp_sql = "select gameId, season, gameType, limitedScoring, gameDate, `venue.default`, " \
                  "`venueLocation.default`, startTimeUTC, easternUTCOffset, venueUTCOffset, gameState, " \
                  "gameScheduleState, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
                  "`periodDescriptor.maxRegulationPeriods`, `awayTeam.id`, `awayTeam.name.default`, " \
                  "`awayTeam.abbrev`, `awayTeam.score`, `awayTeam.sog`, `awayTeam.logo`, " \
                  "`awayTeam.placename.default`, `awayTeam.placenameWithPreposition.default`, `homeTeam.id`, " \
                  "`homeTeam.name.default`, `homeTeam.abbrev`, `homeTeam.score`, `homeTeam.sog`, `homeTeam.logo`, " \
                  "`homeTeam.placename.default`, `homeTeam.placenameWithPreposition.default`, shootoutInuse, " \
                  "otInUse, `clock.timeRemaining`, `clock.secondsRemaining`, `clock.running`, " \
                  "`clock.inIntermission`, displayPeriod, `gameOutcome.lastPeriodType`, `gameVideo.threeMinRecap`, " \
                  "regPeriods, `summary.awayTeamWins`, `summary.homeTeamWins`, `summary.neededToWin`, " \
                  "`summary.linescore.totals.away`, `summary.linescore.totals.home`, " \
                  "`summary.gameReports.gameSummary`, `summary.gameReports.eventSummary`, " \
                  "`summary.gameReports.playByPlay`, `summary.gameReports.faceoffSummary`, " \
                  "`summary.gameReports.faceoffComparison`, `summary.gameReports.rosters`, " \
                  "`summary.gameReports.shotSummary`, `summary.gameReports.shiftChart`, " \
                  "`summary.gameReports.toiAway`, `summary.gameReports.toiHome`, " \
                  "`summary.awayTeam.gameInfo.headCoach.default`, `summary.homeTeam.gameInfo.headCoach.default` " \
                  "from game_center_import where gameId = " + str(self.game_id)
        self.game_center_pbp_df = pd.read_sql(pbp_sql, db)
        self.game_center_pbp_df.fillna('', inplace=True)

        rr_sql = "select gameId, `seasonSeriesWins.awayTeamWins`, `seasonSeriesWins.homeTeamWins`, " \
                 "`seasonSeriesWins.neededToWin`, `gameInfo.awayTeam.headCoach.default`, " \
                 "`gameInfo.homeTeam.headCoach.default`, `gameVideo.threeMinRecap`, `linescore.totals.away`, " \
                 "`linescore.totals.home` from game_center_right_rail_import where gameId = " + str(self.game_id)
        self.game_center_rr_df = pd.read_sql(rr_sql, db)
        self.game_center_rr_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        self.tv_broadcasts.queryDB()
        self.play_by_play.queryDB()
        self.roster_spots.queryDB()
        self.team_game_stats.queryDB()
        self.season_series.queryDB()
        self.referees.queryDB()
        self.linesmen.queryDB()
        self.scratches.queryDB()

        return True

    def queryNHL(self):
        if self.game_id != '':
            url_prefix = 'https://api-web.nhle.com/v1/gamecenter/'

            pbp_suffix = '/play-by-play'
            pbp_query_url = "{}{}{}".format(url_prefix, self.game_id, pbp_suffix)
            self.pbp_json = fetch_json_data(pbp_query_url)
            game_center_pbp_df = pd.json_normalize(self.pbp_json)
            game_center_pbp_df.insert(0, 'gameId', self.game_id)
            self.game_center_pbp_df = self.game_center_pbp_df.head(0)
            self.game_center_pbp_df = pd.concat([self.game_center_pbp_df, game_center_pbp_df])
            self.game_center_pbp_df.fillna('', inplace=True)

            rr_suffix = '/right-rail'
            rr_query_url = "{}{}{}".format(url_prefix, self.game_id, rr_suffix)
            self.rr_json = fetch_json_data(rr_query_url)
            game_center_rr_df = pd.json_normalize(self.rr_json)
            game_center_rr_df.insert(0, 'gameId', self.game_id)
            self.game_center_rr_df = self.game_center_rr_df.head(0)
            self.game_center_rr_df = pd.concat([self.game_center_rr_df, game_center_rr_df])
            self.game_center_rr_df.fillna('', inplace=True)

            # in play-by-play
            if 'tvBroadcasts' in self.pbp_json:
                self.tv_broadcasts.json = self.pbp_json['tvBroadcasts']
                self.tv_broadcasts.queryNHL()

            if 'plays' in self.pbp_json:
                self.play_by_play.json = self.pbp_json['plays']
                self.play_by_play.queryNHL()

            if 'rosterSpots' in self.pbp_json:
                self.roster_spots.json = self.pbp_json['rosterSpots']
                self.roster_spots.queryNHL()

            # in right-rail
            if "teamGameStats" in self.rr_json:
                self.team_game_stats.json = self.rr_json['teamGameStats']
                self.team_game_stats.queryNHL()

            if "seasonSeries" in self.rr_json:
                self.season_series.json = self.rr_json['seasonSeries']
                self.season_series.queryNHL()

            if "referees" in self.rr_json['gameInfo']:
                self.referees.json = self.rr_json['gameInfo']['referees']
                self.referees.queryNHL()

            if "linesmen" in self.rr_json['gameInfo']:
                self.linesmen.json = self.rr_json['gameInfo']['linesmen']
                self.linesmen.queryNHL()

            if "scratches" in self.rr_json['gameInfo']['awayTeam']:
                self.scratches.json = self.rr_json['gameInfo']['awayTeam']['scratches'] + \
                                      self.rr_json['gameInfo']['homeTeam']['scratches']
                self.scratches.queryNHL()

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True
