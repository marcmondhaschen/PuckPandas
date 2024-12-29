import pandas as pd
import nhlpd


class TeamsImport:
    def __init__(self):
        self.teams_df = self.query_db()

    def update_db(self, tri_code=''):
        cursor, db = nhlpd.db_import_login()

        if tri_code != '':
            self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

        if len(self.teams_df.index) > 0:
            for index, row in self.teams_df.iterrows():
                sql = "insert into teams_import (teamId, franchiseId, fullName, leagueId, triCode) " \
                      "values (%s, %s, %s, %s, %s) "
                val = (row['id'], row['franchiseId'], row['fullName'], row['leagueId'], row['triCode'])
                cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def clear_db(tri_code=''):
        cursor, db = nhlpd.db_import_login()

        if tri_code == '':
            sql = "truncate table teams_import"
        else:
            sql = "delete from teams_import where triCode = '" + tri_code + "'"

        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()

        return True

    @staticmethod
    def query_db(tri_code=''):
        sql_prefix = "select teamId, franchiseId, fullName, leagueId, triCode from teams_import "
        sql_suffix = ""

        if tri_code != '':
            sql_suffix = "where triCode = " + tri_code

        sql = "{}{}".format(sql_prefix, sql_suffix)

        cursor, db = nhlpd.db_import_login()
        teams_df = pd.read_sql(sql, db)
        teams_df = teams_df.fillna('')

        db.commit()
        cursor.close()
        db.close()

        return teams_df

    def query_nhl(self, tri_code=''):
        json_data = nhlpd.fetch_json_data('https://api.nhle.com/stats/rest/en/team')
        api_teams_df = pd.json_normalize(json_data, record_path=['data'])
        api_teams_df = api_teams_df.fillna('')
        self.teams_df = pd.concat([self.teams_df, api_teams_df])

        if tri_code != '':
            self.teams_df = self.teams_df[self.teams_df['triCode'] == tri_code]

        return True

    def query_nh_lupdate_db(self, tri_code=''):
        self.query_nhl(tri_code)
        self.clear_db(tri_code)
        self.update_db(tri_code)

        return True

    def team_id_from_tri_code(self, tri_code):
        team_id = self.teams_df.loc[self.teams_df['triCode'] == tri_code, 'teamId'].item()

        return team_id

    def tri_code_from_team_id(self, team_id):
        tri_code = self.teams_df.loc[self.teams_df['teamId'] == team_id, 'triCode'].item()

        return tri_code
