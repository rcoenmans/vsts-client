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

import unittest
import datetime

from vstsclient.vstsclient import VstsClient
from vstsclient.constants import (
    ProcessTemplate,
    SourceControlType,
    SystemFields,
    MicrosoftFields,
    LinkTypes
)
from vstsclient.models import (
    Project,
    Iteration,
    Workitem,
    WorkitemType,
    JsonPatchDocument,
    JsonPatchOperation
)
from vstsclient._http import HTTPError

class VstsClientTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/vsts_settings.txt', 'r')
        self.instance = file.readline().rstrip()
        self.personal_access_token = file.readline().rstrip()
        file.close()

    def test_get_all_projects(self):
        client = VstsClient(self.instance, self.personal_access_token)
        projects = client.get_projects()
        self.assertIsNotNone(projects)
        self.assertGreater(len(projects), 0)

    def test_get_project(self):
        client = VstsClient(self.instance, self.personal_access_token)
        project = client.get_project('Contoso')
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)

    def test_create_project(self):
        client = VstsClient(self.instance, self.personal_access_token)
        project = client.create_project('Contoso', 'A test project for Contoso', SourceControlType.GIT, ProcessTemplate.AGILE)
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)

    def test_get_iterations(self):
        client = VstsClient(self.instance, self.personal_access_token)
        iters  = client.get_iterations('Contoso', 2)
        self.assertIsNotNone(iters)

    def test_get_iteration(self):
        client = VstsClient(self.instance, self.personal_access_token)
        iteration = client.get_iteration('Contoso', 'Sprint A')
        self.assertIsNotNone(iteration)       
        self.assertIsInstance(iteration, Iteration) 

    def test_create_iteration(self):
        client = VstsClient(self.instance, self.personal_access_token)

        name = 'Sprint A'
        start_date = datetime.datetime.utcnow()
        finish_date = start_date + datetime.timedelta(days=21)
        iteration = client.create_iteration('Contoso', name, start_date, finish_date)
        self.assertIsNotNone(iteration)

    def test_get_areas(self):
        client = VstsClient(self.instance, self.personal_access_token)
        areas  = client.get_areas('Contoso', 2)
        self.assertIsNotNone(areas)

    def test_get_workitems(self):
        client = VstsClient(self.instance, self.personal_access_token)
        workitems = client.get_workitems_by_id('1')
        self.assertIsNotNone(workitems)
        self.assertGreater(len(workitems), 0)
        self.assertIsInstance(workitems[0], Workitem)

    def test_create_user_story(self):
        client = VstsClient(self.instance, self.personal_access_token)

        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Test Story D'))
        doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'This is a description'))
        doc.add(JsonPatchOperation('add', SystemFields.CREATED_BY, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.ASSIGNED_TO, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.TAGS, 'migrated'))
        doc.add(JsonPatchOperation('add', MicrosoftFields.VALUE_AREA, 'Architectural'))

        workitem = client.create_workitem('Contoso', 'User Story', doc)
        self.assertIsNotNone(workitem)

    def test_create_epic(self):
        client = VstsClient(self.instance, self.personal_access_token)

        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Epic B'))
        doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'This is *epic*'))
        doc.add(JsonPatchOperation('add', SystemFields.CREATED_BY, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.ASSIGNED_TO, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.TAGS, 'migrated'))
        doc.add(JsonPatchOperation('add', MicrosoftFields.VALUE_AREA, 'Architectural'))

        epic = client.create_workitem('Contoso', 'Epic', doc)
        self.assertIsNotNone(epic)

    def test_create_feature(self):
        client = VstsClient(self.instance, self.personal_access_token)

        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Flying car'))
        doc.add(JsonPatchOperation('add', SystemFields.DESCRIPTION, 'A flying car'))
        doc.add(JsonPatchOperation('add', SystemFields.CREATED_BY, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.ASSIGNED_TO, 'Robbie Coenmans <robbie.coenmans@hotmail.com>'))
        doc.add(JsonPatchOperation('add', SystemFields.TAGS, 'migrated'))
        doc.add(JsonPatchOperation('add', MicrosoftFields.VALUE_AREA, 'Business'))

        feature = client.create_workitem('Contoso', 'Feature', doc)
        self.assertIsNotNone(feature)

    def test_add_link(self):
        client = VstsClient(self.instance, self.personal_access_token)

        # Get a User Story
        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'This is just a test story'"
        result = client.query(query, 'Contoso')
        userstory_id = result.rows[0]['id']

        # Get a Feature
        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'Flying car'"
        result = client.query(query, 'Contoso')
        feature_id = result.rows[0]['id'] 

        # Link them together using a parent relationship
        client.add_link(userstory_id, feature_id, LinkTypes.PARENT, "This is a comment")

    def test_upload_attachment(self):
        client = VstsClient(self.instance, self.personal_access_token)

        with open('./tests/vsts_settings.txt', 'rb') as f:
            attachment = client.upload_attachment('vsts_settings.txt', f)
            self.assertIsNotNone(attachment)

    def test_add_attachment(self):
        client = VstsClient(self.instance, self.personal_access_token)
        attachment = None

        # Upload attachment
        with open('./tests/vsts_settings.txt', 'rb') as f:
            attachment = client.upload_attachment('vsts_settings.txt', f)
            
        # Find a workitem
        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'This is just a test story'"
        result = client.query(query, 'Contoso')
        id     = result.rows[0]['id']
        
        # Link the attachment
        workitem = client.add_attachment(id, attachment.url, 'Linking an attachment to a workitem test')
        self.assertIsNotNone(workitem)

    def test_query(self):
        client = VstsClient(self.instance, self.personal_access_token)

        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'This is just a test story'"
        result = client.query(query, 'Contoso')
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.rows)
        self.assertGreater(len(result.rows), 0)

    def test_http_error(self):
        client = VstsClient(self.instance, self.personal_access_token)
        try:
            client.get_workitem('invalid_id')
        except HTTPError as e:
            self.assertIsNotNone(e)

if __name__ == '__main__':
    unittest.main()