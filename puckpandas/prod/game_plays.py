import pandas as pd
import puckpandas as pp
from sqlalchemy import text

class GamePlays:
    def __init__(self):
        self.table_columns = ['playId','gameId','eventId','sortOrder','teamId','typeCode','situationCode','homeTeam']
        self.game_plays_df = pd.DataFrame()
        self.query_db()
        self.game_plays_df = self.game_plays_df.reindex(columns=self.table_columns)
        self.current_season = pp.TeamSeasonsImport.current_season()

    def update_db(self):
        if self.game_plays_df.size > 0:
            engine = pp.dba_prod_login()
            sql = "insert into puckpandas.game_plays` (playId, gameId, eventId, sortOrder, teamId, typeCode, " \
                  "situationCode, homeTeamDefendingSide, xCoord, yCoord, zoneCode) select b.playId, a.gameId, " \
                  "a.eventId, a.sortOrder, a.`details.eventOwnerTeamId` as teamId, a.typeCode, case when " \
                  "a.situationCode = 0 then null else lpad(a.situationCode, 4, '0') end as situationCode, case when " \
                  "a.homeTeamDefendingSide like '0%' then null else a.homeTeamDefendingSide end as " \
                  "homeTeamDefendingSide, case when a.`details.zoneCode` like '0%' then null else a.`details.xCoord` " \
                  "end as xCoord, case when a.`details.zoneCode` like '0%' then null else a.`details.yCoord` end as " \
                  "yCoord, case when a.`details.zoneCode` like '0%' then null else a.`details.zoneCode` end as " \
                  "zoneCode from puckpandas_import.plays_import as a join puckpandas_import.games_import as g on " \
                  "a.gameId = g.gameId join puckpandas.plays as b on a.gameId = b.gameId and a.eventId = b.eventId " \
                  "where g.seasonId = " + str(self.current_season)

            with engine.connect() as conn:
                conn.execute(text(sql))

        return True

    @staticmethod
    def clear_db():
        engine = pp.dba_prod_login()
        sql = "delete from puckpandas.game_plays"

        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_prod_login()
        sql = "select playId, gameId, eventId, sortOrder, teamId, typeCode, situationCode, homeTeamDefendingSide, " \
              "xCoord, yCoord, zoneCode from puckpandas.game_plays"
        game_plays_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if game_plays_df.size > 0:
            game_plays_df = game_plays_df.reindex(columns=self.table_columns)
            game_plays_df.infer_objects().fillna('', inplace=True)
            game_plays_df.drop_duplicates(inplace=True)
            self.game_plays_df = game_plays_df

        return self.game_plays_df
