# Copyright (c) 2016 Wipro Technologies
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

"""
Handles all requests relating to access groups.
"""

from oslo_config import cfg
from oslo_log import log
from oslo_utils import excutils
from oslo_utils import strutils
import six

from manila.common import constants
from manila.db import base
from manila import exception
from manila.i18n import _
from manila.scheduler import rpcapi as scheduler_rpcapi
from manila import share
from manila.share import rpcapi as share_rpcapi
from manila.share import share_types


CONF = cfg.CONF

LOG = log.getLogger(__name__)


class API(base.Base):
    """API for interacting with the share manager."""

    def __init__(self, db_driver=None):
        self.scheduler_rpcapi = scheduler_rpcapi.SchedulerAPI()
        self.share_rpcapi = share_rpcapi.ShareAPI()
        self.share_api = share.API()
        super(API, self).__init__(db_driver)

    def create(self, context, name=None, description=None,
               access_type=None, access_level=None):
        """Create new access group."""
        
        values = {
            'name': name,
            'description': description,
            'access_type': access_type,
            'access_level': access_level,
        }

        access_group = self.db.access_group_create(context, values)
        print("NMH 22222 access_group is",access_group)
        return access_group

    def get_access_group(self, context, ag_id):
        access_group = self.db.access_group_get(context, ag_id)
        print("NMH 8888 access_group/api.py access_group obtained is",access_group)
        print("NMH 8888 access_group/api.py access_group entries obtained is",access_group.access_group_entries)
        return access_group

    def get_all(self, context, detailed=False):
        access_groups = self.db.access_group_get_all(
            context, detailed=detailed)

        print("NMH 8888 access_group/api.py access_groups obtained is",access_groups)
        return access_groups

    def create_entry(self, context, access_group_id=None, access_to=None):
        """Create new access group entry."""
        
        values = {
            'access_group_id': access_group_id,
            'access_to': access_to,
        }

        access_group_entry = self.db.access_group_create_entry(context, values)
        print("NMH 22222 access_group entry is",access_group_entry)
        return access_group_entry

    def get_access_group_entry(self, context, access_group_entry_id):
        access_group_entry = self.db.access_group_get_entry(context, access_group_entry_id)
        print("NMH 8888 access_group/api.py access_group_entry obtained is",access_group_entry)
        return access_group_entry


    def get_all_access_group_entries_per_group(self, context, access_group_id):
        
        self.get_all_access_group_entries(context, access_group_id=access_group_id)
        
    def get_all_access_group_entries(self, context, access_group_id,
                                     sort_key='created_at', sort_dir='desc',
                                     detailed=False):
        
        #policy.check_policy(context, 'access_group_entries', 'get_all_access_group_entries')
        
        string_args = {'sort_key': sort_key, 
                       'sort_dir': sort_dir, 
                      }
        if access_group_id:
            string_args.update({'access_group_id': access_group_id})

        for k, v in string_args.items():
            print("NMH 222222 k, v is ",k, v)
            if not (isinstance(v, six.string_types) and v):
                msg = _("Wrong '%(k)s' filter provided: "
                        "'%(v)s'.") % {'k': k, 'v': string_args[k]}
                raise exception.InvalidInput(reason=msg)
       
        print("NMH 888888877777666 access_group_id is",access_group_id)
        access_group_entries = self.db.access_group_entries_get_all(
            context, access_group_id=access_group_id,
            sort_key=sort_key, sort_dir=sort_dir,
            detailed=detailed)

        print("NMH 8888 access_group_entry/api.py access_group_entries obtained is",access_group_entries)
        return access_group_entries

#    def delete_access_group_entry(self, context, access_group_entry):
        
#        access_group_entry = self.db.access_group_get_entry(context, access_group_entry['id'])
#        LOG.info(_LI("Deleting replica %s."), id)

#        self.db.access_group_delete_entry(context, access_group_entry['id'])

#        self.db.share_replica_update(
#            context, share_replica['id'],
#            {'status': constants.STATUS_DELETING,
#            'terminated_at': timeutils.utcnow()}
#       )

 #           self.share_rpcapi.delete_share_replica(
 #               context,
 #               share_replica['id'],
 #               host,
 #               share_id=share_replica['share_id'],
 #               force=force)

    def create_share_access_group_mapping(self, context, share_id=None, access_group_id=None):
        """Create share access group mapping."""

        values = {
            'share_id': share_id,
            'access_group_id': access_group_id,
        }

        share_access_group_mapping = self.db.create_share_access_group_mapping(context, values)
        print("NMH 22222 share_access_group_mapping is",share_access_group_mapping)
        return share_access_group_mapping

    def get_share_access_group_mapping(self, context, share_id=None, access_group_id=None):
        """Get share access group mapping."""

        values = {
            'share_id': share_id,
            'access_group_id': access_group_id,
        }
        try:
            share_access_group_mapping = self.db.get_share_access_group_mapping(
                context, values)
        except exception.ShareAccessGroupMappingNotFound:
            return None
 
        print("NMH 22222 share_access_group_mapping is",share_access_group_mapping)
        return share_access_group_mapping
    
    def delete_share_access_group_mapping(self, context, share_id=None, access_group_id=None):
        """delete share access group mapping."""

        values = {
            'share_id': share_id,
            'access_group_id': access_group_id,
        }

        self.db.share_access_group_mapping_destroy(context, values)
        print("NMH 22222 share_access_group_mapping is destroyed")


