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
import random

from vstsclient.vstsclient import VstsClient
from vstsclient.constants import (
    SystemFields,
    MicrosoftFields,
    LinkTypes
)
from vstsclient.models import (
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

    def test_get_workitems(self):
        client = VstsClient(self.instance, self.personal_access_token)
        workitems = client.get_workitems_by_id('62')
        self.assertIsNotNone(workitems)
        self.assertGreater(len(workitems), 0)
        self.assertIsInstance(workitems[0], Workitem)

    def test_get_workitem_types(self):
        client = VstsClient(self.instance, self.personal_access_token)
        types = client.get_workitem_types('Contoso')
        self.assertIsNotNone(types)

    def test_create_user_story(self):
        client = VstsClient(self.instance, self.personal_access_token)

        doc = JsonPatchDocument()
        doc.add(JsonPatchOperation('add', SystemFields.TITLE, 'Test Story'))
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
        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'Test Story'"
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
        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'Test Story'"
        result = client.query(query, 'Contoso')
        id     = result.rows[0]['id']
        
        # Link the attachment
        workitem = client.add_attachment(id, attachment.url, 'Linking an attachment to a workitem test')
        self.assertIsNotNone(workitem)

    def test_query(self):
        client = VstsClient(self.instance, self.personal_access_token)

        query  = "Select [System.Id], [System.Title], [System.State] From WorkItems Where [System.Title] = 'Test Story'"
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