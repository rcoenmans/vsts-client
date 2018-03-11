# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2018 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import requests
import json

from ._http import HTTPRequest
from ._http.httpclient import _HTTPClient

from ._auth import _get_auth_header

from ._deserialize import (
    _parse_json_to_workitemtypes,
    _parse_json_to_projects,
    _parse_json_to_project,
    _parse_json_to_workitem,
    _parse_json_to_workitems,
    _parse_json_to_iteration,
    _parse_json_to_area,
    _parse_json_to_query_result
)

from ._conversion import (
    _datetime_to_utc_string
)

class VstsClient(object):
    def __init__(self, instance, personal_access_token):
        # VSTS: {account}.visualstudio.com
        # TFS:  server:port (the default port is 8080)
        self.instance = instance

        # https://docs.microsoft.com/en-us/vsts/integrate/get-started/authentication/pats
        self.personal_access_token = personal_access_token
        
        self._http_client = _HTTPClient(
            protocol = 'HTTPS',
            session  = requests.Session(),
            timeout  = 30,
        )

    def set_proxy(self, host, port, user, password):
        self._http_client.set_proxy(host, port, user, password)

    # GET {account}.visualstudio.com/DefaultCollection/_apis/projects
    def get_projects(self):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/_apis/projects'
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_projects)

    # GET {account}.visualstudio.com/DefaultCollection/_apis/projects/{project}?includeCapabilities=true&api-version=1.0
    def get_project(self, project_name):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/_apis/projects/{}'.format(project_name)
        request.query = 'includeCapabilities=true&api-version=1.0'
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_project)
    
    # POST {account}.visualstudio.com/DefaultCollection/_apis/projects?api-version=2.0-preview
    def create_project(self, name, description, source_control_type='Git', template_type_id='6b724908-ef14-45cf-84f8-768b5384da45'):
        # Create the payload
        payload = {
            'name': name,
            'description': description,
            'capabilities': {
                'versioncontrol': {
                    'sourceControlType': source_control_type
                },
                'processTemplate': {
                    'templateTypeId': template_type_id
                }
            }
        }

        # Create the HTTP Request
        request = HTTPRequest()
        request.method = 'POST'
        request.path = '/DefaultCollection/_apis/projects'
        request.query = 'api-version=2.0-preview'
        request.body = json.dumps(payload)
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_project)

    # GET {account}.visualstudio.com/DefaultCollection/{project}/_apis/wit/workItemTypes?api-version={version}
    def get_workitem_types(self, project_name):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/{}/_apis/wit/workItemTypes'.format(project_name)
        request.query = 'api-version=1.0'
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_workitemtypes)

    # GET {account}.visualstudio.com/DefaultCollection/{project}/_apis/wit/classificationNodes/areas?$depth={depth}&api-version=1.0
    def get_areas(self, project_name, depth=1):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/{}/_apis/wit/classificationNodes/areas'.format(project_name)
        request.query = '$depth={}&api-version=1.0'.format(depth)
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_area)

    # GET {account}.visualstudio.com/DefaultCollection/{project}/_apis/wit/classificationNodes/iterations/{iteration}?api-version=1.0
    def get_iteration(self, project_name, name):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/{}/_apis/wit/classificationNodes/iterations/{}'.format(project_name, name)
        request.query = 'api-version=1.0'
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_iteration)

    # POST {account}.visualstudio.com/DefaultCollection/{project}/_apis/wit/classificationNodes/iterations?api-version=1.0
    def create_iteration(self, project_name, name, start_date, finish_date):
        # Create the payload
        payload = {
            'name': name,
            'attributes': {
                'startDate': _datetime_to_utc_string(start_date),
                'finishDate': _datetime_to_utc_string(finish_date)
            }
        }
        
        # Create the HTTP Request
        request = HTTPRequest()
        request.method = 'POST'
        request.path = '/DefaultCollection/{}/_apis/wit/classificationNodes/iterations'.format(project_name)
        request.query = 'api-version=1.0'
        request.body = json.dumps(payload)
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request)

    # GET {account}.visualstudio.com/DefaultCollection/_apis/wit/workitems?ids=297,299,300&api-version=1.0
    def get_workitems_by_id(self, workitem_ids):  
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/DefaultCollection/_apis/wit/workitems'
        request.query = 'ids={}&api-version=1.0'.format(workitem_ids)
        request.headers = {
            'Content-Type': 'application/json'
        }
        return self._perform_request(request, _parse_json_to_workitems)
    
    # PATCH {account}.visualstudio.com/DefaultCollection/{project}/_apis/wit/workitems/${workItemTypeName}?api-version=1.0
    def create_workitem(self, project_name, workitem_type_name, title, description=None):
        # Create the payload
        payload = []
        payload.append({ 'op': 'add', 'path': '/fields/System.Title', 'value': str(title) })
        
        if description is not None:
            payload.append({ 'op': 'add', 'path': '/fields/System.Description', 'value': str(description) })
        
        # Create the HTTP Request
        request = HTTPRequest()
        request.method = 'PATCH'
        request.path = '/DefaultCollection/{}/_apis/wit/workitems/${}'.format(project_name, workitem_type_name)
        request.query = 'api-version=1.0'
        request.body = json.dumps(payload)
        request.headers = {
            'Content-Type': 'application/json-patch+json'
        }
        return self._perform_request(request, _parse_json_to_workitem)

    # POST {account}.visualstudio.com/DefaultCollection/[{project}/]_apis/wit/wiql?api-version={version}
    def query(self, query, project_name=None):
        request = HTTPRequest()
        request.method = 'POST'
        request.path = '/DefaultCollection/_apis/wit/wiql'
        request.query = 'api-version=1.0'
        request.headers = {
            'Content-Type': 'application/json'
        }
        request.body = json.dumps({ 'query': query })

        if project_name is not None:
            request.path = '/DefaultCollection/{}/_apis/wit/wiql'.format(project_name)

        return self._perform_request(request, _parse_json_to_query_result)


    def _perform_request(self, request, parser=None):
        request.host = self.instance
        request.headers['Accept'] = 'application/json'
        request.headers['Authorization'] = _get_auth_header(self.personal_access_token)

        response = self._http_client.perform_request(request)
        result = json.loads(response.body.decode('UTF-8'))

        if parser:
            return parser(result)
        else:
            return result