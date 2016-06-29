# Copyright 2016 Wipro Technologies
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

"""The access groups api."""

from oslo_log import log
import webob
from webob import exc

from manila.api import common
from manila.api.openstack import wsgi
from manila.api.views import access_groups as access_groups_views
from manila import db
from manila import exception
from manila.i18n import _, _LI
import manila.access_group.api as ag_api

LOG = log.getLogger(__name__)


class AccessGroupsController(wsgi.Controller, wsgi.AdminActionsMixin):
    """The Access Groups API controller for the OpenStack API."""

    resource_name = 'access_group'
    _view_builder_class = access_groups_views.ViewBuilder
    
    def __init__(self):
        super(AccessGroupsController, self).__init__()
        self.access_group_api = ag_api.API()
    
    @wsgi.response(202)
    def create(self, req, body):
        """Creates a new access_group."""
        print("NMH 1234 access_groups.py in create() i m here 11111 body is",body)    
        context = req.environ['manila.context']

        if not self.is_valid_body(body, 'access_group'):
            raise exc.HTTPUnprocessableEntity()

        access_group = body['access_group']

        # Verify that share can be snapshotted
        LOG.info(_LI("Create an access_group"))

        access_group = self.access_group_api.create(
            context,
            access_group.get('name'),
            access_group.get('description'),
            access_group.get('access_type'),
            access_group.get('access_level'),
            )
        return self._view_builder.detail(req, access_group)
    
    def index(self, req):
        """Returns a summary list of access_groups."""
        print("NMH 99999 i m here in index() 1111")    
        return self._get_access_groups(req, is_detail=False)

    def detail(self, req):
        """Returns a detailed list of access_groups."""
        print("NMH 99999 i m here in detail() 22222")    
        return self._get_access_groups(req, is_detail=True)
    
    def show(self, req, id):
        """Return data about the given access_group."""
        context = req.environ['manila.context']
        try:
            access_group = self.access_group_api.get_access_group(context, id)
            print("NMH 999999 api/v2/access_groups.py access_group is",access_group)
        except exception.NotFound:
            raise exc.HTTPNotFound()
        
        return self._view_builder.detail(req, access_group)
    
    @wsgi.Controller.authorize('get_all')
    def _get_access_groups(self, req, is_detail):
        """Returns a list of access_groups."""
        context = req.environ['manila.context']
        access_groups = self.access_group_api.get_all(context)
        print("NMH 222222 api/v2/access_groups.py access_groups is",access_groups)
        limited_list = common.limited(access_groups, req)
        if is_detail:
            access_groups = self._view_builder.detail_list(req, limited_list)
        else:
            access_groups = self._view_builder.summary_list(req, limited_list)

        return access_groups


def create_resource():
    print("NMH 999999 access_groups.py i m here 66666666")
    return wsgi.Resource(AccessGroupsController())
