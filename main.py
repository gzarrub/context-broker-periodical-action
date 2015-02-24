import test as t

import time
import os

from apscheduler.schedulers.background import BackgroundScheduler



if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(t.action, 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible