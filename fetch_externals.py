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

import argparse
import json
import os
import subprocess
import sys

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

###############################################################################
# Git class
###############################################################################

class Git(object):
    def __init__(self, pwd, path, fetchurl, pushurl=None, revision='origin/master'):
        self.pwd = pwd
        self.path = path
        self.absolutepath = os.path.join(pwd, path)
        self.fetchurl = fetchurl
        self.pushurl = pushurl
        self.revision = revision

    def init(self):
        if not os.path.exists(self.absolutepath):
            os.makedirs(self.absolutepath)

        if not os.path.exists(os.path.join(self.absolutepath, '.git')):
            check_output(['git', 'init'], cwd=self.absolutepath)

    def remote_add(self, name, fetchurl):
        remotes = check_output(['git', 'remote'], cwd=self.absolutepath).decode('utf-8').split('\n')
        if not name in remotes:
            check_output(['git', 'remote', 'add', '-m', self.revision, name, self.fetchurl], cwd=self.absolutepath)

            if self.pushurl:
                check_output(['git', 'remote', 'set-url', '--add', '--push', name, self.pushurl], cwd=self.absolutepath)

    def fetch(self):
        check_output(['git', 'fetch'], cwd=self.absolutepath)

    def checkout(self, revision):
        rev = self.__get_rev(revision)
        check_output(['git', 'checkout', rev], stderr=subprocess.STDOUT, cwd=self.absolutepath)

    def clone(self):
        if not os.path.exists(os.path.join(self.absolutepath, '.git')):
            self.init()
            self.remote_add('origin', self.fetchurl)
            self.fetch()
            self.checkout(self.revision)

    def rebase(self):
        rev = self.__get_rev(self.revision)
        check_output(['git', 'rebase', rev], cwd=self.absolutepath)

    def set_sha1(self):
        self.revision = self.__get_rev(self.revision)

    def get_dict(self):
        data = {}
        data['path'] = self.path
        data['fetchurl'] = self.fetchurl

        if self.pushurl:
            data['pushurl'] = self.pushurl

        data['revision'] = self.revision

        return data

    def __get_rev(self, revision):
        try:
            rev = check_output(['git', 'rev-parse', 'origin/' + self.revision], stderr=subprocess.STDOUT, cwd=self.absolutepath)
        except:
            rev = check_output(['git', 'rev-parse', self.revision], cwd=self.absolutepath)

        return rev.decode('utf-8').strip()

###############################################################################
# Externals class
###############################################################################

class Externals:
    def __init__(self, config):
        self.externals = []
        self.load_config(config)

    def load_config(self, config):
        self.pwd = os.path.dirname(os.path.realpath(config))

        with open(config, 'r') as fp:
            data = json.load(fp)

        for ext in data['externals']:
            git = Git(self.pwd, ext['path'], ext['fetchurl'], ext.get('pushurl', None), ext['revision'])
            self.externals.append(git)

    def fetch(self):
        for ext in self.externals:
            ext.clone()
            ext.fetch()
            ext.checkout(ext.revision)

    def set_sha1(self):
        for ext in self.externals:
            ext.set_sha1()

    def get_dict(self):
        data = { 'externals': [] }
        for ext in self.externals:
            data['externals'].append(ext.get_dict())

        return data

    def dump(self, fhandle):
        fhandle.write(json.dumps(self.get_dict(), sort_keys=False, separators=(',', ': '), indent=4))

###############################################################################
# Handle functions
###############################################################################

def handle_fetch(args):
    externals = Externals(args.configuration)
    externals.fetch()

def handle_dump(args):
    externals = Externals(args.configuration)

    if args.sha1:
        externals.set_sha1()

    externals.dump(sys.stdout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch external repositories.')
    parser.add_argument('-c', '--configuration', default='externals.json', help='Externals configuration file')
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('fetch', description='Fetch external repositories.')
    subparser.set_defaults(func=handle_fetch)

    subparser = subparsers.add_parser('dump', description='Dump configuration.')
    subparser.set_defaults(func=handle_dump)
    subparser.add_argument('-s', '--sha1', action='store_true', help='Replace revision with current SHA-1')

    args = parser.parse_args()

    if 'func' not in args:
        parser.print_help()
        sys.exit(2)

    sys.exit(args.func(args))

