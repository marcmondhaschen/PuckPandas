from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .games import GamesImport
from .games_import_log import GamesImportLog


class PlayByPlayImport:
    play_by_play_df = pd.DataFrame(columns=['eventId', 'timeInPeriod', 'timeRemaining', 'situationCode',
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
                                            'details.drawnByPlayerId', 'id'])

    def __init__(self, play_by_play_df=pd.DataFrame()):
        self.play_by_play_df = pd.concat([self.play_by_play_df, play_by_play_df])

    @staticmethod
    def updateDB(self, game_id):
        log = GamesImportLog(game_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), plays_found=1)
        log.insertDB(log)
        return True

    @staticmethod
    def clearDB(game_id=''):
        cursor, db = db_import_login()

        if game_id == '':
            sql = "truncate table teams_import"
        else:
            sql = "delete from teams_import where triCode = '" + tri_code + "'"

        print(sql)

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        return True

    def queryNHL(self, game_id):
        return True

    def queryNHLupdateDB(self, game_id):
        self.queryNHL(game_id)
        self.clearDB(game_id)
        self.updateDB(self, game_id)

        return True


class TvBroadcasts:
    tv_broadcasts_df = pd.DataFrame()

    def __init__(self, tv_broadcasts_df=pd.DataFrame()):
        self.tv_broadcasts_df = pd.concat([self.tv_broadcasts_df, tv_broadcasts_df])

    @staticmethod
    def updateDB(self, game_id):
        log = GamesImportLog(game_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), tv_broadcasts_found=1)
        log.insertDB(log)
        return True

    @staticmethod
    def clearDB(game_id):
        return True

    def queryDB(self):
        return True

    def queryNHL(self, game_id):
        return True

    def queryNHLupdateDB(self, game_id):
        self.queryNHL(game_id)
        self.clearDB(game_id)
        self.updateDB(self, game_id)

        return True


class GameResults:
    game_results_df = pd.DataFrame()

    def __init__(self, game_results_df=pd.DataFrame()):
        self.game_results_df = pd.concat([self.game_results_df, game_results_df])

    @staticmethod
    def updateDB(self, game_id):
        log = GamesImportLog(game_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), summary_found=1)
        log.insertDB(log)
        return True

    @staticmethod
    def clearDB(game_id):
        return True

    def queryDB(self):
        return True

    def queryNHL(self, game_id):
        return True

    def queryNHLupdateDB(self, game_id):
        self.queryNHL(game_id)
        self.clearDB(game_id)
        self.updateDB(self, game_id)

        return True


class GameRoster:
    game_roster_df = pd.DataFrame(columns=['teamId', 'playerId', 'sweaterNumber', 'positionCode',
                                           'headshot', 'firstName.default', 'lastName.default', 'id'])

    def __init__(self, game_roster_df=pd.DataFrame()):
        self.game_roster_df = pd.concat([self.game_roster_df, game_roster_df])

    @staticmethod
    def updateDB(self, game_id):
        log = GamesImportLog(game_id, datetime.today().strftime('%Y-%m-%d %H:%M:%S'), roster_spots_found=1)
        log.insertDB(log)
        return True

    @staticmethod
    def clearDB(game_id):
        return True

    def queryDB(self):
        return True

    def queryNHL(self, game_id):
        return True

    def queryNHLupdateDB(self, game_id):
        self.queryNHL(game_id)
        self.clearDB(game_id)
        self.updateDB(self, game_id)

        return True


class GameCenterImport:
    games = GamesImport()
    playByPlay = PlayByPlayImport()
    tvBroadcasts = TvBroadcasts()
    gameResults = GameResults()
    gameRoster = GameRoster()

    def __init__(self, games=GamesImport(), play_by_play=PlayByPlayImport(), tv_broadcasts=TvBroadcasts(),
                 game_results=GameResults(), game_roster=GameRoster()):
        self.games = games
        self.playByPlay = play_by_play
        self.tvBroadcasts = tv_broadcasts
        self.gameResults = game_results
        self.gameRoster = game_roster

    @staticmethod
    def updateDB(self, game_id=''):
        return True

    @staticmethod
    def clearDB(self, game_id=''):
        return True

    def queryDB(self):
        return True

    def queryNHL(self, game_id=''):
        return True

    def queryNHLupdateDB(self, game_id):
        self.queryNHL(game_id)
        self.clearDB(game_id)
        self.updateDB(self, game_id)

        return True


def fetch_gameids_to_query():
    gameids_sql = 'select distinct gameId from games_import where gameDate < date_sub(sysdate(), INTERVAL 2 DAY) ' \
                  'and (PBPCheckSuccess is null or PBPCheckSuccess = 0) order by gameDate desc, gameId'
    cursor, db = db_import_login()
    gameids_df = pd.read_sql(gameids_sql, db)

def fetch_game_details(gameids_df):
    if len(gameids_df) == 0:
        return False

    pbp_master_df = master_pbp_frame()
    gr_master_df = master_gr_frame()

    for index, row in gameids_df.iterrows():
        url_prefix = 'https://api-web.nhle.com/v1/gamecenter/'
        url_suffix = '/play-by-play'
        query_url = "{}{}{}".format(url_prefix, row['gameId'], url_suffix)

        json_data = fetch_json_data(query_url)

        if 'plays' in json_data:
            play_by_play_df = pd.json_normalize(json_data, record_path=['plays'], meta=['id'])
            pbp_master_df = pd.concat([pbp_master_df, play_by_play_df])
            pbp_master_df = transform_play_by_play(pbp_master_df)

        if 'rosterSpots' in json_data:
            game_roster_df = pd.json_normalize(json_data, record_path=['rosterSpots'], meta=['id'])
            gr_master_df = pd.concat([gr_master_df, game_roster_df])
            gr_master_df = transform_game_rosters(gr_master_df)

        if load_pbp_details(pbp_master_df):
            pbp_master_df = pbp_master_df.head(0)
        if load_roster_details(gr_master_df):
            gr_master_df = gr_master_df.head(0)

    return True

def load_pbp_details(pbp_df):
   for index, row in pbp_df.iterrows():
        sql = "insert into play_by_play_import (gameId, eventId, period, periodType, timeInPeriod, " \
              "timeRemaining, situationCode, typeCode, typeDescKey, sortOrder, eventOwnerTeamId, losingPlayerId,  " \
              "winningPlayerId, xCoord, yCoord, zoneCode, reason, hittingPlayerId, hitteePlayerId, shotType, " \
              "shootingPlayerId, goalieInNetId, awaySOG, homeSOG, playerId, blockingPlayerId, secondaryReason, " \
              "detailTypeCode, detailDescKey, detailDuration, detailCommittedByPlayerId, detailDrawnByPlayerId, " \
              "scoringPlayerId, scoringPlayerTotal, assist1PlayerId, assist1PlayerTotal, assist2PlayerId, " \
              "assist2PlayerTotal, awayScore, homeScore) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s)"
        val = (row['id'], row['eventId'], row['periodDescriptor.number'], row['periodDescriptor.periodType'],
               row['timeInPeriod'], row['timeRemaining'], row['situationCode'], row['typeCode'], row['typeDescKey'],
               row['sortOrder'], row['details.eventOwnerTeamId'], row['details.losingPlayerId'],
               row['details.winningPlayerId'], row['details.xCoord'], row['details.yCoord'], row['details.zoneCode'],
               row['details.reason'], row['details.hittingPlayerId'], row['details.hitteePlayerId'],
               row['details.shotType'], row['details.shootingPlayerId'], row['details.goalieInNetId'],
               row['details.awaySOG'], row['details.homeSOG'], row['details.playerId'], row['details.blockingPlayerId'],
               row['details.secondaryReason'], row['details.typeCode'], row['details.descKey'],
               row['details.duration'], row['details.committedByPlayerId'], row['details.drawnByPlayerId'],
               row['details.scoringPlayerId'], row['details.scoringPlayerTotal'], row['details.assist1PlayerId'],
               row['details.assist1PlayerTotal'], row['details.assist2PlayerId'], row['details.assist2PlayerTotal'],
               row['details.awayScore'], row['details.homeScore'])

def load_roster_details(gr_df):
    for index, row in gr_df.iterrows():
        sql = "insert into game_rosters_import (gameId, teamId, playerId, sweaterNumber, positionCode, " \
              "`firstName.default`,`lastName.default`) values (%s, %s, %s, %s, %s, %s, %s)"
        val = (row['id'], row['teamId'], row['playerId'], row['sweaterNumber'], row['positionCode'],
               row['firstName.default'], row['lastName.default'])
        cursor.execute(sql, val)