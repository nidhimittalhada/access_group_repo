# Copyright 2014 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

from tempest.api.share import base
from tempest import config_share as config
from tempest import exceptions
from tempest import test

CONF = config.CONF


class ShareServersAdminTest(base.BaseSharesAdminTest):

    @classmethod
    def setUpClass(cls):
        super(ShareServersAdminTest, cls).setUpClass()
        if not CONF.share.multitenancy_enabled:
            msg = ("Share servers can be tested only with multitenant drivers."
                  " Skipping.")
            raise cls.skipException(msg)
        __, cls.share = cls.create_share()
        __, cls.share_network = cls.shares_client.get_share_network(
            cls.shares_client.share_network_id)
        cls.sn_name_and_id = [
            cls.share_network["name"],
            cls.share_network["id"],
        ]

        # Date should be like '2014-13-12T11:10:09.000000'
        cls.date_re = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2}[A-Z]{1}"
                                 "[0-9]{2}:[0-9]{2}:[0-9]{2}).*$")

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_without_filters(self):
        resp, servers = self.shares_client.list_share_servers()
        self.assertIn(int(resp["status"]), test.HTTP_SUCCESS)
        self.assertTrue(len(servers) > 0)
        keys = [
            "id",
            "host",
            "status",
            "share_network_name",
            "updated_at",
            "project_id",
        ]
        for server in servers:
            # All expected keys are present
            for key in keys:
                self.assertIn(key, server.keys())
            # 'Updated at' is valid date
            self.assertTrue(self.date_re.match(server["updated_at"]))
            # Host is not empty
            self.assertTrue(len(server["host"]) > 0)
            # Id is not empty
            self.assertTrue(len(server["id"]) > 0)
            # Project id is not empty
            self.assertTrue(len(server["project_id"]) > 0)

        # Server we used is present
        any((s["share_network_name"] in self.sn_name_and_id and
             self.assertEqual(s["status"].lower(), "active")) for s in servers)

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_with_host_filter(self):
        # Get list of share servers and remember 'host' name
        __, servers = self.shares_client.list_share_servers()
        # Remember name of server that was used by this test suite
        # to be sure it will be still existing.
        host = ""
        for server in servers:
            if server["share_network_name"] in self.sn_name_and_id:
                if not server["host"]:
                    msg = ("Server '%s' has wrong value for host - "
                          "'%s'.") % (server["id"], server["host"])
                    raise exceptions.InvalidContentType(message=msg)
                host = server["host"]
                break
        if not host:
            msg = ("Appropriate server was not found. Its share_network_data"
                   ": '%s'. List of servers: '%s'.") % (self.sn_name_and_id,
                                                        str(servers))
            raise exceptions.NotFound(message=msg)
        search_opts = {"host": host}
        __, servers = self.shares_client.list_share_servers(search_opts)
        self.assertTrue(len(servers) > 0)
        for server in servers:
            self.assertEqual(server["host"], host)

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_with_status_filter(self):
        # Get list of share servers
        __, servers = self.shares_client.list_share_servers()
        # Remember status of server that was used by this test suite
        # to be sure it will be still existing.
        status = ""
        for server in servers:
            if server["share_network_name"] in self.sn_name_and_id:
                if not server["status"]:
                    msg = ("Server '%s' has wrong value for status - "
                          "'%s'.") % (server["id"], server["host"])
                    raise exceptions.InvalidContentType(message=msg)
                status = server["status"]
                break
        if not status:
            msg = ("Appropriate server was not found. Its share_network_data"
                   ": '%s'. List of servers: '%s'.") % (self.sn_name_and_id,
                                                        str(servers))
            raise exceptions.NotFound(message=msg)
        search_opts = {"status": status}
        __, servers = self.shares_client.list_share_servers(search_opts)
        self.assertTrue(len(servers) > 0)
        for server in servers:
            self.assertEqual(server["status"], status)

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_with_project_id_filter(self):
        search_opts = {"project_id": self.share_network["project_id"]}
        __, servers = self.shares_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertTrue(len(servers) > 0)
        for server in servers:
            self.assertEqual(server["project_id"],
                             self.share_network["project_id"])

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_with_share_network_name_filter(self):
        search_opts = {"share_network": self.share_network["name"]}
        __, servers = self.shares_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertTrue(len(servers) > 0)
        for server in servers:
            self.assertEqual(server["share_network_name"],
                             self.share_network["name"])

    @test.attr(type=["gate", "smoke", ])
    def test_list_share_servers_with_share_network_id_filter(self):
        search_opts = {"share_network": self.share_network["id"]}
        __, servers = self.shares_client.list_share_servers(search_opts)
        # Should exist, at least, one share server, used by this test suite.
        self.assertTrue(len(servers) > 0)
        for server in servers:
            self.assertIn(server["share_network_name"],
                          self.sn_name_and_id)

    @test.attr(type=["gate", "smoke", ])
    def test_show_share_server(self):
        __, servers = self.shares_client.list_share_servers()
        resp, server = self.shares_client.show_share_server(servers[0]["id"])
        self.assertIn(int(resp["status"]), test.HTTP_SUCCESS)
        keys = [
            "id",
            "host",
            "project_id",
            "status",
            "share_network_name",
            "created_at",
            "updated_at",
            "backend_details",
        ]
        # all expected keys are present
        for key in keys:
            self.assertIn(key, server.keys())
        # 'created_at' is valid date
        self.assertTrue(self.date_re.match(server["created_at"]))
        # 'updated_at' is valid date
        self.assertTrue(self.date_re.match(server["updated_at"]))
        # Host is not empty
        self.assertTrue(len(server["host"]) > 0)
        # Id is not empty
        self.assertTrue(len(server["id"]) > 0)
        # Project id is not empty
        self.assertTrue(len(server["project_id"]) > 0)
        # Status is not empty
        self.assertTrue(len(server["status"]) > 0)
        # share_network_name is not empty
        self.assertTrue(len(server["share_network_name"]) > 0)
        # backend_details should be a dict
        self.assertTrue(isinstance(server["backend_details"], dict))

    @test.attr(type=["gate", "smoke", ])
    def test_show_share_server_details(self):
        __, servers = self.shares_client.list_share_servers()
        resp, details = self.shares_client.show_share_server_details(
            servers[0]["id"])
        self.assertIn(int(resp["status"]), test.HTTP_SUCCESS)
        # If details are present they and their values should be only strings
        for k, v in details.iteritems():
            self.assertTrue(isinstance(k, basestring))
            self.assertTrue(isinstance(v, basestring))