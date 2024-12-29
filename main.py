from datetime import datetime, timezone
import numpy as np
import nhlpd


# for now, main serves as a program script to test functions
if __name__ == "__main__":
    current_time = np.datetime64(datetime.now(timezone.utc))

    scheduler = nhlpd.Scheduler()
    scheduler.poll_nhl()
    print("the end?")
