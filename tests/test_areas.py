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

from vstsclient.vstsclient import VstsClient

class AreasTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/vsts_settings.txt', 'r')
        self.instance = file.readline().rstrip()
        self.personal_access_token = file.readline().rstrip()
        file.close()

    def test_get_areas(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)
        
        # Act
        areas = client.get_areas('Contoso', 2)
        
        # Assert
        self.assertIsNotNone(areas)

    def test_create_area(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)
        
        # Act
        area = client.create_area('Contoso', 'Area {}'.format(random.randrange(99)))
        
        # Assert
        self.assertIsNotNone(area)

if __name__ == '__main__':
    unittest.main()