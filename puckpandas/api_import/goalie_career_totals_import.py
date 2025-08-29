import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class GoalieCareerTotalsImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'regularSeason.gamesPlayed', 'regularSeason.goals', 'regularSeason.assists',
                              'regularSeason.pim', 'regularSeason.gamesStarted', 'regularSeason.points',
                              'regularSeason.wins', 'regularSeason.losses', 'regularSeason.otLosses',
                              'regularSeason.shotsAgainst', 'regularSeason.goalsAgainst',
                              'regularSeason.goalsAgainstAvg', 'regularSeason.savePctg', 'regularSeason.shutouts',
                              'regularSeason.timeOnIce', 'regularSeason.timeOnIceMinutes',
                              'regularSeason.timeOnIceSeconds', 'playoffs.gamesPlayed', 'playoffs.goals',
                              'playoffs.assists', 'playoffs.pim', 'playoffs.gamesStarted', 'playoffs.points',
                              'playoffs.wins', 'playoffs.losses', 'playoffs.otLosses', 'playoffs.shotsAgainst',
                              'playoffs.goalsAgainst', 'playoffs.goalsAgainstAvg', 'playoffs.savePctg',
                              'playoffs.shutouts', 'playoffs.timeOnIce', 'playoffs.timeOnIceMinutes',
                              'playoffs.timeOnIceSeconds']
        self.goalie_career_df = pd.DataFrame()
        self.goalie_career_df = self.goalie_career_df.reindex(columns=self.table_columns)

    def update_db(self):
        career_totals_found = 0
        if self.json != {}:
            career_totals_found = 1
            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.goalie_career_totals_import (playerId, `regularSeason.gamesPlayed`, " \
                  "`regularSeason.goals`, `regularSeason.assists`, `regularSeason.pim`, " \
                  "`regularSeason.gamesStarted`, `regularSeason.points`, `regularSeason.wins`, " \
                  "`regularSeason.losses`, `regularSeason.otLosses`, `regularSeason.shotsAgainst`, " \
                  "`regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, " \
                  "`regularSeason.savePctg`, `regularSeason.shutouts`, `regularSeason.timeOnIce`, " \
                  "`regularSeason.timeOnIceMinutes`, `regularSeason.timeOnIceSeconds`, `playoffs.gamesPlayed`, " \
                  "`playoffs.goals`, `playoffs.assists`, `playoffs.pim`, `playoffs.gamesStarted`, `playoffs.points`, " \
                  "`playoffs.wins`, `playoffs.losses`, `playoffs.otLosses`, `playoffs.shotsAgainst`, " \
                  "`playoffs.goalsAgainst`, `playoffs.goalsAgainstAvg`, `playoffs.savePctg`, `playoffs.shutouts`, " \
                  "`playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, `playoffs.timeOnIceSeconds`) values " \
                  "(:playerId, :regularSeasongamesPlayed, :regularSeasongoals, :regularSeasonassists, " \
                  ":regularSeasonpim, :regularSeasongamesStarted, :regularSeasonpoints, :regularSeasonwins, " \
                  ":regularSeasonlosses, :regularSeasonotLosses, :regularSeasonshotsAgainst, " \
                  ":regularSeasongoalsAgainst, :regularSeasongoalsAgainstAvg, :regularSeasonsavePctg, " \
                  ":regularSeasonshutouts, :regularSeasontimeOnIce, :regularSeasontimeOnIceMinutes, " \
                  ":regularSeasontimeOnIceSeconds, :playoffsgamesPlayed, :playoffsgoals, :playoffsassists, " \
                  ":playoffspim, :playoffsgamesStarted, :playoffspoints, :playoffswins, :playoffslosses, " \
                  ":playoffsotLosses, :playoffsshotsAgainst, :playoffsgoalsAgainst, :playoffsgoalsAgainstAvg, " \
                  ":playoffssavePctg, :playoffsshutouts, :playoffstimeOnIce, :playoffstimeOnIceMinutes, " \
                  ":playoffstimeOnIceSeconds)"
            goalie_career_transform_df = self.goalie_career_df
            goalie_career_transform_df.columns = goalie_career_transform_df.columns.str.replace('.', '')
            params = goalie_career_transform_df.to_dict('records')

            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

        log = pp.PlayerImportLog(player_id=self.player_id, career_totals_found=career_totals_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.goalie_career_totals_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql= "select playerId, `regularSeason.gamesPlayed`, `regularSeason.goals`, `regularSeason.assists`, " \
              "`regularSeason.pim`, `regularSeason.gamesStarted`, `regularSeason.points`, `regularSeason.wins`, " \
              "`regularSeason.losses`, `regularSeason.otLosses`, `regularSeason.shotsAgainst`, " \
              "`regularSeason.goalsAgainst`, `regularSeason.goalsAgainstAvg`, `regularSeason.savePctg`, " \
              "`regularSeason.shutouts`, `regularSeason.timeOnIce`, `regularSeason.timeOnIceMinutes`, " \
              "`regularSeason.timeOnIceSeconds`, `playoffs.gamesPlayed`, `playoffs.goals`, `playoffs.assists`, " \
              "`playoffs.pim`, `playoffs.gamesStarted`, `playoffs.points`, `playoffs.wins`, `playoffs.losses`, " \
              "`playoffs.otLosses`, `playoffs.shotsAgainst`, `playoffs.goalsAgainst`, `playoffs.goalsAgainstAvg`, " \
              "`playoffs.savePctg`, `playoffs.shutouts`, `playoffs.timeOnIce`, `playoffs.timeOnIceMinutes`, " \
              "`playoffs.timeOnIceSeconds` from puckpandas_import.goalie_career_totals_import where playerId = " + \
             str(self.player_id)
        goalie_career_totals_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.infer_objects().fillna('', inplace=True)
            self.goalie_career_df = goalie_career_totals_df

        return True

    def query_api(self):
        goalie_career_totals_df = pd.json_normalize(self.json)
        goalie_career_totals_df.rename(columns={"id": "playerId"}, inplace=True)
        goalie_career_totals_df.insert(0, 'playerId', self.player_id)

        if goalie_career_totals_df.size > 0:
            goalie_career_totals_df = goalie_career_totals_df.reindex(columns=self.table_columns)
            goalie_career_totals_df.fillna(0, inplace=True)
            self.goalie_career_df = goalie_career_totals_df

        if self.goalie_career_df.loc[0, 'regularSeason.timeOnIce'] != 0:
            self.goalie_career_df[['regularSeason.timeOnIceMinutes', 'regularSeason.timeOnIceSeconds']] = (
                self.goalie_career_df['regularSeason.timeOnIce'].str.split(":", expand=True))
            self.goalie_career_df['regularSeason.timeOnIceSeconds'] = (
                    int(self.goalie_career_df['regularSeason.timeOnIceMinutes'].iloc[0]) * 60 +
                    int(self.goalie_career_df['regularSeason.timeOnIceSeconds'].iloc[0]))
        if self.goalie_career_df.loc[0, 'playoffs.timeOnIce'] != 0:
            self.goalie_career_df[['playoffs.timeOnIceMinutes', 'playoffs.timeOnIceSeconds']] = (
                self.goalie_career_df['playoffs.timeOnIce'].str.split(":", expand=True))
            self.goalie_career_df['playoffs.timeOnIceSeconds'] = (
                    int(self.goalie_career_df['playoffs.timeOnIceMinutes'].iloc[0]) * 60 +
                    int(self.goalie_career_df['playoffs.timeOnIceSeconds'].iloc[0]))

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
