from datetime import datetime
import pandas as pd
import time
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .seasons import SeasonsImport
from .teams import TeamsImport
from .import_table_update_log import ImportTableUpdateLog
from .games_import_log import GamesImportLog


class GamesImport:
    games_df = pd.DataFrame(columns=['gameId', 'seasonId', 'gameType', 'gameDate', 'venue', 'neutralSite',
                                     'startTimeUTC', 'venueUTCOffset', 'venueTimezone', 'gameState',
                                     'gameScheduleState', 'awayTeam', 'awayTeamSplitSquad', 'awayTeamScore',
                                     'homeTeam', 'homeTeamSplitSquad', 'homeTeamScore', 'periodType', 'gameOutcome'])

    def __init__(self, games_df=pd.DataFrame()):
        self.games_df = pd.concat([self.games_df, games_df])

    @staticmethod
    def updateDB(self, tri_code='', season_id=''):
        teams = TeamsImport()
        teams.queryDB()

        if len(self.games_df) > 0:
            cursor, db = db_import_login()

            if tri_code != '':
                team_id = teams.teams_df[teams.teams_df['triCode'] == tri_code]['teamId'].values[0]
                home_games = self.games_df[self.games_df['homeTeam.id'] == team_id]
                away_games = self.games_df[self.games_df['awayTeam.id'] == team_id]
                self.games_df = pd.concat([home_games, away_games])

            if season_id != '':
                self.games_df = self.games_df[self.games_df['season'] == season_id]

            for index, row in self.games_df.iterrows():
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

                log = GamesImportLog(row['id'], datetime.today().strftime('%Y-%m-%d %H:%M:%S'), game_found=1)
                log.insertDB(log)

            db.commit()
            cursor.close()
            db.close()

        log_object = ImportTableUpdateLog("games_import", datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 1)
        log_object.updateDB(log_object)

        return True

    @staticmethod
    def clearDB(tri_code='', season_id=''):
        teams = TeamsImport()
        teams.queryDB()

        cursor, db = db_import_login()

        if tri_code == '' and season_id == '':
            sql = "truncate table games_import"
        else:
            sql = "delete from games_import where gameId > 0"
            if tri_code != '':
                team_id = str(teams.teams_df[teams.teams_df['triCode'] == tri_code]['teamId'].values[0])
                sql = sql + " and (homeTeam = " + team_id + " or awayTeam = " + team_id + ")"
            if season_id != '':
                sql = sql + " and seasonId = '" + str(season_id) + "'"

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self, tri_code='', season_id=''):
        teams = TeamsImport()
        teams.queryDB()

        sql_prefix = "select gameId, seasonId, gameType, gameDate, venue, neutralSite, startTimeUTC, venueUTCOffset, " \
                     "venueTimezone, gameState, gameScheduleState, awayTeam, awayTeamSplitSquad, awayTeamScore, " \
                     "homeTeam, homeTeamSplitSquad, homeTeamScore, periodType, gameOutcome from games_import where " \
                     "gameId > 0"
        sql_suffix = ""

        if tri_code != '':
            team_id = str(teams.teams_df[teams.teams_df['triCode'] == tri_code]['teamId'].values[0])
            sql_suffix += " and (homeTeam = " + team_id + " or awayTeam = " + team_id + ")"

        if season_id != '':
            sql_suffix += " and seasonId = " + season_id + " "

        sql = "{}{}".format(sql_prefix,  sql_suffix)

        cursor, db = db_import_login()
        games_df = pd.read_sql(sql, db)
        self.games_df = games_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return True

    def queryNHL(self, tri_code='', season_id=''):
        seasons = SeasonsImport()
        seasons.queryDB()

        season_id = str(season_id)

        if tri_code != '':
            seasons.seasons_df = seasons.seasons_df[seasons.seasons_df['triCode'] == tri_code]

        if season_id != '':
            seasons.seasons_df = seasons.seasons_df[seasons.seasons_df['seasonId'] == season_id]

        games_df = pd.DataFrame()

        for index, row in seasons.seasons_df.iterrows():
            base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
            query_string = "{}{}/{}".format(base_url, row['triCode'], row['seasonId'])
            json_data = fetch_json_data(query_string)

            if 'games' in json_data:
                team_schedule_df = pd.json_normalize(json_data, record_path=['games'])
                if 'tvBroadcasts' in team_schedule_df:
                    team_schedule_df.drop(columns='tvBroadcasts', inplace=True)
                team_schedule_df.fillna('', inplace=True)
                games_df = pd.concat([games_df, team_schedule_df])

            time.sleep(0.25)

        games_df.drop_duplicates(inplace=True)
        games_df.fillna('', inplace=True)
        games_df.dropna(axis=1, inplace=True)
        self.games_df = games_df

        return True

    def queryNHLupdateDB(self, tri_code='', season_id=''):
        self.queryNHL(tri_code, season_id)
        self.clearDB(tri_code, season_id)
        self.updateDB(self, tri_code, season_id)

        return True
