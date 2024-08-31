from datetime import datetime
import pandas as pd
import time
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .seasons import SeasonsImport
from .import_table_update_log import ImportTableUpdateLog
from .games_import_log import GamesImportLog


class SchedulesImport:
    schedules_df = pd.DataFrame(columns=['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite',
                                         'startTimeUTC', 'venueUTCOffset', 'venueTimezone', 'gameState',
                                         'gameScheduleState', 'awayTeam', 'awayTeamSplitSquad', 'awayTeamScore',
                                         'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore', 'periodType',
                                         'gameOutcome'])

    def __init__(self, schedules_df=pd.DataFrame()):
        self.schedules_df = pd.concat([self.schedules_df, schedules_df])

    @staticmethod
    def updateDB(self, tri_code='', season_id=''):
        if len(self.schedules_df) > 0:
            cursor, db = db_import_login()

            if tri_code != '':
                self.schedules_df = self.schedules_df[self.schedules_df['triCode'] == tri_code]

            if season_id != '':
                self.schedules_df = self.schedules_df[self.schedules_df['seasonId'] == season_id]

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

                log = GamesImportLog()

            db.commit()
            cursor.close()
            db.close()

        log_object = ImportTableUpdateLog("games_import", datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 1)
        log_object.updateDB(log_object)

        return True

    @staticmethod
    def clearDB(tri_code='', season_id=''):
        cursor, db = db_import_login()

        if tri_code == '' and season_id == '':
            sql = "truncate table games_import"
        else:
            sql_prefix = "delete from games_import where gameId > 0 "
            sql_middle = ""
            sql_suffix = ""
            if tri_code != '':
                sql_middle = "and triCode = " + tri_code + " "
            if season_id != '':
                sql_suffix = "and seasonId = " + season_id + " "
            sql = "{}{}{}".format(sql_prefix, sql_middle, sql_suffix)
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self, tri_code='', season_id=''):
        sql_prefix = "select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, venueUTCOffset, " \
                     "venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, awayTeamScore, " \
                     "homeTeam, homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome from games_import where " \
                     "gameId > 0 "
        sql_middle = ""
        sql_suffix = ""

        if tri_code != '':
            sql_middle = "and  triCode = " + tri_code + " "

        if season_id != '':
            sql_suffix = "and seasonId = " + season_id + " "

        sql = "{}{}{}".format(sql_prefix, sql_middle, sql_suffix)

        cursor, db = db_import_login()
        schedules_df = pd.read_sql(sql, db)
        self.schedules_df = schedules_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self, tri_code='', season_id=''):
        seasons = SeasonsImport()
        seasons.queryDB()

        if tri_code != '':
            seasons.seasons_df = seasons.seasons_df[seasons.seasons_df['triCode'] == tri_code]

        if season_id != '':
            seasons.seasons_df = seasons.seasons_df[seasons.seasons_df['seasonId'] == season_id]

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

    def queryNHLupdateDB(self, tri_code='', season_id=''):
        self.queryNHL(tri_code, season_id)
        self.clearDB(tri_code, season_id)
        self.updateDB(self, tri_code, season_id)

        return True
