# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2019 Robbie Coenmans
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
from vstsclient.models import TestPlan

class TestPlanTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/vsts_settings.txt', 'r')
        self.instance = file.readline().rstrip()
        self.personal_access_token = file.readline().rstrip()
        file.close()

    def test_create_testplan(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)  
        name = 'Test Plan {}'.format(random.randrange(99))
        desc = 'Description for {}'.format(name)
        
        # Act
        testplan = client.create_testplan('Contoso', name, desc)
        
        # Assert
        self.assertIsNotNone(testplan)
        self.assertEqual(name, testplan.name)
        self.assertEqual(desc, testplan.description)

    def test_create_testplan_with_start_and_end_date(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)  
        name = 'Test Plan {}'.format(random.randrange(99))
        desc = 'Description for {}'.format(name)
        start_date  = datetime.datetime.utcnow()
        end_date    = start_date + datetime.timedelta(days=21)
        
        # Act
        testplan = client.create_testplan('Contoso', name, desc, start_date, end_date)
        
        # Assert
        self.assertIsNotNone(testplan)
        self.assertEqual(name, testplan.name)
        self.assertEqual(desc, testplan.description)

if __name__ == '__main__':
    unittest.main()