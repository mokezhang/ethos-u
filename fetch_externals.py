#!/usr/bin/env python

#
# Copyright (c) 2019-2020 Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import subprocess

def print_args(args, **kwargs):
    cwd = kwargs['cwd']

    if isinstance(args, list):
        args = ' '.join(args)

    print('%s$ %s' % (cwd, args))

def check_call(args, **kwargs):
    print_args(args, **kwargs)
    return subprocess.check_call(args, **kwargs)

def check_output(args, **kwargs):
    print_args(args, **kwargs)
    return subprocess.check_output(args, **kwargs)

class Git(object):
    def __init__(self, path, fetchurl, pushurl=None, revision='origin/master'):
        self.path = path
        self.fetchurl = fetchurl
        self.pushurl = pushurl
        self.revision = revision

    def init(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if not os.path.exists(os.path.join(self.path, '.git')):
            check_output(['git', 'init'], cwd=self.path)

    def remote_add(self, name, fetchurl):
        remotes = check_output(['git', 'remote'], cwd=self.path).decode('utf-8').split('\n')
        if not name in remotes:
            check_output(['git', 'remote', 'add', '-m', self.revision, name, self.fetchurl], cwd=self.path)

            if self.pushurl:
                check_output(['git', 'remote', 'set-url', '--add', '--push', name, self.pushurl], cwd=self.path)

    def fetch(self):
        check_output(['git', 'fetch'], cwd=self.path)

    def checkout(self, revision):
        rev = self.__get_rev(revision)
        check_output(['git', 'checkout', rev], stderr=subprocess.STDOUT, cwd=self.path)

    def clone(self):
        if not os.path.exists(os.path.join(self.path, '.git')):
            self.init()
            self.remote_add('origin', self.fetchurl)
            self.fetch()
            self.checkout(self.revision)

    def rebase(self):
        rev = self.__get_rev(self.revision)
        check_output(['git', 'rebase', rev], cwd=self.path)

    def __get_rev(self, revision):
        try:
            rev = check_output(['git', 'rev-parse', 'origin/' + self.revision], cwd=self.path)
        except:
            rev = check_output(['git', 'rev-parse', self.revision], cwd=self.path)

        return rev.decode('utf-8').strip()

basedir = os.path.dirname(os.path.realpath(__file__))

externals = [
    Git(os.path.join(basedir, 'core_software'), 'ssh://review.mlplatform.org:29418/ml/ethos-u/ethos-u-core-software', revision='master'),
    Git(os.path.join(basedir, 'core_software/core_driver'), 'ssh://review.mlplatform.org:29418/ml/ethos-u/ethos-u-core-driver', revision='master'),
    Git(os.path.join(basedir, 'core_software/cmsis'), 'https://github.com/ARM-software/CMSIS_5.git', revision='master'),
    Git(os.path.join(basedir, 'core_software/tensorflow'), 'https://github.com/tensorflow/tensorflow', revision='master'),
]

for external in externals:
    external.clone()
    external.fetch()
    external.rebase()
