# import json
# import pandas as pd
# import requests
# from api_query import fetch_json_data
# from mysql_db import nhlpandas_db_login

# build a string that's nicely formatted json data...
# data = '''[{"abc":"None","cde":4,"efg":1,"blah":{"k":23,"y":26,"u":48}},{"abc":"hdf","cde":10,"efg":2,
# "blah":{"k":244,"y":747,"u":75,"g":88}}]'''

# json_data = json.loads(data)

# build dataframe object
# df = pd.read_json(data)

# df2 = pd.json_normalize(json_data)

# select the indexing column
# df.set_index('efg')

# build a second dataframe that's just the sub-table info
# sub_df = df.blah.apply(pd.Series)

# adds 'blah' as a super-label to each column, leaving sub-labels as they were
# sub_df = pd.concat({'blah': sub_df}, axis=1, names=['l1', 'l2'])

# adds a blank super-label to each column, making ready to pair with the subtable
# df = pd.concat({'': df}, axis=1, names=['l1', 'l2'])

# re-pairs the sub and super tables
# df = pd.concat((df, sub_df), axis=1)

# drop the column that had the subtables in it
# df = df.drop('blah', axis=1)

# show result
# print(df)

# def fetch_seasons():
#     # data = fetch_json_data('https://statsapi.web.nhl.com/api/v1/seasons')
#     json_data = fetch_json_data('https://api.nhle.com/stats/rest/en/season?')
#
#     data = [(str(season['id'])[:4], str(season['id'])) for season in json_data['data']]
#
#     seasons_df = pd.DataFrame(data, columns=['year', 'seasonId'])
#     seasons_df.set_index('seasonId')
#
#     return seasons_df
#
#
# test_df = fetch_seasons()


# json_data = fetch_json_data('https://api-web.nhle.com/v1/player/8478402/landing')
#
#
#
# print(json_data['awards'])

# test_df['derp'] = 'success'

# play_by_play_df = pd.json_normalize(json_data, "awards")

# play_by_play_df = play_by_play_df.explode('seasons')

# doesn't work
# check_df = play_by_play_df['seasons']

# doesn't work
# play_by_play_df = pd.concat([play_by_play_df, pd.json_normalize(play_by_play_df['seasons'])])

# url = 'https://api-web.nhle.com/v1/player/8476412/landing'
# json_data = json.loads(requests.get(url).text)


# play_by_play_df = pd.concat([play_by_play_df, play_by_play_df['seasons'].apply(pd.Series)], axis=1)\
#     .drop(columns=['seasons'])

# column_string = ""
#
# # for col in play_by_play_df.columns:
# #     column_string = "{}'{}', ".format(column_string, col)
#
# print(column_string)

# import pandas as pd
# from alchemy_db import nhlpandas_dba_login
# from sqlalchemy import insert, select, and_, or_
# import puckpandas as puckpandas
#
# engine = nhlpandas_dba_login()
#
# with engine.connect() as conn:
#     select(teams_import.triCode).where(teams_import.)
#     sql = "select * from teams_import"
#     df = pd.read_sql(sql, conn)  # executes simple select statement
#
#     # insert statement with variables
#     stmt = insert("sql_tableName").values(first_name="spongeBob", last_name="squarePants")
#
#     # select statement with variables
#
# print(
#     select(Address.email_address).where(
#         and_(
#             or_(User.name == "squidward", User.name == "sandy"),
#             Address.user_id == User.id,
#         )
#     )
# )

# SELECT address.email_address
# FROM address, user_account
# WHERE (user_account.name = :name_1 OR user_account.name = :name_2)
# AND address.user_id = user_account.id
#
# df.to_sql('garbage1', conn, if_exists='fail', index=False)  # builds a new table from DataFrame
# df.to_sql('garbage1', conn, if_exists='replace', index=False)
# builds a new table or replaces it - test this option to make sure SQL schema remains intact
# df.to_sql('garbage1', conn, if_exists='append', index=False)  # builds a new table or inserts new rows
#
# print(df)


from puckpandas.alchemy_db import dba_import_login
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session
import pandas as pd

engine = dba_import_login()

df = pd.read_sql("select * from teams_import", engine)
print(df)

metadata = MetaData()
metadata.reflect(bind=engine)
my_table = Table('teams_import', metadata, autoload=True)

query = my_table.select()
print(query)
my_session = Session(engine)
my_session.execute(query)

print(my_table)

# this code didn't work as expected
# it failed to insert rows into the target table
# engine = puckpandas.dba_import_login()
# df = pd.read_sql("select * from shifts_import", engine)
# self.shifts_df.to_sql(name='shifts_import', con=engine, if_exists='append', index=False)