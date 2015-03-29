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
import subprocess

from unipath import Path

from .base import BaseProcess, register_process
from ..storage import target_type


RSYNC = '/usr/bin/rsync'
SSH = '/usr/bin/ssh'
SUDO = '/usr/bin/sudo'

logger = logging.getLogger(__name__)

class RsyncProcess(BaseProcess):
    def __init__(self, config, storage_cls):
        self.user = config.getc('user')
        self.host = config.getc('host')
        self.port = config.getc('port', type_=int)
        self.source_path = config.getc('source_path')
        self.orig_source_path = self.source_path
        self.key_path = config.getc('key_path')
        self.target_path = Path(config.getc('target_path'))
        self.remote_sudo = config.getc('remote_sudo', type_=bool)
        self.local_sudo = config.getc('local_sudo', type_=bool)
        self.exclude = config.getlist('exclude', default=[])
        self.storage = storage_cls(config.getc('target_base'))
        self.prepare_script = config.getc('prepare_script')

    def backup(self):
        with self.storage.new_target(target_type.DIR, self.target_path) as target:
            logger.debug('rsync from %s to %s', self.source_path, target.path)
            args = [RSYNC, '--archive', '--verbose', '--protect-args', '--del', '--delete-excluded']
            if self.local_sudo:
                args.insert(0, SUDO)
            if target.inplace is not None:
                args.append('--inplace' if target.inplace else '--no-inplace')
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
            if self.prepare_script:
                if not self.prepare(ssh_args):
                    raise Exception('Prepare script failed')
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
            logger.debug('Running: %s', repr(args))
            rsync = subprocess.Popen(args, shell=False)
            rsync.communicate()
            if self.prepare_script:
                self.prepare(ssh_args, done=True)
            if rsync.returncode != 0:
                raise Exception('Rsync failed with code %d', rsync.returncode)

    def prepare(self, ssh_args, done=False):
        # call remote prepare script before and after backup
        ssh_args = ssh_args[:]
        ssh_args.append(self.host)
        if self.remote_sudo:
            ssh_args.append('sudo')
        ssh_args.append(self.prepare_script)
        if done:
            ssh_args.append('CLEANUP')
            ssh_args.append(self.orig_source_path)
        else:
            ssh_args.append('PREPARE')
            ssh_args.append(self.source_path)
        logger.debug('Prepare script: %s', repr(ssh_args))
        script = subprocess.Popen(ssh_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = script.communicate()
        out = out.strip()
        err = err.strip()
        if not done:
            if script.returncode != 0:
                logger.error('Remote prepare script failed with code %d', script.returncode)
                level = logging.ERROR
                ret = False
            else:
                self.source_path = out
                level = logging.DEBUG
                ret = True
        else:
            if script.returncode != 0:
                ret = False
                logger.error('Remote post-backup script failed with code %d', script.returncode)
                level = logging.ERROR
            else:
                ret = True
                level = logging.DEBUG
        if level:
            logger.log(level, 'Script output: %s', out)
            logger.log(level, 'Script stderr: %s', err)
        return ret


register_process(RsyncProcess)

