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

from google.appengine.api import datastore
from google.appengine.api.files import records


def split_handle(handle):
    """Returns bucket name and blob name from gs file handle."""
    if not handle.startswith('/gs/'):
        raise ValueError("handle must start with '/gs/' prefix.")
    path = handle[len('/gs/'):]
    i = path.rindex('/')
    return path[:i], path[i+1:]


def parse_backup_info_file(fp):
    """Returns entities iterator from a backup_info file."""
    reader = records.RecordsReader(fp)
    version = reader.read()
    if version != '1':
        raise IOError('Unsupported version')
    return (datastore.Entity.FromPb(record) for record in reader)
