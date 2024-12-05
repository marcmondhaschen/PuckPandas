# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    game_center = nhlpd.GameCenterImport()
    game_center = game_center.queryNHLupdateDB(game_id=2023021019)
    game_center_copy = nhlpd.GameCenterImport()
    game_center_copy.queryDB(game_id=2023021019)
    print(game_center_copy.scratches.scratches_df)
