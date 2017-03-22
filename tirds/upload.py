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
import StringIO
from contextlib import closing

from google.cloud import storage

from tirds import backup
from tirds.log import getLogger

logger = getLogger(__name__)


def find_info(path):
    for f in os.listdir(path):
        if f.endswith('.backup_info'):
            return os.path.join(path, f)
    return None


def upload(args):
    srcdir = args.srcdir
    new_bucket_name = args.bucket
    storage_client = storage.Client.from_service_account_json(args.keyfile)

    backup_info_filepath = find_info(srcdir)
    if backup_info_filepath is None:
        logger.warning("backup_info not found in %s", srcdir)
        raise ValueError("backup_info not found")
    blob_name = os.path.basename(backup_info_filepath)

    with open(backup_info_filepath, 'r') as fp:
        entities = backup.parse_backup_info_file(fp)
        org_backup_info = entities.next()
        org_blob_files = [entity for entity in entities]

    new_backup_info, new_blob_files = backup.convert_bucket(
        org_backup_info, org_blob_files, new_bucket_name)

    bucket = storage_client.get_bucket(new_bucket_name)
    blob = bucket.blob(blob_name)
    with closing(StringIO.StringIO()) as tmp:
        backup.write_backup_info(new_backup_info, new_blob_files, tmp)
        val = tmp.getvalue()
        tmp.seek(0, os.SEEK_END)
        size = tmp.tell()
    with closing(StringIO.StringIO(val)) as fp:
        logger.info("upload from %s to %s/%s", blob.name, bucket.name, blob.name)
        blob.upload_from_file(fp, size=size)

    for f in os.listdir(srcdir):
        if os.path.isdir(os.path.join(srcdir, f)):
            _upload(bucket, srcdir, f)

    logger.info("Uploads complete. Import Backup Information from /gs/%s/%s", new_bucket_name, blob_name)


def _upload(bucket, srcdir, filename):
    if os.path.isdir(os.path.join(srcdir, filename)):
        for f in os.listdir(os.path.join(srcdir, filename)):
            f = os.path.join(filename, f)
            _upload(bucket, srcdir, f)
    else:
        blob = bucket.blob(filename)
        logger.info("upload from %s to %s/%s", blob.name, bucket.name, blob.name)
        blob.upload_from_filename(os.path.join(srcdir, filename))
