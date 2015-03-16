import test as t
import logging
import inspect
import time
import os

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='%s/log/error.log' % cmd_folder, level=logging.WARNING)

from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(t.action, 'interval', seconds=15)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible
