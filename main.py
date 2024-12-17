# from datetime import datetime
import nhlpd

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    scheduler = nhlpd.Scheduler()
    scheduler.pollNHL()
    print("the end?")
