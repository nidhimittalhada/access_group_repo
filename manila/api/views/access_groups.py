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

    _collection_name = 'access_groups'

    def summary_list(self, request, access_groups):
        """Show a list of access_groups without many details."""
        return self._list_view(self.summary, request, access_groups)

    def detail_list(self, request, access_groups):
        """Detailed view of a list of access groups."""
        return self._list_view(self.detail, request, access_groups)

    def _list_view(self, func, request, access_groups):
        """Provide a view for a list of access groups."""
        access_groups_list = [func(request, access_group)['access_group']
                          for access_group in access_groups]
        print("NMH 444444555555555666666666 access_groups_list",access_groups_list)                  
        access_groups_dict = {self._collection_name: access_groups_list}

        return access_groups_dict
    
    def summary(self, request, access_group):
        """Generic, non-detailed view of an access group."""
        return {
            'access_group': {
                'id': access_group.get('id'),
                'created_at': access_group.get('created_at'),
                'updated_at': access_group.get('updated_at'),
                'project_id': access_group.get('project_id'),
                'name': access_group.get('name'),
                'description': access_group.get('description'),
                'access_type': access_group.get('access_type'),
                'access_level': access_group.get('access_level')
                }
        }

    def detail(self, request, access_group):
        """Detailed view of a single access group."""
        print("NMH 1111 view access_group is",access_group)
        print("NMH 1111 view access_group entries is",access_group.access_group_entries)

        access_to_arr = []
        for ae in access_group.access_group_entries:
            access_to_arr.append(ae.get('access_to'))

        access_entry_count = len(access_to_arr)
        print("NMH 1111 ae_arr",access_to_arr)
        return {
            'access_group': {
                'id': access_group.get('id'),
                'created_at': access_group.get('created_at'),
                'updated_at': access_group.get('updated_at'),
                'project_id': access_group.get('project_id'),
                'name': access_group.get('name'),
                'description': access_group.get('description'),
                'access_type': access_group.get('access_type'),
                'access_level': access_group.get('access_level'),
                'access_to': str(access_to_arr),
                'access_entry_count': access_entry_count
            }
        }
