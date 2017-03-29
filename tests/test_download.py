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

from mock import Mock


class TestInternalDownload(unittest.TestCase):
    def _getTarget(self):
        from tirds.download import _download
        return _download

    def _callFUT(self, storage_client, bucket_name, blob_name, outdir):
        target = self._getTarget()
        return target(storage_client, bucket_name, blob_name, outdir)

    def test_normal(self):
        from google.cloud import storage
        blob_mock = Mock(spec=storage.Blob)
        blob_mock.download_to_filename.return_value = None

        bucket_mock = Mock(spec=storage.Bucket)
        bucket_mock.blob.return_value = blob_mock

        storage_client_mock = Mock(spec=storage.Client)
        storage_client_mock.get_bucket.return_value = bucket_mock

        ret = self._callFUT(storage_client_mock, 'test-bucket', 'test-blob', 'test-outdir')

        assert storage_client_mock.get_bucket.call_count == 1
        assert storage_client_mock.get_bucket.call_args[0] == ('test-bucket',)
        assert bucket_mock.blob.call_count == 1
        assert bucket_mock.blob.call_args[0] == ('test-blob',)
        assert blob_mock.download_to_filename.call_count == 1
        assert blob_mock.download_to_filename.call_args[0] == ('test-outdir/test-blob',)
        assert ret == 'test-outdir/test-blob'
