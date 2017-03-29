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

from copy import deepcopy

from google.appengine.api import datastore
from google.appengine.api.files import records


def split_handle(handle):
    """Returns bucket name and blob name from gs file handle."""
    if not handle.startswith('/gs/'):
        raise ValueError("handle must start with '/gs/' prefix.")
    path = handle[len('/gs/'):]
    i = path.rfind('/')
    if i < 0:
        raise ValueError("handle has no blob name.")
    return path[:i], path[i+1:]


def parse_backup_info_file(fp):
    """Returns entities iterator from a backup_info file."""
    reader = records.RecordsReader(fp)
    version = reader.read()
    if version != '1':
        raise IOError('Unsupported version')
    return (datastore.Entity.FromPb(record) for record in reader)


def write_backup_info(backup_info, blob_files, fp):
    with records.RecordsWriter(fp) as writer:
        writer.write('1')
        writer.write(backup_info.ToPb().SerializeToString())
        for kind_backup_files in blob_files:
            writer.write(kind_backup_files.ToPb().SerializeToString())


def convert_bucket(backup_info, blob_files, new_bucket_name):
    new_backup_info = deepcopy(backup_info)

    org_bucket_name, blob_name = split_handle(backup_info['gs_handle'])
    new_backup_info['gs_handle'] = '/gs/{0}/{1}'.format(new_bucket_name, blob_name)

    new_blob_files = []
    for kind_backup_files in blob_files:
        new_kind_backup_files = deepcopy(kind_backup_files)
        new_files = [
            f.replace(org_bucket_name, new_bucket_name)
            for f in kind_backup_files['files']]
        new_kind_backup_files['files'] = new_files
        new_blob_files.append(new_kind_backup_files)

    return new_backup_info, new_blob_files
