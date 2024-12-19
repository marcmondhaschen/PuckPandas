from datetime import datetime, timezone
import pandas as pd
import nhlpd

""" shift details first appear in the NHL's API set in the 20102011 season """


class ShiftsImport:
    def __init__(self, game_id):
        self.shifts_df = pd.DataFrame(columns=['id', 'detailCode', 'duration', 'endTime', 'eventDescription',
                                               'eventDetails', 'eventNumber', 'firstName', 'gameId', 'hexValue',
                                               'lastName', 'period', 'playerId', 'shiftNumber', 'startTime',
                                               'teamAbbrev', 'teamId', 'teamName', 'typeCode'])
        self.game_id = game_id

    def updateDB(self):
        cursor, db = nhlpd.db_import_login()

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

            log = nhlpd.GamesImportLog(game_id=row['id'],
                                       last_date_updated=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                                       shifts_found=1)
            log.updateDB()

        db.commit()
        cursor.close()
        db.close()

        return True

    def clearDB(self):
        cursor, db = nhlpd.db_import_login()
        sql = "delete from shifts_import where game_id =" + str(self.game_id)
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

        return True

    def queryDB(self):
        cursor, db = nhlpd.db_import_login()
        sql = "select id, detailCode, duration, endTime, eventDescription, eventDetails, eventNumber, firstName, " \
              "gameId, hexValue, lastName, period, playerId, shiftNumber, startTime, teamAbbrev, teamId, teamName, " \
              "typeCode from shifts_import where gameId = " + str(self.game_id)
        shifts_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        self.shifts_df = self.shifts_df.head(0)
        self.shifts_df = pd.concat([self.shifts_df, shifts_df])
        self.shifts_df.fillna('', inplace=True)

        return True

    def queryNHL(self):
        url_prefix = 'https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId='
        url_string = "{}{}".format(url_prefix, self.game_id)
        json_data = nhlpd.fetch_json_data(url_string)

        if len(json_data['data']) > 0:
            shifts_df = pd.json_normalize(json_data, record_path=['data'])
            self.shifts_df = self.shifts_df.head(0)
            self.shifts_df = pd.concat([self.shifts_df, shifts_df])
            self.shifts_df.fillna('', inplace=True)

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB()

        return True
