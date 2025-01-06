import puckpandas

# for now, main serves as a program script to test functions
if __name__ == "__main__":
    scheduler = puckpandas.Scheduler()
    scheduler.poll_nhl()
    print("the end!")
