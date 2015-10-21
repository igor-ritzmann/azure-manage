# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import argparse
import os
import subprocess
import sys

from azure_manage.config import Config


class Main:
    parser = argparse.ArgumentParser(description='Build image')
    parser.add_argument('--auto', action='store_true')
    parser.add_argument('--bindir', metavar='BINDIR', default=os.path.dirname(os.path.realpath(sys.argv[0])))
    parser.add_argument('--config', metavar='CONFIG', default=None)
    parser.add_argument('section', metavar='SECTION')
    parser.add_argument('version', metavar='VERSION')

    def __init__(self):
        args = self.parser.parse_args()
        self.bindir = args.bindir

        with open(args.config) as c:
            config_section = Config(c)[args.section]

        self.release = config_section['release']
        self.image_name = config_section['image_name'].format_map(vars(args))

    def __call__(self):
        os.umask(0o22)
        subprocess.check_call(
            (
                'sudo',
                'unshare', '--mount', '--pid', '--fork', '--mount-proc',
                os.path.join(self.bindir, 'azure_build_image_debian'),
                '--release', self.release,
                '--output', self.image_name,
                '--debootstrap-url', 'http://debian-archive.trafficmanager.net/debian',
            ),
        )


def main():
    Main()()