#    Copyright 2017 drillbits
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest

import pytest


class TestSplitHandle(unittest.TestCase):
    def _getTarget(self):
        from tirds.backup import split_handle
        return split_handle

    def _callFUT(self, handle):
        target = self._getTarget()
        return target(handle)

    def test_normal(self):
        bucket_name, blob_name = self._callFUT('/gs/path/to.py')
        assert (bucket_name, blob_name) == ('path', 'to.py')

    def test_multilevel(self):
        bucket_name, blob_name = self._callFUT('/gs/path/to/handle.py')
        assert (bucket_name, blob_name) == ('path/to', 'handle.py')

    def test_not_gs(self):
        with pytest.raises(ValueError):
            self._callFUT('gs/path/to.py')
            self._callFUT('/gspath/to.py')

    def test_no_blob_name(self):
        with pytest.raises(ValueError):
            self._callFUT('gs/path.py')
