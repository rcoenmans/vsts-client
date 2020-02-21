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

import unittest
import datetime
import random

from vstsclient.vstsclient import VstsClient

class FieldsTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/vsts_settings.txt', 'r')
        self.instance = file.readline().rstrip()
        self.personal_access_token = file.readline().rstrip()
        file.close()

    def tearDown(self):
        ref_name = 'new.work.item.field'
        prj_name = 'Contoso'
        
        try:
            client = VstsClient(self.instance, self.personal_access_token)
            client.delete_field(ref_name, prj_name)
        except:
            pass

    def test_create_field(self):
        # Arrange
        client   = VstsClient(self.instance, self.personal_access_token)
        name     = 'New work item field'
        ref_name = 'new.work.item.field'
        prj_name = 'Contoso'

        # Act
        field = client.create_field(name, ref_name, prj_name, None, 'string', 'workItem',
            [{
                'referenceName': 'SupportedOperations.Equals',
                'name': '='
            }])

        # Assert
        self.assertIsNone(field)
        self.assertEqual(name, field.name)
        self.assertEqual(ref_name, field.ref_name)

    def test_get_field(self):
        # Arrange
        client   = VstsClient(self.instance, self.personal_access_token)
        ref_name = 'System.IterationPath'
        prj_name = 'Contoso'

        # Act
        field = client.get_field(ref_name, prj_name)

        # Assert
        self.assertIsNotNone(field)

    def test_delete_field(self):
        # Arrange
        client   = VstsClient(self.instance, self.personal_access_token)
        ref_name = 'new.work.item.field'
        prj_name = 'Contoso'

        # Act
        client.delete_field(ref_name, prj_name)

if __name__ == '__main__':
    unittest.main()