import pandas as pd
from api_query import fetch_json_data
from mysql_db import db_login


def fetch_seasons():
    """
    Queries the local MySQL database for a list of NHL teams and uses that list to query the NHL API for a list of
    seasons played for each NHL team

    Parameters:

    Returns: team_seasons_df - a Pandas Dataframe object containing a list of each season played for each NHL team in
    the local MySQL database
    """
    # query all the team codes from the local db
    teams_sql = 'select triCode from teams'
    cursor, db = db_login()
    teams_df = pd.read_sql(teams_sql, db)

    # query seasons played for each team code from NHL
    team_seasons_df = pd.DataFrame()

    for index, row in teams_df.iterrows():
        base_url = 'https://api-web.nhle.com/v1/roster-season/'
        team_tricode = row['triCode']
        query_string = "{}{}".format(base_url, team_tricode)
        json_data = fetch_json_data(query_string)

        seasons_df = pd.DataFrame(json_data)
        seasons_df.rename(columns={0: "seasonId"}, inplace=True)
        seasons_df['triCode'] = team_tricode

        team_seasons_df = pd.concat([team_seasons_df, seasons_df])

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return team_seasons_df


def transform_seasons(team_seasons_df: pd.DataFrame):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: teams_seasons_df - the Pandas Dataframe object to be transformed

    Returns: teams_seasons_df - the transformed Pandas Dataframe object
    """
    # Renumber the index; assembly through concatenation leaves the index count fragmented.
    team_seasons_df.reset_index()

    # Change nan values to null for MySQL
    team_seasons_df = team_seasons_df.fillna('')

    return team_seasons_df


# TODO error checking on return
def load_seasons_import(team_seasons_df: pd.DataFrame):
    """
    Imports the transformed NHL seasons played for each team into the local MySQL database

    Parameters: team_seasons_df - a Pandas Dataframe object containing the NHL API's teams/seasons data

    Returns: True - Returns True upon completion
    """
    cursor, db = db_login()

    for index, row in team_seasons_df.iterrows():
        sql = "insert into team_seasons (triCode, seasonId) values (%s, %s)"
        val = (row['triCode'], row['seasonId'])
        cursor.execute(sql, val)

    # tidy up the cursors
    db.commit()
    cursor.close()
    db.close()

    return True


# TODO error checking on return
def etl_seasons():
    """
    Queries a list of seasons played for each NHL team from the NHL API, transforms the JSON responses into a
    Pandas DataFrame, and imports that DataFrame to a local MySQL table

    Parameters:

    Returns: True - Returns True upon completion
    """
    df = fetch_seasons()
    df = transform_seasons(df)
    load_seasons_import(df)
    return True
