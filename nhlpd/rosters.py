from datetime import datetime
import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login
from .seasons import SeasonsImport
from .import_table_update_log import ImportTableUpdateLog


class RostersImport:
    rosters_df = pd.DataFrame(columns=['triCode', 'seasonId', 'playerId'])

    def __init__(self, rosters_df=pd.DataFrame()):
        self.rosters_df = pd.concat([self.rosters_df, rosters_df])

    @staticmethod
    def updateDB(self, tri_code='', season_id=''):
        if len(self.rosters_df) > 0:
            cursor, db = db_import_login()

            if tri_code != '':
                self.rosters_df = self.rosters_df[self.rosters_df['triCode'] == tri_code]

            if season_id != '':
                self.rosters_df = self.rosters_df[self.rosters_df['seasonId'] == season_id]

            for index, row in self.rosters_df.iterrows():
                if 'id' in row:
                    sql = "insert into rosters_import (triCode, seasonId, playerId) " \
                          "values (%s, %s, %s)"
                    val = (row['triCode'], row['seasonId'], row['id'])
                    cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()

        log_object = ImportTableUpdateLog("rosters_import", datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 1)
        log_object.updateDB(log_object)

        return True

    @staticmethod
    def clearDB(tri_code='', season_id=''):
        cursor, db = db_import_login()

        if tri_code == '' and season_id == '':
            sql = "truncate table rosters_import"
        else:
            sql_prefix = "delete from rosters_import where playerId != 0 "
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
        sql_prefix = "select triCode, seasonId, playerId from rosters_import where seasonId > 0 "
        sql_middle = ""
        sql_suffix = ""

        if tri_code != '':
            sql_middle = "and  triCode = " + tri_code + " "

        if season_id != '':
            sql_suffix = "and seasonId = " + season_id + " "

        sql = "{}{}{}".format(sql_prefix, sql_middle, sql_suffix)

        cursor, db = db_import_login()
        rosters_df = pd.read_sql(sql, db)
        self.rosters_df = rosters_df.fillna('')

        return True

    def queryNHL(self, tri_code='', season_id=''):
        seasons = SeasonsImport()
        seasons.queryDB()

        rosters_df = pd.DataFrame()

        for index, row in seasons.seasons_df.iterrows():
            url_prefix = "https://api-web.nhle.com/v1/roster/"
            query_url = "{}{}/{}".format(url_prefix, row['triCode'], row['seasonId'])

            json_data = fetch_json_data(query_url)

            forwards_data = pd.json_normalize(json_data, record_path=['forwards'])
            defensemen_data = pd.json_normalize(json_data, record_path=['defensemen'])
            goalies_data = pd.json_normalize(json_data, record_path=['goalies'])

            this_roster_df = pd.concat([forwards_data, defensemen_data, goalies_data])
            # this_roster_df = this_roster_df[['id']]
            this_roster_df['triCode'] = row['triCode']
            this_roster_df['seasonId'] = row['seasonId']
            this_roster_df.fillna('', inplace=True)
            rosters_df = pd.concat([rosters_df, this_roster_df])

        self.rosters_df = rosters_df

        if tri_code != '':
            self.rosters_df = self.rosters_df[self.rosters_df['triCode'] == tri_code]

        if season_id != '':
            self.rosters_df = self.rosters_df[self.rosters_df['seasonId'] == season_id]

        return True

    def queryNHLupdateDB(self, tri_code='', season_id=''):
        self.queryNHL(tri_code, season_id)
        self.clearDB(tri_code, season_id)
        self.updateDB(self, tri_code, season_id)
        return True
