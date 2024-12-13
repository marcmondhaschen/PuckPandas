from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .games import GamesImport
from .games_import_log import GamesImportLog

""" shift details first appear in the NHL's API set in the 20102011 season """


class ShiftsImport:
    shifts_df = pd.DataFrame(columns=['id', 'detailCode', 'duration', 'endTime', 'eventDescription', 'eventDetails',
                                      'eventNumber', 'firstName', 'gameId', 'hexValue', 'lastName', 'period',
                                      'playerId', 'shiftNumber', 'startTime', 'teamAbbrev', 'teamId', 'teamName',
                                      'typeCode'])

    def __init__(self, shifts_df=pd.DataFrame()):
        self.shifts_df = pd.concat([self.shifts_df, shifts_df])

    def updateDB(self):
        cursor, db = db_import_login()

        for index, row in self.shifts_df.iterrows():
            sql = 'insert into shifts_import (id, detailCode, duration, endTime, eventDescription, eventDetails, ' \
                  'eventNumber, firstName, gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, ' \
                  'teamAbbrev, teamId, teamName, typeCode) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
                  '%s, %s, %s, %s, %s, %s, %s)'
            val = [row['id'], row['detailCode'], row['duration'], row['endTime'], row['eventDescription'],
                   row['eventDetails'], row['eventNumber'], row['firstName'], row['gameId'], row['hexValue'],
                   row['lastName'], row['period'], row['playerId'], row['shiftNumber'], row['startTime'],
                   row['teamAbbrev'], row['teamId'], row['teamName'], row['typeCode']]
            cursor.execute(sql, val)

            log = GamesImportLog(game_id=row['id'], last_date_updated=datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                                 shifts_found=1)
            log.updateDB()

        # tidy up the cursors
        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def clearDB(game_id=''):
        cursor, db = db_import_login()

        if game_id == '':
            sql = "truncate table shifts_import"
        else:
            sql = "delete from shifts_import where game_id =" + str(game_id)
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self, gameid='', playerid='', teamid=''):
        shifts_sql = "select id, detailCode, duration, endTime, eventDescription, eventDetails, eventNumber, " \
                     "firstName, gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, teamAbbrev, " \
                     "teamId, teamName, typeCode from shifts_import where id > 0 "

        gameid_sql = playerid_sql = teamid_sql = ''

        if gameid != '':
            gameid_sql = "and gameId = " + gameid + " "
        if playerid != '':
            playerid_sql = "and playerId = " + playerid + " "
        if teamid != '':
            teamid_sql = "and teamId = " + teamid + " "

        shifts_sql = "{}{}{}{}".format(shifts_sql, gameid_sql, playerid_sql, teamid_sql)

        cursor, db = db_import_login()
        shifts_df = pd.read_sql(shifts_sql, db)
        self.shifts_df = shifts_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self, game_id=''):
        schedules = GamesImport()
        schedules.queryDB()

        if game_id != '':
            self.shifts_df = self.shifts_df[self.shifts_df['id'] == game_id]

        if len(schedules.games_df) == 0:
            return False

        for index, row in schedules.games_df.iterrows():
            game_id = row['gameId']

            url_prefix = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId='
            url_string = "{}{}".format(url_prefix, game_id)
            json_data = fetch_json_data(url_string)

            if len(json_data['data']) > 0:
                shifts_df = pd.json_normalize(json_data, record_path=['data'])
                shifts_df.fillna('', inplace=True)

                self.shifts_df = pd.concat([self.shifts_df, shifts_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True
