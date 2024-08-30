from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .schedules import SchedulesImport

""" shift details first appear in the NHL's API set in the 20102011 season """

class ShiftsImport:
    shifts_df = pd.DataFrame(columns=['id', 'detailCode', 'duration', 'endTime', 'eventDescription', 'eventDetails',
                                      'eventNumber', 'firstName', 'gameId', 'hexValue', 'lastName', 'period',
                                      'playerId', 'shiftNumber', 'startTime', 'teamAbbrev', 'teamId', 'teamName',
                                      'typeCode'])

    def __init__(self, shifts_df=pd.DataFrame()):
        self.shifts_df = pd.concat([self.shifts_df, shifts_df])

    @staticmethod
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

        # tidy up the cursors
        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def clearDB():
        cursor, db = db_import_login()

        sql = "truncate table shifts_import"
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

    def queryNHL(self, gameid=''):
        schedules = SchedulesImport()
        schedules.queryDB()

        if len(schedules.schedules_df) == 0:
            return False

        for index, row in schedules.schedules_df.iterrows():
            game_id = row['gameId']
            shifts_load_check = False

            url_prefix = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId='
            url_string = "{}{}".format(url_prefix, game_id)
            json_data = fetch_json_data(url_string)

            if len(json_data['data']) > 0:
                shifts_df = pd.json_normalize(json_data, record_path=['data'])
                master_shifts_df = master_shift_frame()
                shifts_df = pd.concat([shifts_df, master_shifts_df])
                shifts_df = transform_shifts_frame(shifts_df)
                shifts_load_check = load_shifts_frame(shifts_df)

            log_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            log_df = pd.DataFrame(data=[[game_id, log_date, shifts_load_check]],
                                  columns=['gameId', 'logDate', 'checked'])
            log_df = log_df.fillna('')
            # update_shift_log(log_df)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)

        return True


def update_shift_log(log_df):
    """
    Logs when each game's shifts are recorded.

    Parameters: log_df - a DataFrame with a set of gameIds and their boolean checked/unchecked status

    Returns: True - returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in log_df.iterrows():
        sql = "insert into shift_import_log (gameId, logDate, checked) values (%s, %s, %s)"
        val = [row['gameId'], row['logDate'], row['checked']]

        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True