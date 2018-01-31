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

from vstsclient import VstsClient
from vstsclient.models import (
    Project,
    Iteration,
    Workitem,
    WorkitemType,
    ProcessTemplate,
    SourceControlType
)

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
        projects = client.get_projects()
        project = client.get_project(projects[0].name)
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)

    def test_create_project(self):
        client = VstsClient(self.instance, self.personal_access_token)
        project = client.create_project('Essent', 'A test project for Essent', SourceControlType.Git, ProcessTemplate.Agile)
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)

    def test_get_workitems(self):
        client = VstsClient(self.instance, self.personal_access_token)
        workitems = client.get_workitems_by_id('1')
        self.assertIsNotNone(workitems)
        self.assertGreater(len(workitems), 0)
        self.assertIsInstance(workitems[0], Workitem)

    def test_get_iteration(self):
        client = VstsClient(self.instance, self.personal_access_token)
        projects = client.get_projects()
        project = projects[0]
        iteration = client.get_iteration(project.name, 'Sprint A')
        self.assertIsNotNone(iteration)       
        self.assertIsInstance(iteration, Iteration) 

    def test_create_iteration(self):
        client = VstsClient(self.instance, self.personal_access_token)
        projects = client.get_projects()
        project = projects[0]
        name = 'Sprint A'
        start_date = datetime.datetime.utcnow()
        finish_date = start_date + datetime.timedelta(days=21)
        iteration = client.create_iteration(project.name, name, start_date, finish_date)
        self.assertIsNotNone(iteration)

    def test_create_workitem(self):
        client = VstsClient(self.instance, self.personal_access_token)
        
        projects = client.get_projects()
        project = projects[0]
        self.assertIsInstance(project, Project)

        workitemtypes = client.get_workitem_types(project.name)
        userstory = None
        for workitemtype in workitemtypes:
            if workitemtype.name == 'User Story':
                userstory = workitemtype
        
        if userstory is not None:
            self.assertIsInstance(userstory, WorkitemType)
            workitem = client.create_workitem(project.name, userstory.name, 'Test story A', 'This is a test user story')
            self.assertIsNotNone(workitem)