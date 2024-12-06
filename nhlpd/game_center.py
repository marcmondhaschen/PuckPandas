import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class ScratchesImport:
    game_id = ''
    scratches_df = pd.DataFrame(columns=['gameId', 'playerId', 'firstName.default', 'lastName.default'])
    json = {}

    def __init__(self, game_id='', scratches_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.scratches_df = pd.concat([self.scratches_df, scratches_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table scratches_import"
        else:
            sql = "delete from scratches_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, playerId, `firstName.default`, `lastName.default` from scratches_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.scratches_df = pd.read_sql(sql, db)
        self.scratches_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        scratches_df = pd.json_normalize(self.json)
        scratches_df.fillna('', inplace=True)
        scratches_df.rename(columns={"id": "playerId"}, inplace=True)

        if self.game_id != '':
            scratches_df.insert(0, 'gameId', self.game_id)

        self.scratches_df = pd.concat([self.scratches_df, scratches_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class LinesmenImport:
    game_id = ''
    linesmen_df = pd.DataFrame(columns=['gameId', 'default'])
    json = {}

    def __init__(self, game_id='', linesmen_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.linesmen_df = pd.concat([self.linesmen_df, linesmen_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table linesmen_import"
        else:
            sql = "delete from linesmen_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, `default` from linesmen_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.linesmen_df = pd.read_sql(sql, db)
        self.linesmen_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        linesmen_df = pd.json_normalize(self.json)
        linesmen_df.fillna('', inplace=True)

        if self.game_id != '':
            linesmen_df.insert(0, 'gameId', self.game_id)

        self.linesmen_df = pd.concat([self.linesmen_df, linesmen_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class RefereesImport:
    game_id = ''
    referees_df = pd.DataFrame(columns=['gameId', 'default'])
    json = {}

    def __init__(self, game_id='', referees_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.referees_df = pd.concat([self.referees_df, referees_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table referees_import"
        else:
            sql = "delete from referees_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, `default` from referees_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.referees_df = pd.read_sql(sql, db)
        self.referees_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        referees_df = pd.json_normalize(self.json)
        referees_df.fillna('', inplace=True)

        if self.game_id != '':
            referees_df.insert(0, 'gameId', self.game_id)

        self.referees_df = pd.concat([self.referees_df, referees_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class SeasonSeriesImport:
    game_id = ''
    season_series_df = pd.DataFrame(columns=['gameId', 'seriesNumber', 'refGameId'])
    json = {}

    def __init__(self, game_id='', season_series_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.season_series_df = pd.concat([self.season_series_df, season_series_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table season_series_import"
        else:
            sql = "delete from season_series_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, seriesNumber, refGameId from season_series_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.season_series_df = pd.read_sql(sql, db)
        self.season_series_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        season_series_df = pd.json_normalize(self.json)
        season_series_df.fillna('', inplace=True)
        # noinspection PyTypeChecker
        season_series_df.insert(0, 'seriesNumber', range(len(season_series_df)))
        season_series_df.rename(columns={"id": "refGameId"}, inplace=True)

        if self.game_id != '':
            season_series_df.insert(0, 'gameId', self.game_id)

        self.season_series_df = pd.concat([self.season_series_df, season_series_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class TeamGameStatsImport:
    game_id = ''
    team_game_stats_df = pd.DataFrame(columns=['gameId', 'category', 'awayValue', 'homeValue'])
    json = {}

    def __init__(self, game_id='', team_game_stats_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.team_game_stats_df = pd.concat([self.team_game_stats_df, team_game_stats_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table team_game_stats_import"
        else:
            sql = "delete from team_game_stats_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, category, awayValue, homeValue from team_game_stats_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.team_game_stats_df = pd.read_sql(sql, db)
        self.team_game_stats_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        team_game_stats_df = pd.json_normalize(self.json)
        team_game_stats_df.fillna('', inplace=True)

        if self.game_id != '':
            team_game_stats_df.insert(0, 'gameId', self.game_id)

        self.team_game_stats_df = pd.concat([self.team_game_stats_df, team_game_stats_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class RosterSpotsImport:
    game_id = ''
    roster_spots_df = pd.DataFrame(columns=['gameId', 'teamId', 'playerId', 'sweaterNumber', 'positionCode', 'headshot',
                                            'firstName', 'lastName'])
    json = {}

    def __init__(self, game_id='', roster_spots_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.roster_spots_df = pd.concat([self.roster_spots_df, roster_spots_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table roster_spots_import"
        else:
            sql = "delete from roster_spots_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, teamId, playerId, sweaterNumber, positionCode, headshot, `firstName`, " \
                     "`lastName` from roster_spots_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.roster_spots_df = pd.read_sql(sql, db)
        self.roster_spots_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        roster_spots_df = pd.json_normalize(self.json)
        roster_spots_df = roster_spots_df.fillna('')

        if self.game_id != '':
            roster_spots_df.insert(0, 'gameId', self.game_id)

        self.roster_spots_df = pd.concat([self.roster_spots_df, roster_spots_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class PlaysImport:
    game_id = ''
    plays_df = pd.DataFrame(columns=['gameId', 'eventId', 'timeInPeriod', 'timeRemaining', 'situationCode',
                                     'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder',
                                     'periodDescriptor.number', 'periodDescriptor.periodType',
                                     'details.eventOwnerTeamId', 'details.losingPlayerId', 'details.winningPlayerId',
                                     'details.xCoord', 'details.yCoord', 'details.zoneCode', 'details.shotType',
                                     'details.shootingPlayerId', 'details.goalieInNetId', 'details.awaySOG',
                                     'details.homeSOG', 'details.reason', 'details.playerId',
                                     'details.hittingPlayerId', 'details.hitteePlayerId', 'details.scoringPlayerId',
                                     'details.scoringPlayerTotal', 'details.assist1PlayerId',
                                     'details.assist1PlayerTotal', 'details.assist2PlayerId',
                                     'details.assist2PlayerTotal', 'details.awayScore', 'details.homeScore',
                                     'details.blockingPlayerId', 'details.secondaryReason', 'details.typeCode',
                                     'details.descKey', 'details.duration', 'details.committedByPlayerId',
                                     'details.drawnByPlayerId'])
    json = {}

    def __init__(self, game_id='', plays_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.plays_df = pd.concat([self.plays_df, plays_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

    def updateDB(self):
        if len(self.plays_df.index) > 0:
            cursor, db = db_import_login()

            for index, row in self.plays_df.iterrows():
                sql = "insert into plays_import (gameId, eventId, period, periodType, timeInPeriod, timeRemaining, "\
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

        if self.game_id == '':
            sql = "truncate table plays_import"
        else:
            sql = "delete from plays_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, eventId, period, periodType, timeInPeriod, timeRemaining, situationCode, " \
                     "typeCode, typeDescKey, sortOrder, eventOwnerTeamId, losingPlayerId,  winningPlayerId, xCoord, " \
                     "yCoord, zoneCode, reason, hittingPlayerId, hitteePlayerId, shotType, shootingPlayerId, " \
                     "goalieInNetId, awaySOG, homeSOG, playerId, blockingPlayerId, secondaryReason, detailTypeCode, " \
                     "detailDescKey, detailDuration, detailCommittedByPlayerId, detailDrawnByPlayerId, " \
                     "scoringPlayerId, scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, assist2PlayerId, " \
                     "assist2PlayerTotal, awayScore, homeScore from plays_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.plays_df = pd.read_sql(sql, db)
        self.plays_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        plays_df = pd.json_normalize(self.json)
        plays_df.fillna('', inplace=True)

        if self.game_id != '':
            plays_df.insert(0, 'gameId', self.game_id)

        self.plays_df = pd.concat([self.plays_df, plays_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class TvBroadcastsImport:
    game_id = ''
    tv_broadcasts_df = pd.DataFrame(columns=['gameId', 'broadcastId', 'market', 'countryCode', 'network',
                                             'sequenceNumber'])
    json = {}

    def __init__(self, game_id='', tv_broadcasts_df=pd.DataFrame(), json=None):
        self.game_id = game_id
        self.tv_broadcasts_df = pd.concat([self.tv_broadcasts_df, tv_broadcasts_df])
        if json is None:
            self.json = {}
        else:
            self.json = json

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

        if self.game_id == '':
            sql = "truncate table tv_broadcasts_import"
        else:
            sql = "delete from tv_broadcasts_import where gameId = " + str(self.game_id)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        sql_prefix = "select gameId, broadcastId, market, countryCode, network, sequenceNumber from " \
                     "tv_broadcasts_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()
        self.tv_broadcasts_df = pd.read_sql(sql, db)
        self.tv_broadcasts_df.fillna('', inplace=True)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        tv_broadcasts_df = pd.json_normalize(self.json)
        tv_broadcasts_df.fillna('', inplace=True)
        tv_broadcasts_df.rename(columns={"id": "broadcastId"}, inplace=True)

        if self.game_id != '':
            tv_broadcasts_df.insert(0, 'gameId', self.game_id)

        self.tv_broadcasts_df = pd.concat([self.tv_broadcasts_df, tv_broadcasts_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True


class GameCenterImport:
    game_id = ''
    game_center_pbp_df = pd.DataFrame(columns=['gameId', 'season', 'gameType', 'limitedScoring', 'gameDate',
                                               'venue.default', 'venueLocation.default', 'startTimeUTC',
                                               'easternUTCOffset', 'venueUTCOffset', 'gameState', 'gameScheduleState',
                                               'periodDescriptor.number', 'periodDescriptor.periodType',
                                               'periodDescriptor.maxRegulationPeriods', 'awayTeam.id',
                                               'awayTeam.name.default', 'awayTeam.abbrev', 'awayTeam.score',
                                               'awayTeam.sog', 'awayTeam.logo', 'awayTeam.placename.default',
                                               'awayTeam.placenameWithPreposition.default', 'homeTeam.id',
                                               'homeTeam.name.default', 'homeTeam.abbrev', 'homeTeam.score',
                                               'homeTeam.sog', 'homeTeam.logo', 'homeTeam.placename.default',
                                               'homeTeam.placenameWithPreposition.default', 'shootoutInuse', 'otInUse',
                                               'clock.timeRemaining', 'clock.secondsRemaining', 'clock.running',
                                               'clock.inIntermission', 'displayPeriod', 'gameOutcome.lastPeriodType',
                                               'gameVideo.threeMinRecap', 'regPeriods', 'summary.awayTeamWins',
                                               'summary.homeTeamWins', 'summary.neededToWin',
                                               'summary.linescore.totals.away', 'summary.linescore.totals.home',
                                               'summary.gameReports.gameSummary', 'summary.gameReports.eventSummary',
                                               'summary.gameReports.playByPlay', 'summary.gameReports.faceoffSummary',
                                               'summary.gameReports.faceoffComparison', 'summary.gameReports.rosters',
                                               'summary.gameReports.shotSummary', 'summary.gameReports.shiftChart',
                                               'summary.gameReports.toiAway', 'summary.gameReports.toiHome',
                                               'summary.awayTeam.gameInfo.headCoach.default',
                                               'summary.homeTeam.gameInfo.headCoach.default'])
    pbp_json = {}

    game_center_rr_df = pd.DataFrame(columns=['gameId', 'seasonSeriesWins.awayTeamWins',
                                              'seasonSeriesWins.homeTeamWins', 'seasonSeriesWins.neededToWin',
                                              'gameInfo.awayTeam.headCoach.default',
                                              'gameInfo.homeTeam.headCoach.default', 'gameVideo.threeMinRecap',
                                              'linescore.totals.away', 'linescore.totals.home'])
    rr_json = {}

    tv_broadcasts = TvBroadcastsImport()
    play_by_play = PlaysImport()
    roster_spots = RosterSpotsImport()
    team_game_stats = TeamGameStatsImport()
    season_series = SeasonSeriesImport()
    referees = RefereesImport()
    linesmen = LinesmenImport()
    scratches = ScratchesImport()

    def __init__(self, game_id, game_center_pbp_df=pd.DataFrame(), game_center_rr_df=pd.DataFrame(), pbp_json=None,
                 rr_json=None, tv_broadcasts=TvBroadcastsImport(), plays=PlaysImport(),
                 roster_spots=RosterSpotsImport(), team_game_stats=TeamGameStatsImport(),
                 season_series=SeasonSeriesImport(), referees=RefereesImport(), linesmen=LinesmenImport(),
                 scratches=ScratchesImport()):
        self.game_id = game_id
        self.game_center_pbp_df = pd.concat([self.game_center_pbp_df, game_center_pbp_df])
        self.game_center_rr_df = pd.concat([self.game_center_rr_df, game_center_rr_df])

        if pbp_json is None:
            self.pbp_json = {}
        else:
            self.pbp_json = pbp_json

        if rr_json is None:
            self.rr_json = {}
        else:
            self.rr_json = rr_json

        self.tv_broadcasts = tv_broadcasts
        self.play_by_play = plays
        self.roster_spots = roster_spots
        self.team_game_stats = team_game_stats
        self.season_series = season_series
        self.referees = referees
        self.linesmen = linesmen
        self.scratches = scratches

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

        if self.game_id != '':
            sql = "delete from game_center_import where gameId = " + str(self.game_id)
            cursor.execute(sql)

        if self.game_id != '':
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
        sql_prefix = "select gameId, season, gameType, limitedScoring, gameDate, `venue.default`, " \
                     "`venueLocation.default`, startTimeUTC, easternUTCOffset, venueUTCOffset, gameState, " \
                     "gameScheduleState, `periodDescriptor.number`, `periodDescriptor.periodType`, " \
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
                     "`summary.awayTeam.gameInfo.headCoach.default`, `summary.homeTeam.gameInfo.headCoach.default` " \
                     "from game_center_import "
        sql_suffix = ""

        if self.game_id != '':
            sql_suffix = "where gameId = " + str(self.game_id)

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = db_import_login()

        self.game_center_pbp_df = pd.read_sql(sql, db)
        self.game_center_pbp_df.fillna('', inplace=True)

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
            rr_suffix = '/right-rail'
            rr_query_url = "{}{}{}".format(url_prefix, self.game_id, rr_suffix)

            self.pbp_json = fetch_json_data(pbp_query_url)
            game_center_pbp_df = pd.json_normalize(self.pbp_json)
            game_center_pbp_df.fillna('', inplace=True)
            game_center_pbp_df.insert(0, 'gameId', self.game_id)
            self.game_center_pbp_df = pd.concat([self.game_center_pbp_df, game_center_pbp_df])

            self.rr_json = fetch_json_data(rr_query_url)
            game_center_rr_df = pd.json_normalize(self.rr_json)
            game_center_rr_df.fillna('', inplace=True)
            game_center_rr_df.insert(0, 'gameId', self.game_id)
            self.game_center_rr_df = pd.concat([self.game_center_rr_df, game_center_rr_df])

            # in play-by-play
            if 'tvBroadcasts' in self.pbp_json:
                self.tv_broadcasts.json = self.pbp_json['tvBroadcasts']
                self.tv_broadcasts.game_id = self.game_id
                self.tv_broadcasts.queryNHL()

            if 'plays' in self.pbp_json:
                self.play_by_play.json = self.pbp_json['plays']
                self.play_by_play.game_id = self.game_id
                self.play_by_play.queryNHL()

            if 'rosterSpots' in self.pbp_json:
                self.roster_spots.json = self.pbp_json['rosterSpots']
                self.roster_spots.game_id = self.game_id
                self.roster_spots.queryNHL()

            # in right-rail
            if "teamGameStats" in self.rr_json:
                self.team_game_stats.json = self.rr_json['teamGameStats']
                self.team_game_stats.game_id = self.game_id
                self.team_game_stats.queryNHL()

            if "seasonSeries" in self.rr_json:
                self.season_series.json = self.rr_json['seasonSeries']
                self.season_series.game_id = self.game_id
                self.season_series.queryNHL()

            if "referees" in self.rr_json['gameInfo']:
                self.referees.json = self.rr_json['gameInfo']['referees']
                self.referees.game_id = self.game_id
                self.referees.queryNHL()

            if "linesmen" in self.rr_json['gameInfo']:
                self.linesmen.json = self.rr_json['gameInfo']['linesmen']
                self.linesmen.game_id = self.game_id
                self.linesmen.queryNHL()

            if "scratches" in self.rr_json['gameInfo']['awayTeam']:
                self.scratches.json = self.rr_json['gameInfo']['awayTeam']['scratches'] + \
                                      self.rr_json['gameInfo']['homeTeam']['scratches']
                self.scratches.game_id = self.game_id
                self.scratches.queryNHL()

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True
