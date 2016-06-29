# Copyright 2013 NetApp
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

from manila.api import common


class ViewBuilder(common.ViewBuilder):
    """Model a server API response as a python dictionary."""

    _collection_name = 'access_group_entries'

    def summary_list(self, request, access_group_entries):
        """Show a list of access_group_entries without many details."""
        return self._list_view(self.summary, request, access_group_entries)

    def detail_list(self, request, access_group_entries):
        """Detailed view of a list of access group_entries."""
        return self._list_view(self.detail, request, access_group_entries)

    def _list_view(self, func, request, access_group_entries):
        """Provide a view for a list of access group_entries."""
        access_group_entries_list = [func(request, access_group_entry)['access_group_entry']
                          for access_group_entry in access_group_entries]
        print("NMH 444455555666666 access_group_entries_list formed is ",access_group_entries_list)                  
        access_group_entries_dict = {self._collection_name: access_group_entries_list}
        return access_group_entries_dict
    
    def summary(self, request, access_group_entry):
        """Generic, non-detailed view of an access group entry."""
        return {
            'access_group_entry': {
                'id': access_group_entry.get('id'),
                'created_at': access_group_entry.get('created_at'),
                'updated_at': access_group_entry.get('updated_at'),
                'project_id': access_group_entry.get('project_id'),
                'access_group_id': access_group_entry.get('access_group_id'),
                'access_to': access_group_entry.get('access_to'),
                }
        }

    def detail(self, request, access_group_entry):
        """Detailed view of a single access group entry."""
        print("NMH 1111 view access_group_entry is",access_group_entry)
        print("NMH 1111 view related access group is ",access_group_entry.access_groups)
        
        return {
            'access_group_entry': {
                'id': access_group_entry.get('id'),
                'created_at': access_group_entry.get('created_at'),
                'updated_at': access_group_entry.get('updated_at'),
                'project_id': access_group_entry.get('project_id'),
                'access_group_id': access_group_entry.get('access_group_id'),
                'access_to': access_group_entry.get('access_to'),
                'access_group_name': access_group_entry.access_groups.get('name'),
                'access_level': access_group_entry.access_groups.get('access_level'),
                'access_type': access_group_entry.access_groups.get('access_type')
            }
        }
