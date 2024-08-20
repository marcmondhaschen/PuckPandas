import pandas as pd
from .api_query import fetch_json_data
from .mysql_db import db_import_login


class TeamsImport:
    teams_df = pd.DataFrame(columns=['id', 'franchiseId', 'fullName', 'leagueId', 'rawTricode', 'triCode'])

    def __init__(self, teams_df=pd.DataFrame()):
        self.teams_df = pd.concat([self.teams_df, teams_df])

    @staticmethod
    def updateDB(self):
        """
        Imports the teams dataframe contents into the local MySQL database

        Parameters: none

        Returns: True - Returns True upon completion
        """
        if len(self.teams_df) > 0:
            cursor, db = db_import_login()

            for index, row in self.teams_df.iterrows():
                sql = "insert into teams_import (teamId, franchiseId, fullName, leagueId, triCode) " \
                      "values (%s, %s, %s, %s, %s)"
                val = (row['id'], row['franchiseId'], row['fullName'], row['leagueId'], row['triCode'])
                cursor.execute(sql, val)

            db.commit()
            cursor.close()
            db.close()
        return True

    @staticmethod
    def clearDB():

        cursor, db = db_import_login()

        sql = "truncate table teams_import"
        cursor.execute(sql)

        db.commit()
        cursor.close()
        db.close()
        return True

    def queryDB(self):
        """
        Requests a list of NHL teams currently loaded in the local database. Updates the Teams object's teams_df with
        the database's reply.

        Parameters:

        Returns:
        """

        teams_sql = "select teamId, franchiseId, fullName, leagueId, triCode from teams_import"

        cursor, db = db_import_login()
        db_teams_df = pd.read_sql(teams_sql, db)
        self.teams_df = db_teams_df.fillna('')

        return True

    def queryNHL(self):
        """
        Requests a list of past & present NHL teams from the NHL API. Updates the Teams object's teams_df with
        the NHL's reply.

        Parameters:

        Returns:
        """

        json_data = fetch_json_data('https://api.nhle.com/stats/rest/en/team')
        api_teams_df = pd.json_normalize(json_data, record_path=['data'])
        api_teams_df = api_teams_df.fillna('')
        self.teams_df = pd.concat([self.teams_df, api_teams_df])

        return True

    def queryNHLupdateDB(self):
        self.queryNHL()
        self.clearDB()
        self.updateDB(self)

        return True


def fetch_nhl_teams():
    """
    Requests a list of past & present NHL teams from the NHLE API. Receives the NHL's reply in JSON and returns a
    Pandas DataFrame object with the same info.

    Parameters:

    Returns: teams_df - a Pandas Dataframe object
    """
    data = fetch_json_data('https://api.nhle.com/stats/rest/en/team')
    teams_df = pd.json_normalize(data, record_path=['data'])

    return teams_df


def transform_nhl_teams(teams_df):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: teams_df - the Pandas Dataframe object to be transformed

    Returns: teams_df - the transformed Pandas Dataframe object
    """
    # establish an index column
    teams_df.set_index('id')

    # change nan values to null for MySQL
    teams_df = teams_df.fillna('')

    return teams_df


# TODO error checking on return
def load_nhl_teams_import(teams_df):
    """
    Imports the transformed NHL teams dataframe into the local MySQL database

    Parameters: teams_df - a Pandas Dataframe object containing the NHL API's teams data

    Returns: True - Returns True upon completion
    """
    cursor, db = db_import_login()

    for index, row in teams_df.iterrows():
        sql = "insert into teams_import (teamId, franchiseId, fullName, leagueId, triCode) values (%s, %s, %s, %s, %s)"
        val = (row['id'], row['franchiseId'], row['fullName'], row['leagueId'], row['triCode'])
        cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()

    return True


# TODO error checking on return
def etl_nhl_teams():
    """
    Queries a list of NHL teams from the NHL API, transforms the JSON response into a Pandas DataFrame,
    and imports that DataFrame to a local MySQL table

    Parameters:

    Returns: True - Returns True upon completion
    """
    df = fetch_nhl_teams()
    df = transform_nhl_teams(df)
    load_nhl_teams_import(df)

    return True
