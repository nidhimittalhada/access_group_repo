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

"""The access group entries api."""

from oslo_log import log
import webob
from webob import exc

from manila.api import common
from manila.api.openstack import wsgi
from manila.api.views import access_groups as access_groups_views
from manila.api.views import access_group_entries as access_group_entries_views
from manila import db
from manila import exception
from manila.i18n import _, _LI
import manila.access_group.api as ag_api

LOG = log.getLogger(__name__)


class AccessGroupEntriesController(wsgi.Controller, wsgi.AdminActionsMixin):
    """The Access Group Entries API controller for the OpenStack API."""

    resource_name = 'access_group_entry'
    _view_builder_class = access_group_entries_views.ViewBuilder
    
    def __init__(self):
        super(AccessGroupEntriesController, self).__init__()
        self.access_group_api = ag_api.API()
    
    @wsgi.response(202)
    def create(self, req, body):
        """Creates a new access_group."""
        print("NMH 1234 access_group_entries.py in create() i m here 11111 body is",body)    
        context = req.environ['manila.context']

        if not self.is_valid_body(body, 'access_group_entry'):
            raise exc.HTTPUnprocessableEntity()

        access_group_entry = body['access_group_entry']

        # Verify that share can be snapshotted
        LOG.info(_LI("Create an access_group_entry"))

        access_group_entry = self.access_group_api.create_entry(
            context,
            access_group_entry.get('access_group_id'),
            access_group_entry.get('access_to')
            )
        return self._view_builder.detail(req, access_group_entry)
    
    def show(self, req, id):
        """Return data about the given access_group_entry."""
        context = req.environ['manila.context']
        try:
            access_group_entry = self.access_group_api.get_access_group_entry(context, id)
            print("NMH 999999 api/v2/access_groups.py access_group_entry got is",access_group_entry)
        except exception.NotFound:
            raise exc.HTTPNotFound()
        
        return self._view_builder.detail(req, access_group_entry)
    
    def index(self, req):
        """Returns a summary list of access_group_entries."""
        print("NMH 99999 i m here in index() 1111")    
        return self._get_access_group_entries(req, is_detail=False)

    def detail(self, req):
        """Returns a detailed list of access_groups."""
        print("NMH 99999 i m here in detail() 22222")    
        return self._get_access_group_entries(req, is_detail=True)
    
    @wsgi.Controller.authorize('get_all')
    def _get_access_group_entries(self, req, is_detail):
        """Returns a list of access_group_entries."""
        context = req.environ['manila.context']

        search_opts = {}
        search_opts.update(req.GET)

        sort_key = search_opts.pop('sort_key', 'created_at')
        sort_dir = search_opts.pop('sort_dir', 'desc')
        access_group_id = search_opts.pop('access_group_id', None)

        common.remove_invalid_options(context, search_opts,
                                      self._get_access_entries_search_options())
        
        access_group_entries = self.access_group_api.get_all_access_group_entries(
            context,
            access_group_id = access_group_id,
            sort_key=sort_key,
            sort_dir=sort_dir,
        )

        print("NMH 222222 api/v2/access_group_entries.py access_group_entries is",access_group_entries)

        limited_list = common.limited(access_group_entries, req)
       
        if is_detail:
            access_group_entries = self._view_builder.detail_list(req, limited_list)
        else:
            access_group_entries = self._view_builder.summary_list(req, limited_list)
        return access_group_entries
    
    def _get_access_entries_search_options(self):
        """Return access_entry search options allowed by non-admin."""
        return ('access_group_id')
    
    @wsgi.Controller.authorize
    def delete(self, req, id):
        """Delete an access_group_entry."""
        context = req.environ['manila.context']

        try:
            access_group_entry = self.access_group_api.get_access_group_entry(context, id)
            print("NMH 999999 api/v2/access_groups.py access_group_entry got is",access_group_entry)
        except exception.NotFound:
            msg = _("No access_group_entry exists with ID %s.")
            raise exc.HTTPNotFound(explanation=msg % id)
 
        try:
            self.access_group_api.delete_access_group_entry(context,
                                                            access_group_entry)
        except exception.AccessGroupEntryException as e:
            raise exc.HTTPBadRequest(explanation=six.text_type(e))

        return webob.Response(status_int=202)

def create_resource():
    print("NMH 999999 access_groups.py i m here 66666666")
    return wsgi.Resource(AccessGroupEntriesController())
