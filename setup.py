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

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as fp:
    long_description = fp.read()

version = '0.0.2'

setup(
    name='tirds',
    version=version,
    description='tirds is a command-line tool to backup and restore Google Cloud Datastore Entities via local',
    long_description=long_description,
    url='https://github.com/drillbits/tirds',
    author='drillbits',
    author_email='neji@drillbits.jp',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
    keywords='appengine gae datastore backup restore',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'appengine-sdk',  # TODO: unofficial `pip install`-able appengine SDK.
        'google-cloud-storage',
        'pyyaml',
    ],
    tests_require=[
        'pytest',
        'mock',
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'tirds=tirds.main:main',
        ],
    },
)
