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
from vstsclient.models import Iteration

class IterationsTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/vsts_settings.txt', 'r')
        self.instance = file.readline().rstrip()
        self.personal_access_token = file.readline().rstrip()
        file.close()

    def test_get_iterations(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)
        
        # Act
        iters  = client.get_iterations('Contoso', 2)
        
        # Assert
        self.assertIsNotNone(iters)

    def test_get_iteration(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)
        
        # Act
        iteration = client.get_iteration('Contoso', 'Sprint A')
        
        # Assert
        self.assertIsNotNone(iteration)       
        self.assertIsInstance(iteration, Iteration) 

    def test_create_iteration(self):
        # Arrange
        client = VstsClient(self.instance, self.personal_access_token)
        
        name = 'Sprint {}'.format(random.randrange(99))
        start_date  = datetime.datetime.utcnow()
        finish_date = start_date + datetime.timedelta(days=21)
        
        # Act
        iteration = client.create_iteration('Contoso', name, start_date, finish_date)
        
        # Assert
        self.assertIsNotNone(iteration)

if __name__ == '__main__':
    unittest.main()