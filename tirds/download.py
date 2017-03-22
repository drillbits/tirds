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

import os
from datetime import datetime

from google.cloud import storage

from tirds import backup
from tirds.log import getLogger

logger = getLogger(__name__)


def download(args):
    bucket_name, blob_name = backup.split_handle(args.handle)
    storage_client = storage.Client.from_service_account_json(args.keyfile)

    outdir = args.outdir
    if outdir is None:
        name = 'tirds_download_{0:%Y%m%d%H%M%S}'.format(datetime.now())
        outdir = os.path.abspath(os.path.join(os.getcwd(), name))
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    logger.info("download backup to %s", outdir)

    backup_info_filepath = _download(storage_client, bucket_name, blob_name, outdir)
    with open(backup_info_filepath, 'r') as fp:
        entities = backup.parse_backup_info_file(fp)
        entities.next()  # skip backup_info
        for entity in entities:
            for f in entity.get('files', []):
                blob_name = f[f.find(bucket_name) + len(bucket_name) + 1:]
                _download(storage_client, bucket_name, blob_name, outdir)


def _download(storage_client, bucket_name, blob_name, outdir):
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    dest = os.path.join(outdir, blob_name)

    destdir = os.path.dirname(dest)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    logger.info("download from %s/%s to %s", bucket_name, blob_name, dest)
    blob.download_to_filename(dest)
    return dest
