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

__author__ = 'b.gzr'
import os
import inspect
import json
import requests
import datetime
import DataManager as DM


class ContextBroker():
    def __init__(self, cb_url, user='', password=''):
        """
        Add a new entity list if it is valid.
            :param cb_url: Context Broker URL
            :param user: user (Only for http://orion.lab.fiware.org:1026)
            :param password: password (Only for http://orion.lab.fiware.org:1026)
        """
        self.orion = False
        if cb_url.find("http://orion.lab.fiware.org:1026") != -1:
            self.orion = True
            self.user = user
            self.password = password
            self.get_auth_token()

        if cb_url[len(cb_url)-1] == '/':
            cb_url = cb_url[:len(cb_url)-1]

        self.CBurl = cb_url
        self.entity = DM.Entity()

    def get_auth_token(self):
        """
        Returns token IDM .
            :rtype : unicode
        """
        try:
            # data = {
            #     "auth": {
            #         "passwordCredentials": {
            #             "username": self.user,
            #             "password": self.password,
            #         }
            #     }
            # }
            # payload = json.dumps(data)
            # headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            # response = requests.post("http://cloud.lab.fiware.org:4730/v2.0/tokens", headers=headers, data=payload)
            # if response.status_code == 200:
            #     self.token = response.json()['access']['token']['id']
            # print self.token
            self.token = '0vm3yTQ0MzuLaFR7GDJgVFcKRU0n9Swtzp82CpSvFllTOwUA8oRGiYZdqqnVhVnJIkEzXfYtwayRakSHPmfaGQ'
            
        except Exception as e:
            msg = "OrionAction.get_auth_token(): %s" % e
            DM.data_manager_error(msg)

    def clean_all(self):
        """
        Sets all the lists to empty lists.
        """
        self.entity.attribute.metadata.metadata_list_purge()
        self.entity.attribute.attribute_list_purge()
        self.entity.entity_list_purge()

    def get_response(self, data, url):
        """
        Context Broker request
            :param data:
            :param url:
            :rtype : requests.models.Response
        """
        try:
            if self.orion:
                headers = {'Content-Type': 'application/json', "X-Auth-Token": self.token, 'Accept': 'application/json'}
            else:
                headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

            response = requests.post(url, headers=headers, data=data)
            return response

        except requests.RequestException as e:
            msg = "ContextBroker.get_response(): %s" % e.message
            DM.data_manager_error(msg)

    def update_context(self, action='APPEND'):
        """
        Context Broker updateContext function
            :param action: update context action ['APPEND', 'UPDATE', 'DELETE']
            :rtype : requests.models.Response
        """
        if action not in ['APPEND', 'UPDATE', 'DELETE']:
            msg = "ContextBroker.update_context():The action passed to the function was not valid"
            DM.data_manager_error(msg)

        if len(self.entity.get_entity_list()) == 0:
            msg = "ContextBroker.update_contexte(): Empty entity_list was passed to the function"
            DM.data_manager_error(msg)

        payload = {'contextElements': self.entity.get_entity_list(),
                   'updateAction': action}

        data = json.dumps(payload)
        url = self.CBurl+'/v1/updateContext'
        response = self.get_response(data, url)
        z = 0
        while response.status_code == 401:
            print "invalid token "
            self.get_auth_token()
            response = self.get_response(data, url)
            if z == 2:
                msg = "ContextBroker.query_context(): User token not authorized, please check you credentials."
                DM.data_manager_error(msg)
            z += 1
        self.clean_all()

        return response

    def query_context(self, attributes=[]):
        """
        Context Broker queryContext function
            :param attributes:
            :rtype : requests.models.Response
        """
        if len(self.entity.get_entity_list()) == 0:
            msg = "ContextBroker.query_context(): Empty entity_list was passed to the function"
            DM.data_manager_error(msg)

        for entity in self.entity.get_entity_list():
            if 'attributes' in entity:
                del entity['attributes']

        payload = {'entities': self.entity.get_entity_list()}
        if len(attributes) != 0:
            payload['attributes'] = attributes

        data = json.dumps(payload)

        url = self.CBurl+'/v1/queryContext'
        response = self.get_response(data, url)
        z = 0
        while response.status_code == 401:
            print "invalid token "
            self.get_auth_token()
            response = self.get_response(data, url)
            if z == 2:
                msg = "ContextBroker.query_context(): User token not authorized, please check you credentials."
                DM.data_manager_error(msg)
            z += 1
        self.clean_all()

        return response

    def discover_context_availability(self, attributes=[]):
        """
        Context Broker /registry/discoverContextAvailability function
            :param attributes:
            :rtype : requests.models.Response
        """
        if len(self.entity.get_entity_list()) == 0:
            msg = "ContextBroker.discover_context_availability(): Empty entity_list was passed to the function."
            DM.data_manager_error(msg)

        for entity in self.entity.get_entity_list():
            if 'attributes' in entity:
                del entity['attributes']

        payload = {'entities': self.entity.get_entity_list()}
        if len(attributes) != 0:
            payload['attributes'] = attributes

        data = json.dumps(payload)
        url = self.CBurl+'/v1/registry/discoverContextAvailability'
        response = self.get_response(data, url)
        z = 0
        while response.status_code == 401:
            print "invalid token "
            self.get_auth_token()
            response = self.get_response(data, url)
            if z == 2:
                msg = "ContextBroker.query_context(): User token not authorized, please check you credentials."
                DM.data_manager_error(msg)
            z += 1
        self.clean_all()

        return response

    def register_context(self, provider, attribute_list=[], duration='', registration_id=''):
        """
        Context Broker /registry/registerContext function
            :param provider:
            :param attribute_list:
            :param duration:
            :param registration_id:
            :rtype : requests.models.Response
        """
        if len(self.entity.get_entity_list()) == 0:
            msg = "ContextBroker.register_context(): Empty entity_list was passed to the function."
            DM.data_manager_error(msg)

        entities = self.entity.get_entity_list()[:]
        if 'attributes' in entities[0]:
            del entities[0]['attributes']

        if len(attribute_list) != 0:
            for i in attribute_list:
                for element in i:
                    if element not in ['name', 'type', 'isDomain', 'metadatas']:
                        msg = "ContexBroker.register_context(): List was not added due to an incorrect format."
                        DM.data_manager_error(msg)

            payload = {
                "contextRegistrations": [{
                    'entities': entities,
                    'attributes': attribute_list,
                    'providingApplication': provider,
                }]
            }

        else:
            payload = {
                "contextRegistrations": [{
                    'entities': entities,
                    'providingApplication': provider,
                }]
            }

        if duration != '':
            payload['duration'] = duration
        if registration_id != '':
            payload['registrationId'] = registration_id

        data = json.dumps(payload)
        url = self.CBurl+'/v1/registry/registerContext'
        response = self.get_response(data, url)
        z = 0
        while response.status_code == 401:
            print "invalid token "
            self.get_auth_token()
            response = self.get_response(data, url)
            if z == 2:
                msg = "ContextBroker.query_context(): User token not authorized, please check you credentials."
                DM.data_manager_error(msg)
            z += 1
        self.clean_all()

        cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

        with open('%s/log/registration.log' % cmd_folder, 'a') as log:
            log_str = '%s %s\n %s\n %s\n' % (datetime.datetime.now(), self.CBurl, payload, response.text)
            log.write(log_str)
            log.close()
        return response


