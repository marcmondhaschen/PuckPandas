import pandas as pd
import time
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .seasons import SeasonsImport


class SchedulesImport:
    schedules_df = pd.DataFrame(columns=['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite',
                                         'startTimeUTC', 'venueUTCOffset', 'venueTimezone', 'gameState',
                                         'gameScheduleState', 'awayTeam', 'awayTeamSplitSquad', 'awayTeamScore',
                                         'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore', 'periodType',
                                         'gameOutcome'])

    def __init__(self, schedules_df=pd.DataFrame()):
        self.schedules_df = pd.concat([self.schedules_df, schedules_df])

    @staticmethod
    def updateDB(self):
        if len(self.schedules_df) > 0:
            cursor, db = db_import_login()

            for index, row in self.schedules_df.iterrows():
                sql = "insert into games_import (gameId, seasonId, gameType, gameDate, venue, neutralSite, " \
                      "startTimeUTC, venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, " \
                      "awayTeamSplitSquad, awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, " \
                      "periodType, gameOutcome) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                      "%s, %s, %s, %s)"
                val = (row['id'], row['season'], row['gameType'], row['gameDate'], row['venue.default'],
                       row['neutralSite'], row['startTimeUTC'], row['venueUTCOffset'], row['venueTimezone'],
                       row['gameState'], row['gameScheduleState'], row['awayTeam.id'], row['awayTeam.awaySplitSquad'],
                       row['awayTeam.score'], row['homeTeam.id'], row['homeTeam.homeSplitSquad'], row['homeTeam.score'],
                       row['periodDescriptor.periodType'], row['gameOutcome.lastPeriodType'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        return True

    @staticmethod
    def clearDB():
        cursor, db = db_import_login()

        sql = "truncate table games_import"
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self):
        schedules_sql = "select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, " \
                        "venueUTCOffset, venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, " \
                        "awayTeamScore, homeTeam, homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome from " \
                        "games_import"

        cursor, db = db_import_login()
        schedules_df = pd.read_sql(schedules_sql, db)
        self.schedules_df = schedules_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self):
        cursor, db = db_import_login()

        seasons = SeasonsImport()
        seasons.queryDB()

        db.commit()
        cursor.close()
        db.close()

        schedules_df = pd.DataFrame()

        for index, row in seasons.seasons_df.iterrows():
            base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
            query_string = "{}{}/{}".format(base_url, row['triCode'], row['seasonId'])
            json_data = fetch_json_data(query_string)

            if 'games' in json_data:
                team_schedule_df = pd.json_normalize(json_data, record_path=['games'])
                if 'tvBroadcasts' in team_schedule_df:
                    team_schedule_df.drop(columns='tvBroadcasts', inplace=True)
                team_schedule_df.fillna('', inplace=True)
                schedules_df = pd.concat([schedules_df, team_schedule_df])

            time.sleep(0.25)

        schedules_df.drop_duplicates(inplace=True)
        schedules_df.fillna('', inplace=True)
        schedules_df.dropna(axis=1, inplace=True)
        self.schedules_df = schedules_df

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)

        return True
