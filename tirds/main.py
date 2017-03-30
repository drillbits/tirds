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

import argparse

from tirds import download
from tirds import upload


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    download_parser = subparsers.add_parser(
        'download',
        help="Download the backup files from Google Cloud Storage.")
    download_parser.add_argument(
        'handle',
        help="File handle for the backup_info, in the format `/gs/[BUCKET_NAME]/*.backup_info`.")
    download_parser.add_argument(
        '--out', dest='outdir',
        help="Write the backup files to OUTDIR.")
    download_parser.add_argument(
        '--key-file', dest='keyfile', required=True,
        help="Path to the private key file of the Google service account.")
    download_parser.set_defaults(func=download.download)

    upload_parser = subparsers.add_parser(
        'upload',
        help="Upload the backup files to Google Cloud Storage.")
    upload_parser.add_argument(
        'srcdir',
        help="Upload the backup files in the srcdir.")
    upload_parser.add_argument(
        'bucket',
        help="Upload the backup files to the bucket.")
    upload_parser.add_argument(
        '--key-file', dest='keyfile', required=True,
        help="Path to the private key file of the Google service account.")
    upload_parser.set_defaults(func=upload.upload)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
