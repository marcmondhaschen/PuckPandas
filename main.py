from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    log = nhlpd.PlayerImportLog(player_id='1234', last_date_updated=datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    log.insertDB(log)
