# Copyright 2012 OpenStack Foundation
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

import copy

from heatclient.openstack.common.apiclient import base
from heatclient.openstack.common.py3kcompat import urlutils
from heatclient.openstack.common import strutils
from heatclient.v1 import stacks

DEFAULT_PAGE_SIZE = 20


class Resource(base.Resource):
    def __repr__(self):
        return "<Resource %s>" % self._info

    def update(self, **fields):
        self.manager.update(self, **fields)

    def delete(self):
        return self.manager.delete(self)

    def data(self, **kwargs):
        return self.manager.data(self, **kwargs)

    def to_dict(self):
        return copy.deepcopy(self._info)


class ResourceManager(stacks.StackChildManager):
    resource_class = Resource

    def list(self, stack_id):
        """Get a list of resources.
        :rtype: list of :class:`Resource`
        """
        url = '/stacks/%s/resources' % stack_id
        return self._list(url, "resources")

    def get(self, stack_id, resource_name):
        """Get the details for a specific resource.

        :param stack_id: ID of stack containing the resource
        :param resource_name: ID of resource to get the details for
        """
        stack_id = self._resolve_stack_id(stack_id)
        # Use urlutils for python2/python3 compatibility
        url_str = '/stacks/%s/resources/%s' % (
                  urlutils.quote(stack_id, ''),
                  urlutils.quote(strutils.safe_encode(resource_name), ''))
        resp, body = self.client.json_request('GET', url_str)
        return Resource(self, body['resource'])

    def metadata(self, stack_id, resource_name):
        """Get the metadata for a specific resource.

        :param stack_id: ID of stack containing the resource
        :param resource_name: ID of resource to get metadata for
        """
        stack_id = self._resolve_stack_id(stack_id)
        # Use urlutils for python2/python3 compatibility
        url_str = '/stacks/%s/resources/%s/metadata' % (
                  urlutils.quote(stack_id, ''),
                  urlutils.quote(strutils.safe_encode(resource_name), ''))
        resp, body = self.client.json_request('GET', url_str)
        return body['metadata']

    def generate_template(self, resource_name):
        # Use urlutils for python2/python3 compatibility
        url_str = '/resource_types/%s/template' % (
                  urlutils.quote(strutils.safe_encode(resource_name), ''))
        resp, body = self.client.json_request('GET', url_str)
        return body
