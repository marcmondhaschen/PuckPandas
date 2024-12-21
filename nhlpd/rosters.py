import pandas as pd
import nhlpd


class RostersImport:
    def __init__(self, team_id, season_id):
        self.team_id = team_id
        self.season_id = season_id
        self.teams = nhlpd.TeamsImport()
        self.tri_code = self.teams.tri_code_from_team_id(self.team_id)
        self.roster_df = pd.DataFrame(columns=['triCode', 'seasonId', 'playerId'])

    def update_db(self):
        if self.roster_df.size > 0:
            cursor, db = nhlpd.db_import_login()
            for index, row in self.roster_df.iterrows():
                if 'id' in row:
                    sql = "insert into rosters_import (triCode, seasonId, playerId) " \
                          "values (%s, %s, %s)"
                    val = (row['triCode'], row['seasonId'], row['playerId'])
                    cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

        return True

    def clear_db(self):
        if self.tri_code != '' and self.season_id != '':
            cursor, db = nhlpd.db_import_login()
            sql = "delete from rosters_import where triCode = '" + str(self.tri_code) + "' and seasonId = " + \
                  str(self.season_id)
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()

        return True

    def query_db(self):
        cursor, db = nhlpd.db_import_login()
        sql = "select triCode, seasonId, playerId from rosters_import where seasonId > 0 and  triCode = " + \
              self.tri_code + " and seasonId = " + self.season_id
        query_df = pd.read_sql(sql, db)
        db.commit()
        cursor.close()
        db.close()

        roster_df = self.roster_df.head(0)
        roster_df = pd.concat([roster_df, query_df])
        roster_df.fillna('', inplace=True)
        roster_df.drop_duplicates(inplace=True)
        self.roster_df = roster_df

        return self.roster_df

    def query_nhl(self):
        base_url = 'https://api-web.nhle.com/v1/club-schedule-season/'
        query_string = "{}{}/{}".format(base_url, self.tri_code, self.season_id)
        json_data = nhlpd.fetch_json_data(query_string)

        if 'games' in json_data:
            query_df = pd.json_normalize(json_data, record_path=['games'])

            query_df.rename(columns={'id': 'playerId'}, inplace=True)

            roster_df = self.roster_df.head(0)
            roster_df = pd.concat([roster_df, query_df])
            roster_df.fillna('', inplace=True)

            self.roster_df = roster_df

        return self.roster_df

    def query_nhl_update_db(self):
        self.query_nhl()
        self.clear_db()
        self.update_db()
        return True
