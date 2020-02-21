# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2020 Robbie Coenmans
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
import logging

from ._http import HTTPRequest, HTTPError
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
    _parse_json_to_query_result,
    _parse_json_to_attachment,
    _parse_json_to_testplan,
    _parse_json_to_field
)

from ._conversion import _datetime_to_utc_string
from ._error import _validate_not_none
from ._hosts import _is_new_azure_devops_host

from .models import JsonPatchDocument, JsonPatchOperation

class VstsClient(object):
    def __init__(self, instance, personal_access_token, collection='DefaultCollection'):
        _validate_not_none('instance', instance)
        _validate_not_none('personal_access_token', personal_access_token)

        self.instance = instance if _is_new_azure_devops_host(instance) else '{}/{}'.format(instance, collection)
        self.personal_access_token = personal_access_token      
        self._http_client = _HTTPClient(
            protocol = 'HTTPS',
            session  = requests.Session(),
            timeout  = 30,
        )

        logging.basicConfig(level=logging.DEBUG, filename='vsts-client.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    def set_proxy(self, host, port, user, password):
        _validate_not_none('host', host)
        self._http_client.set_proxy(host, port, user, password)

    # GET {account}.visualstudio.com/{collection}/_apis/projects
    def get_projects(self, state='WellFormed', top=100, skip=0):
        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/_apis/projects'
        request.query   = 'api-version=1.0&stateFilter={}&$top={}&$skip={}'.format(state, top, skip)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_projects)

    # GET {account}.visualstudio.com/{collection}/_apis/projects/{project}?includeCapabilities=true&api-version=1.0
    def get_project(self, project_name):
        _validate_not_none('project_name', project_name)
        
        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/_apis/projects/{}'.format(project_name)
        request.query   = 'includeCapabilities=true&api-version=1.0'
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_project)
    
    # POST {account}.visualstudio.com/{collection}/_apis/projects?api-version=2.0-preview
    def create_project(self, name, description, source_control_type='Git', template_type_id='6b724908-ef14-45cf-84f8-768b5384da45'):
        _validate_not_none('name', name)
        _validate_not_none('description', description)

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
        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/_apis/projects'
        request.query   = 'api-version=2.0-preview'
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_project)

    # GET {account}.visualstudio.com/{collection}/{project}/_apis/wit/workItemTypes?api-version={version}
    def get_workitem_types(self, project_name):
        _validate_not_none('project_name', project_name)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/{}/_apis/wit/workItemTypes'.format(project_name)
        request.query   = 'api-version=1.0'
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_workitemtypes)

    def change_workitem_type(self, workitem_id: int, workitem_type_name):
        _validate_not_none('workitem_id', workitem_id)
        _validate_not_none('workitem_type_name', workitem_type_name)

        doc = JsonPatchDocument()
        doc.add(
            JsonPatchOperation(
                'add', 
                '/fields/System.WorkItemType', 
                '{}'.format(workitem_type_name)
            )
        )
        return self.update_workitem(workitem_id, doc)

    # GET {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/areas?$depth={depth}&api-version=1.0
    def get_areas(self, project_name, depth=1):
        _validate_not_none('project_name', project_name)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/{}/_apis/wit/classificationNodes/areas'.format(project_name)
        request.query   = '$depth={}&api-version=1.0'.format(depth)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_area)

    # GET {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/areas/{area}?api-version=1.0
    def get_area(self, project_name, name):
        _validate_not_none('project_name', project_name)
        _validate_not_none('name', name)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/{}/_apis/wit/classificationNodes/areas/{}'.format(project_name, name)
        request.query   = 'api-version=1.0'
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_area)

    # POST {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/areas?api-version=1.0
    def create_area(self, project_name, name):
        _validate_not_none('project_name', project_name)
        _validate_not_none('name', name)

        payload = { 'name': name }
        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/{}/_apis/wit/classificationNodes/areas'.format(project_name)
        request.query   = 'api-version=1.0'
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_area)

    # DELETE {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/areas/{area}?$reclassifyId={id}&api-version=1.0
    def delete_area(self, project_name, area_path, reclassify_id=''):
        _validate_not_none('project_name', project_name)
        _validate_not_none('area_path', area_path)

        request = HTTPRequest()
        request.method  = 'DELETE'
        request.path    = '/{}/_apis/wit/classificationNodes/areas/{}'.format(project_name, area_path)
        request.query   = 'api-version=1.0&$reclassifyId={}'.format(reclassify_id)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request)

    # GET {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/iterations?$depth={depth}&api-version=1.0
    def get_iterations(self, project_name, depth=1):
        _validate_not_none('project_name', project_name)
        
        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/{}/_apis/wit/classificationNodes/iterations'.format(project_name)
        request.query   = '$depth={}&api-version=1.0'.format(depth)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_iteration)

    # GET {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/iterations/{iteration}?api-version=1.0
    def get_iteration(self, project_name, name):
        _validate_not_none('project_name', project_name)
        _validate_not_none('name', name)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/{}/_apis/wit/classificationNodes/iterations/{}'.format(project_name, name)
        request.query   = 'api-version=1.0'
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_iteration)

    # POST {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/iterations?api-version=1.0
    def create_iteration(self, project_name, name, start_date, finish_date):
        _validate_not_none('project_name', project_name)
        _validate_not_none('name', name)
        _validate_not_none('start_date', start_date)
        _validate_not_none('finish_date', finish_date)

        payload = {
            'name': name,
            'attributes': {
                'startDate': _datetime_to_utc_string(start_date),
                'finishDate': _datetime_to_utc_string(finish_date)
            }
        }
        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/{}/_apis/wit/classificationNodes/iterations'.format(project_name)
        request.query   = 'api-version=1.0'
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_iteration)

    # DELETE {account}.visualstudio.com/{collection}/{project}/_apis/wit/classificationNodes/iterations/{iteration}?$reclassifyId={id}&api-version=1.0
    def delete_iteration(self, project_name, iteration_path, reclassify_id=''):
        _validate_not_none('project_name', project_name)
        _validate_not_none('iteration_path', iteration_path)

        request = HTTPRequest()
        request.method  = 'DELETE'
        request.path    = '/{}/_apis/wit/classificationNodes/iterations/{}'.format(project_name, iteration_path)
        request.query   = 'api-version=1.0&$reclassifyId={}'.format(reclassify_id)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request)

    def move_workitem(self, workitem_id, project_name, area_path, iteration_path):
        _validate_not_none('workitem_id', workitem_id)
        _validate_not_none('project_name', project_name)
        _validate_not_none('area_path', area_path)
        _validate_not_none('iteration_path', iteration_path)

        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation('add', '/fields/System.TeamProject', '{}'.format(project_name)))
        doc.add(JsonPatchOperation('add', '/fields/System.AreaPath', '{}'.format(area_path)))
        doc.add(JsonPatchOperation('add', '/fields/System.IterationPath', '{}'.format(iteration_path)))
        return self.update_workitem(workitem_id, doc)

    # GET {account}.visualstudio.com/{collection}/_apis/wit/workitems?ids=297,299,300&api-version=1.0
    def get_workitems_by_id(self, workitem_ids):
        _validate_not_none('workitem_ids', workitem_ids)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/_apis/wit/workitems'
        request.query   = 'ids={}&api-version=1.0'.format(workitem_ids)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_workitems)
    
    # GET {account}.visualstudio.com/{collection}/_apis/wit/workitems/{workitem_id}?api-version=1.0
    def get_workitem(self, workitem_id):
        _validate_not_none('workitem_id', workitem_id)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/_apis/wit/workitems/{}'.format(workitem_id)
        request.query   = 'api-version=1.0&$expand=all'
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_workitem)

    # PATCH {account}.visualstudio.com/{collection}/{project}/_apis/wit/workitems/${workItemTypeName}?api-version=1.0
    def create_workitem(self, project_name, workitem_type_name, document: JsonPatchDocument, bypass_rules=False):
        _validate_not_none('project_name', project_name)
        _validate_not_none('workitem_type_name', workitem_type_name)
        _validate_not_none('document', document)

        payload = []
        for operation in document:
            payload.append({ 'op': operation.op, 'path': operation.path, 'value': operation.value })
        
        request = HTTPRequest()
        request.method  = 'PATCH'
        request.path    = '/{}/_apis/wit/workitems/${}'.format(project_name, workitem_type_name)
        request.query   = 'api-version=1.0&bypassRules={}'.format(bypass_rules)
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json-patch+json'}
        return self._perform_request(request, _parse_json_to_workitem)

    # PATCH {account}.visualstudio.com/{collection}/_apis/wit/workitems/{workitem_id}?api-version=1.0
    def update_workitem(self, id: int, document: JsonPatchDocument, bypass_rules=False):
        _validate_not_none('id', id)
        _validate_not_none('document', document)

        payload = []
        for operation in document:
            payload.append({ 'op': operation.op, 'path': operation.path, 'value': operation.value })

        request = HTTPRequest()
        request.method  = 'PATCH'
        request.path    = '/_apis/wit/workitems/{}'.format(id)
        request.query   = 'api-version=1.0&bypassRules={}'.format(bypass_rules)
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json-patch+json'}
        return self._perform_request(request, _parse_json_to_workitem)

    # DELETE {account}.visualstudio.com/{collection}/_apis/wit/workitems/{workitem_id}?api-version=1.0
    def delete_workitem(self, id: int):
        _validate_not_none('id', id)

        request = HTTPRequest()
        request.method  = 'DELETE'
        request.path    = '/_apis/wit/workitems/{}'.format(id)
        request.query   = 'api-version=1.0'
        request.headers = {'content-type': 'application/json-patch+json'}
        self._perform_request(request)

    def add_tags(self, workitem_id: int, tags: list):
        _validate_not_none('workitem_id', workitem_id)
        _validate_not_none('tags', tags)

        doc = JsonPatchDocument()
        doc.add(
            JsonPatchOperation(
                'add',
                '/fields/System.Tags',
                '; '.join(tags)
            )
        )
        return self.update_workitem(workitem_id, doc)

    # PATCH {account}.visualstudio.com/{collection}/_apis/wit/workitems/{from_workitem_id}?api-version=1.0
    def add_link(self, from_workitem_id: int, to_workitem_id: int, link_type, comment):
        _validate_not_none('from_workitem_id', from_workitem_id)
        _validate_not_none('to_workitem_id', to_workitem_id)
        _validate_not_none('link_type', link_type)
        _validate_not_none('comment', comment)

        doc = JsonPatchDocument()
        doc.add(
            JsonPatchOperation(
                'add', 
                '/relations/-', 
                {
                    'rel': link_type,
                    'url': '{}://{}/_apis/wit/workItems/{}'.format(self._http_client.protocol, self.instance, to_workitem_id),
                    'attributes': {
                        'comment': comment
                    }
                }
            )
        )
        return self.update_workitem(from_workitem_id, doc)

    # PATCH {account}.visualstudio.com/{collection}/_apis/wit/workitems/{workitem_id}?api-version=1.0
    def add_hyperlink(self, workitem_id, url, comment=None):
        _validate_not_none('workitem_id', workitem_id)
        _validate_not_none('url', url)

        doc = JsonPatchDocument()
        doc.add(
            JsonPatchOperation(
                'add', 
                '/relations/-', 
                { 'rel': 'Hyperlink', 'url': url }
            )
        )

        # Optionally add a comment
        if comment is not None:
            doc.add(JsonPatchOperation('add', '/fields/System.History', comment))
        
        return self.update_workitem(workitem_id, doc)

    # POST {account}.visualstudio.com/{collection}/_apis/wit/attachments?api-version=1.0&filename={string}
    def upload_attachment(self, filename, data):
        _validate_not_none('filename', filename)
        _validate_not_none('data', data)

        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/_apis/wit/attachments'
        request.query   = 'api-version=1.0&filename={}'.format(filename)
        request.headers = {'content-type': 'application/octet-stream'}
        request.body    = data
        return self._perform_request(request, _parse_json_to_attachment)

    # PATCH {account}.visualstudio.com/{collection}/_apis/wit/workitems/{workitem_id}?api-version=1.0
    def add_attachment(self, workitem_id: int, attachment_url, comment):
        _validate_not_none('workitem_id', workitem_id)
        _validate_not_none('attachment_url', attachment_url)
        _validate_not_none('comment', comment)

        doc = JsonPatchDocument()
        doc.add(
            JsonPatchOperation(
                'add', 
                '/relations/-', 
                {
                    'rel': 'AttachedFile',
                    'url': attachment_url,
                    'attributes': {
                        'comment': comment
                    }
                }
            )
        )
        return self.update_workitem(workitem_id, doc)

    # POST {account}.visualstudio.com/{collection}/{project}/_apis/test/plans?api-version=1.0
    def create_testplan(self, project_name, name, description='', start_date=None, end_date=None):
        _validate_not_none('project_name', project_name)
        _validate_not_none('name', name)

        if start_date is None:
            start_date = datetime.datetime.utcnow()

        if end_date is None:    
            end_date = start_date + datetime.timedelta(days=7)

        payload = {
            'name': name,
            'description': description,
            'startDate': _datetime_to_utc_string(start_date),
            'endDate': _datetime_to_utc_string(end_date)
        }
        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/{}/_apis/test/plans'.format(project_name)
        request.query   = 'api-version=1.0'
        request.body    = json.dumps(payload)
        request.headers = {'content-type': 'application/json'}
        return self._perform_request(request, _parse_json_to_testplan)

    # POST {account}.visualstudio.com/{collection}/[{project}/]_apis/wit/wiql?api-version=1.0
    def query(self, query, project_name=None):
        _validate_not_none('query', query)

        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/_apis/wit/wiql'
        request.query   = 'api-version=1.0'
        request.headers = { 'Content-Type': 'application/json' }
        request.body    = json.dumps({ 'query': query })

        if project_name is not None:
            request.path = '/{}/_apis/wit/wiql'.format(project_name)

        return self._perform_request(request, _parse_json_to_query_result)

    # POST {account}.visualstudio.com/_apis/wit/fields?api-version=5.1
    def create_field(self, name, ref_name, project_name=None, description=None, field_type='string', field_usage='workItem', supported_operations=[], read_only=False, can_sort_by=True, is_queryable=True, is_identity=False, is_picklist=False, is_picklist_suggested=False, url=None):
        _validate_not_none('name', name)
        _validate_not_none('ref_name', ref_name)

        payload = {
            'name': name,
            'description': description,
            'referenceName': ref_name,
            'type': field_type,
            'usage': field_usage,
            'readOnly': read_only,
            'canSortBy': can_sort_by,
            'isQueryable': is_queryable,
            'supportedOperations': supported_operations,
            "isIdentity": is_identity,
            "isPicklist": is_picklist,
            "isPicklistSuggested": is_picklist_suggested,
            "url": url
        }

        request = HTTPRequest()
        request.method  = 'POST'
        request.path    = '/_apis/wit/fields'
        request.query   = 'api-version=5.1'
        request.headers = { 'Content-Type': 'application/json' }
        request.body    = json.dumps(payload)

        if project_name is not None:
            request.path = '/{}/_apis/wit/fields'.format(project_name)

        return self._perform_request(request, _parse_json_to_field)

    # GET {account}.visualstudio.com/{organization}/{project}/_apis/wit/fields/{fieldNameOrRefName}?api-version=5.1
    def get_field(self, field_name_or_ref_name, project_name=None):
        _validate_not_none('field_name_or_ref_name', field_name_or_ref_name)

        request = HTTPRequest()
        request.method  = 'GET'
        request.path    = '/_apis/wit/fields/{}'.format(field_name_or_ref_name)
        request.query   = 'api-version=5.1'
        request.headers = { 'Content-Type': 'application/json' }

        if project_name is not None:
            request.path = '/{}/_apis/wit/fields/{}'.format(project_name, field_name_or_ref_name)

        return self._perform_request(request, _parse_json_to_field)

    # DELETE {account}.visualstudio.com/{organization}/{project}/_apis/wit/fields/{fieldNameOrRefName}?api-version=5.1
    def delete_field(self, field_name_or_ref_name, project_name=None):
        _validate_not_none('field_name_or_ref_name', field_name_or_ref_name)

        request = HTTPRequest()
        request.method  = 'DELETE'
        request.path    = '/_apis/wit/fields/{}'.format(field_name_or_ref_name)
        request.query   = 'api-version=5.1'
        request.headers = { 'Content-Type': 'application/json' }

        if project_name is not None:
            request.path = '/{}/_apis/wit/fields/{}'.format(project_name, field_name_or_ref_name)

        self._perform_request(request)


    def _perform_request(self, request, parser=None):
        request.host = self.instance
        request.headers['Accept'] = 'application/json'
        request.headers['Authorization'] = _get_auth_header(self.personal_access_token)
        
        logging.debug(request.body)

        response = self._http_client.perform_request(request)
        
        logging.debug(response.body.decode('UTF-8'))

        if response.status >= 300:
            raise HTTPError(response.status, response.message, response.headers, response.body)

        result = json.loads(response.body.decode('UTF-8'))

        if parser:
            return parser(result)
        
        return result