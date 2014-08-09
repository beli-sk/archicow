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
from __future__ import print_function, absolute_import

import subprocess

from unipath import Path

from .base import BaseProcess, register_process
from ..storage import target_type


RSYNC = '/usr/bin/rsync'
SSH = '/usr/bin/ssh'


class RsyncProcess(BaseProcess):
    def __init__(self, config, storage_cls):
        self.user = config.getc('user')
        self.host = config.getc('host')
        self.port = config.getc('port', type_=int)
        self.source_path = Path(config.getc('source_path'))
        self.key_path = config.getc('key_path')
        self.target_path = Path(config.getc('target_path'))
        self.remote_sudo = config.getc('remote_sudo', type_=bool)
        self.exclude = config.getlist('exclude', default=[])
        self.storage = storage_cls(config.getc('target_base'))

    def backup(self):
        with self.storage.new_target(target_type.DIR, self.target_path) as target:
            print('rsync from {} to {}'.format(self.source_path, target.path))
            args = [RSYNC, '--archive', '--verbose', '--protect-args', '--del', '--delete-excluded']
            if target.inplace:
                args.append('--inplace')
            for pattern in self.exclude:
                args.extend(['--exclude', pattern])
            # ssh connection parameters
            ssh_args = [SSH]
            if self.user:
                ssh_args.extend(['-l', self.user])
            if self.key_path:
                ssh_args.extend(['-i', self.key_path])
            if self.port:
                ssh_args.extend(['-p', str(self.port)])
            args.extend(['-e', ' '.join(ssh_args)])
            # remote sudo
            if self.remote_sudo:
                args.extend(['--rsync-path', 'sudo rsync'])
            # source and destination
            if self.host:
                args.append('{}:{}/'.format(self.host, self.source_path))
            else:
                args.append('{}/'.format(self.source_path))
            args.append(target.path)
            print(repr(args))
            rsync = subprocess.Popen(args, shell=False)
            rsync.communicate()


register_process(RsyncProcess)

