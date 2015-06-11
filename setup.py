#!/usr/bin/python
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of context-broker-periodical-action.
#
# context-broker-periodical-action is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# context-broker-periodical-action is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.


from setuptools import setup, find_packages

setup(
    name='context-broker-periodical-action',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/gzarrub/context-broker-periodical-action',
    license='',
    author='Guillermo Zarzuelo',
    author_email='gzarrub@gmail.com',
    description="""The context-broker-periodical-action is a python software that allows to define periodical task
    related to Orion contextBroker as updatecontext, queryContext and discoverContextAvailability.
    It links a ContextBroker with another service and  lets to provide real  time data from sources which have no
    problems with traffic at regular intervals.""",
    install_requires=['apscheduler', 'pyproj', 'requests']
)