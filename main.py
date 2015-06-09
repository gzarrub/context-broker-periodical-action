#!/usr/bin/python
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of context-broker-periodical-action.
#
# context-broker-periodical-action is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# context-broker-periodical-action is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.

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
    scheduler.add_job(t.action, 'interval', seconds=30)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Not strictly necessary if daemonic mode is enabled but should be done if possible
