#
# ArchiCOW - Backup system supporting copy-on-write storage
# Copyright (C) 2014  Michal Belica <devel@beli.sk>
#
# This file is part of ArchiCOW.
#
# ArchiCOW is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ArchiCOW is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ArchiCOW.  If not, see <http://www.gnu.org/licenses/>.
#
import logging
import argparse
from collections import OrderedDict
from importlib import import_module

from .defs import __version__, app_name, app_description, app_name_desc
from .confparse import CustomConfigParser
from .storage import storage_types
from .process import process_types


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    # command line arguments
    parser = argparse.ArgumentParser(description=app_name_desc)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--config', '-c', metavar='FILE',
            help='config file name')
    group.add_argument('--version', '-V', action='version',
            help='show version and exit',
            version='{} {}'.format(app_name, __version__))
    parser.add_argument('--verbose', '-v', action='store_true',
            help='verbose output')
    parser.add_argument('jobs', metavar='JOB', nargs='+',
            help='backup job(s) to execute')
    args = parser.parse_args()

    if args.verbose:
        pass

    # read config file, with default values for optional fields
    config = CustomConfigParser()
    with open(args.config, 'r') as f:
        config.readfp(f, args.config)

    for job in args.jobs:
        logger.info('Starting job %s.', job)
        config.current_section = 'JOB:{}'.format(job)

        # import configured modules
        for mod in config.getc('modules').split():
            import_module(mod)

        process_cls = process_types[config.getc('process')]
        storage_cls = storage_types[config.getc('storage')]
        process = process_cls(config, storage_cls)
        process.backup()

