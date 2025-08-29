import pandas as pd
import puckpandas as pp
from sqlalchemy import text


class PlayersImport:
    def __init__(self, player_id):
        self.player_id = player_id
        self.json = {}
        self.table_columns = ['playerId', 'isActive', 'currentTeamId', 'currentTeamAbbrev', 'sweaterNumber', 'position',
                              'heightInInches', 'heightInCentimeters', 'weightInPounds', 'weightInKilograms',
                              'birthDate', 'birthCountry', 'shootsCatches', 'inTop100AllTime', 'inHHOF',
                              'firstName.default', 'lastName.default', 'birthCity.default',
                              'birthStateProvince.default', 'draftDetails.year', 'draftDetails.teamAbbrev',
                              'draftDetails.round', 'draftDetails.pickInRound', 'draftDetails.overallPick']
        self.player_bios_df = pd.DataFrame()
        self.position = ''
        self.goalie_seasons = pp.GoalieSeasonsImport(player_id)
        self.goalie_career_totals = pp.GoalieCareerTotalsImport(player_id)
        self.skater_seasons = pp.SkaterSeasonsImport(player_id)
        self.skater_career_totals = pp.SkaterCareerTotalsImport(player_id)
        self.player_awards = pp.PlayerAwardsImport(player_id)
        self.query_db()
        self.player_bios_df = self.player_bios_df.reindex(columns=self.table_columns)

    def update_db(self):
        player_found = 0
        if self.json != {}:
            player_found = 1

            engine = pp.dba_import_login()
            sql = "insert into puckpandas_import.player_bios_import (playerId, isActive, currentTeamId, " \
                  "currentTeamAbbrev, " \
                  "sweaterNumber, position, heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, " \
                  "birthDate, birthCountry, shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, " \
                  "`lastName.default`, `birthCity.default`, `birthStateProvince.default`, `draftDetails.year`, " \
                  "`draftDetails.teamAbbrev`, `draftDetails.round`, `draftDetails.pickInRound`, " \
                  "`draftDetails.overallPick`) values (:playerId, :isActive, :currentTeamId, :currentTeamAbbrev, " \
                  ":sweaterNumber, :position, :heightInInches, :heightInCentimeters, :weightInPounds, " \
                  ":weightInKilograms, :birthDate, :birthCountry, :shootsCatches, :inTop100AllTime, :inHHOF, " \
                  ":firstNamedefault, :lastNamedefault, :birthCitydefault, :birthStateProvincedefault, " \
                  ":draftDetailsyear, :draftDetailsteamAbbrev, :draftDetailsround, :draftDetailspickInRound, " \
                  ":draftDetailsoverallPick)"
            player_transform_df = self.player_bios_df
            player_transform_df.columns = player_transform_df.columns.str.replace('.', '')
            player_transform_df.fillna(0, inplace=True)
            params = player_transform_df.to_dict('records')
            with engine.connect() as conn:
                conn.execute(text(sql), parameters=params)

            if self.position == 'G':
                self.goalie_seasons.update_db()
                self.goalie_career_totals.update_db()
            else:
                self.skater_seasons.update_db()
                self.skater_career_totals.update_db()
            self.player_awards.update_db()

        log = pp.PlayerImportLog(player_id=self.player_id, player_found=player_found)
        log.insert_db()

        return True

    def clear_db(self):
        engine = pp.dba_import_login()
        sql = "delete from puckpandas_import.player_bios_import where playerId = " + str(self.player_id)
        with engine.connect() as conn:
            conn.execute(text(sql))
        engine.dispose()

        if self.position == 'G':
            self.goalie_seasons.clear_db()
            self.goalie_career_totals.clear_db()
        else:
            self.skater_seasons.clear_db()
            self.skater_career_totals.clear_db()
        self.player_awards.clear_db()

        return True

    def query_db(self):
        engine = pp.dba_import_login()
        sql = "select id, playerId, isActive, currentTeamId, currentTeamAbbrev, sweaterNumber, position, " \
              "heightInInches, heightInCentimeters, weightInPounds, weightInKilograms, birthDate, birthCountry, " \
              "shootsCatches, inTop100AllTime, inHHOF, `firstName.default`, `lastName.default`, `birthCity.default`, " \
              "`birthStateProvince.default`, `draftDetails.year`, `draftDetails.teamAbbrev`, `draftDetails.round`, " \
              "`draftDetails.pickInRound`, `draftDetails.overallPick` from puckpandas_import.player_bios_import where "\
              "playerId = " + str(self.player_id)
        player_bios_df = pd.read_sql_query(sql, engine)
        engine.dispose()

        if player_bios_df.size > 0:
            player_bios_df = player_bios_df.reindex(columns=self.table_columns)
            player_bios_df.infer_objects().fillna('', inplace=True)
            self.player_bios_df = player_bios_df
            self.position = self.player_bios_df.at[0, 'position']

        if self.position == 'G':
            self.goalie_seasons.query_db()
            self.goalie_career_totals.query_db()
        else:
            self.skater_seasons.query_db()
            self.skater_career_totals.query_db()
        self.player_awards.query_db()

        return True

    def query_api(self):
        url_prefix = 'https://api-web.nhle.com/v1/player/'
        url_suffix = '/landing'
        url_string = "{}{}{}".format(url_prefix, self.player_id, url_suffix)
        self.json = pp.fetch_json_data(url_string)
        player_bios_df = pd.json_normalize(self.json)

        if player_bios_df.size == 0:
            return False

        player_bios_df = player_bios_df.reindex(columns=self.table_columns)
        player_bios_df.fillna(0, inplace=True)
        self.player_bios_df = player_bios_df

        self.position = self.player_bios_df.at[0, 'position']

        if 'careerTotals' in self.json and len(self.json['careerTotals']) > 0:
            if self.position == 'G':
                self.goalie_career_totals.json = self.json['careerTotals']
                self.goalie_career_totals.query_api()
            else:
                self.skater_career_totals.json = self.json['careerTotals']
                self.skater_career_totals.query_api()

        if 'seasonTotals' in self.json and len(self.json['seasonTotals']) > 0:
            if self.position == 'G':
                self.goalie_seasons.json = self.json['seasonTotals']
                self.goalie_seasons.query_api()
            else:
                self.skater_seasons.json = self.json['seasonTotals']
                self.skater_seasons.query_api()

        if 'awards' in self.json and len(self.json['awards']) > 0:
            self.player_awards.json = self.json['awards']
            self.player_awards.query_api()

        return True

    def query_api_update_db(self):
        self.query_api()
        self.clear_db()
        self.update_db()

        return True
