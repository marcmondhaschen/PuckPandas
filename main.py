# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    game_center = nhlpd.GameCenterImport()
    game_center = game_center.queryNHL(game_id=2023021019)
    # game_center = game_center.queryNHL(game_id=2018010046)
    print(game_center.game_center_open_work_df)
    print(game_center.game_center_df)
