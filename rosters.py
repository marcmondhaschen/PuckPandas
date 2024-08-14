import pandas as pd
from api_query import fetch_json_data
from mysql_db import nhlpandas_db_login


def nhl_pandas_fetch_rosters_to_query():
    """
    Queries the local MySQL database for a list of team triCodes and the seasonIds played so far for each team/triCode

    Parameters:

    Returns: rosters_df - a Pandas DataFrame containing a list of triCodes and the seasonIds as described above
    """
    rosters_sql = "select a.triCode, a.seasonId, 99 as players from team_seasons_import as a " \
                  "where a.triCode = 'STL' and a.seasonId = 20182019"
    # rosters_sql = 'select a.triCode, a.seasonId, count(b.playerId) as players from team_seasons_import as a left ' \
    #               'join rosters_import as b on a.triCode = b.triCode and a.seasonId = b.seasonId group by ' \
    #               'a.triCode, a.seasonId having players = 0'
    cursor, db = nhlpandas_db_login()
    rosters_df = pd.read_sql(rosters_sql, db)

    return rosters_df


def nhlpandas_fetch_team_roster_by_season():
    """
    Queries the NHL API for team rosters for each triCode and seasonId provided

    Parameters:

    Returns: roster_players_df - a Pandas Dataframe containing
    """
    rosters_df = nhl_pandas_fetch_rosters_to_query()

    if len(rosters_df) == 0:
        return False

    for index, row in rosters_df.iterrows():
        url_prefix = "https://api-web.nhle.com/v1/roster/"
        query_url = "{}{}/{}".format(url_prefix, row['triCode'], row['seasonId'])

        json_data = fetch_json_data(query_url)

        forwards_data = pd.json_normalize(json_data, record_path=['forwards'])
        defensemen_data = pd.json_normalize(json_data, record_path=['defensemen'])
        goalies_data = pd.json_normalize(json_data, record_path=['goalies'])

        this_roster_df = pd.concat([forwards_data, defensemen_data, goalies_data])
        this_roster_df = this_roster_df[['id']]
        this_roster_df['triCode'] = row['triCode']
        this_roster_df['seasonId'] = row['seasonId']

        # this_roster_df = nhlpandas_transform_team_roster_by_season(this_roster_df)
        # nhlpandas_load_team_roster_by_season_import(this_roster_df)

    return True


def nhlpandas_transform_team_roster_by_season(roster_players_df):
    """
    Transforms the Pandas dataframe to ready it for import into the local MySQL database

    Parameters: roster_players_df - the Pandas Dataframe object to be transformed

    Returns: roster_players_df - the transformed Pandas Dataframe object
    """
    roster_players_df = roster_players_df.fillna('')
    roster_players_df = roster_players_df.reset_index(drop=True)
    return roster_players_df


def nhlpandas_load_team_roster_by_season_import(this_roster_df):
    """
    Imports the transformed rosters DataFrame into the local MySQL database

    Parameters:

    Returns: this_roster_df - the Pandas Dataframe with rosters by season to be imported
    """
    cursor, db = nhlpandas_db_login()

    for index, row in this_roster_df.iterrows():
        sql = "insert into rosters_import (`triCode`, `seasonId`, `playerId`) values (%s,  %s, %s)"
        val = (row['triCode'], row['seasonId'], row['id'])
        cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()
    return True


def nhlpandas_etl_team_roster_by_season():
    """
    Queries a list of teams and seasons that each team played from the local database, uses this list to query a
    roster for each team & season, transforms the NHL's JSON response into a Pandas Dataframe, and imports that
    DataFrame into a local MySQL table

    Parameters:

    Returns: check_var - returns True upon completion
    """
    check_var = nhlpandas_fetch_team_roster_by_season()

    return check_var
