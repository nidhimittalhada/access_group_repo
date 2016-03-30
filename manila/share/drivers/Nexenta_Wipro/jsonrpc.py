# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2011 Nexenta Systems, Inc.
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
:mod:`nexenta.jsonrpc` -- Nexenta-specific JSON RPC client
=====================================================================

.. automodule:: nexenta.jsonrpc
.. moduleauthor:: Yuriy Taraday <yorik.sar@gmail.com>
"""

import urllib2
from manila import exception

import jsonutils
from oslo_log import log 
LOG = log.getLogger(__name__)


#class NexentaJSONException(nexenta.NexentaException):
#    pass


class NexentaJSONProxy(object):
    def __init__(self, url, user, password, auto=False, obj=None, method=None):
        self.url = url
        self.user = user
        self.password = password
        self.auto = auto
        self.obj = obj
        self.method = method

    def __getattr__(self, name):
        if not self.obj:
            obj, method = name, None
        elif not self.method:
            obj, method = self.obj, name
        else:
            obj, method = '%s.%s' % (self.obj, self.method), name
        return NexentaJSONProxy(self.url, self.user, self.password, self.auto,
                                obj, method)

    def __call__(self, *args):
        data = jsonutils.dumps({'object': self.obj,
                                'method': self.method,
                                'params': args})
        auth = ('%s:%s' % (self.user, self.password)).encode('base64')[:-1]
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Basic %s' % (auth,)}
        LOG.debug('Sending JSON Data: %(data)s.', {'data': data})
        request = urllib2.Request(self.url, data, headers)
        response_obj = urllib2.urlopen(request)
        if response_obj.info().status == 'EOF in headers':
            if self.auto and self.url.startswith('http://'):
                LOG.debug(('Auto switching to HTTPS connection to %(self.url)s'),
                         {'self.url':self.url})

                self.url = 'https' + self.url[4:]
                request = urllib2.Request(self.url, data, headers)
                response_obj = urllib2.urlopen(request)
            else:
                err_msg = (_('Bad response from server, No headers in server response'))
                LOG.error(err_msg)
                raise exception.InvalidShare(reason=err_msg)
        response_data = response_obj.read()
        LOG.debug(('Got response: %(response_data)s'), {'response_data':response_data})
        response = jsonutils.loads(response_data)
        if response.get('error') is not None:
                err_msg = response['error'].get('message', '')
                raise exception.InvalidShare(reason=err_msg)
        else:
            return response.get('result')
