import functions as f
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler


def periodical_action():

    o = f.ContextBroker('http://130.206.85.12:1026')


    print o.discover_context_availability().json()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodical_action, 'interval', seconds=5)
    scheduler.start()

    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)

    except (KeyboardInterrupt, SystemExit, Exception):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible