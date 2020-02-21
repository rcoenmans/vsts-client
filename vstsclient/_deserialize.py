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

from .models import (
    Project,
    Iteration,
    Area,
    Workitem,
    WorkitemType,
    Attachment,
    QueryResult,
    TestPlan,
    Field
)

from ._conversion import _utc_string_to_datetime

def _parse_json_to_workitemtypes(response):
    workitemtypes = []
    for value in response['value']:
        workitemtypes.append(_parse_json_to_workitemtype(value))
    return workitemtypes

def _parse_json_to_workitemtype(response):
    attrs = ['id', 'name', 'url']
    return _map_attrs_values(WorkitemType, attrs, response)

def _parse_json_to_projects(response):
    projects = []
    for value in response['value']:
        projects.append(_parse_json_to_project(value))
    return projects

def _parse_json_to_project(response):
    attrs = ['id', 'name', 'url', 'state', 'revision', 'visibility', 'description', 'capabilities']
    return _map_attrs_values(Project, attrs, response)

def _parse_json_to_workitems(response):
    workitems = []
    for value in response['value']:
        workitems.append(_parse_json_to_workitem(value))
    return workitems

def _parse_json_to_workitem(response):
    attrs = ['id', 'rev', 'fields', 'url']
    return _map_attrs_values(Workitem, attrs, response)

def _parse_json_to_iteration(response):
    attrs = ['id', 'name', 'identifier', 'url']
    obj = _map_attrs_values(Iteration, attrs, response)
    
    if 'attributes' in response:
        obj.attributes.startDate = _utc_string_to_datetime(response['attributes']['startDate'])
        obj.attributes.finishDate = _utc_string_to_datetime(response['attributes']['finishDate'])
    
    if 'hasChildren' in response:
        obj.has_children = bool(response['hasChildren'])

        # Parse child iterations
        if obj.has_children:
            for child in response['children']:
                obj.children.append(_parse_json_to_iteration(child))

    return obj

def _parse_json_to_area(response):
    attrs = ['id', 'name', 'identifier', 'url']
    obj = _map_attrs_values(Area, attrs, response)
    
    if 'hasChildren' in response:
        obj.has_children = bool(response['hasChildren'])

        # Parse child areas
        if obj.has_children:
            for child in response['children']:
                obj.children.append(_parse_json_to_area(child))

    return obj

def _parse_json_to_query_result(response):
    result = QueryResult()
    result.query_type = response['queryType']
    result.as_of      = response['asOf']
    result.columns    = response['columns']
    
    # The actual query results
    if 'workItems' in response:
        result.rows = response['workItems']

    if 'workItemRelations' in response: 
        result.rows = response['workItemRelations']
    
    return result

def _parse_json_to_attachment(response):
    attachment = Attachment()
    attachment.id = response['id']
    attachment.url = response['url']
    return attachment

def _parse_json_to_testplan(response):
    attrs = ['id', 'name', 'description']
    obj = _map_attrs_values(TestPlan, attrs, response)
    obj.start_date = _utc_string_to_datetime(response['startDate'])
    obj.end_date   = _utc_string_to_datetime(response['endDate'])
    return obj

def _parse_json_to_field(response):
    attrs = ['name', 'description', 'type', 'url', 'usage']
    obj = _map_attrs_values(Field, attrs, response)

    obj.ref_name     = respone['referenceName']
    obj.read_only    = response['readOnly']
    obj.can_sort_by  = response['canSortBy']
    obj.is_identity  = response['isIdentity']
    obj.is_picklist  = response['isPicklist']
    obj.is_queryable = response['isQueryable']

    obj.is_picklist_suggested = response['isPicklistSuggested']
    obj.supported_operations  = response['supportedOperations']
    return obj

def _get_attr_value(attr, values, default=None):
    if attr in values:
        return values[attr]
    else:
        return default

def _map_attrs_values(result_class, attrs, values):
    result = result_class()
    for attr in attrs:
        if attr in values:
            setattr(result, attr, _get_attr_value(attr, values))

    return result