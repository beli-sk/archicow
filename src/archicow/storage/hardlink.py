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
import time
import errno
import logging
import subprocess
from unipath import Path

from .base import BaseStorage, BackupTarget, target_type, register


logger = logging.getLogger(__name__)


def filter_all(path):
    return not path.endswith('.work')


def filter_ok(path):
    return not path.endswith('.work') and not path.endswith('.fail')


class HardlinkStorage(BaseStorage):
    """Incremental storage, using hard links between unchanged files.
    Only for directory style backups, like rsync.
    """
    timestamp_format = '%Y-%m-%d_%H-%M-%S'
    cp_path = '/bin/cp'

    def __init__(self, basepath):
        self.basepath = Path(basepath)

    def list_backups(self, path, failed=False):
        target_prefix = Path(self.basepath, path)
        target_dir = target_prefix.parent
        target_name = target_prefix.name
        try:
            return target_dir.listdir(pattern='{}@*'.format(target_name),
                    filter=filter_all if failed else filter_ok)
        except OSError as e:
            if e.errno == errno.ENOENT:
                return None
            else:
                raise

    def get_latest_backup(self, path):
        try:
            return self.list_backups(path)[-1]
        except (IndexError, TypeError):
            return None

    def current_timestamp(self):
        return time.strftime(self.timestamp_format)

    def new_target(self, type_, path):
        target_path = Path(self.basepath, path)
        target_path_ts = Path('{}@{}.work'.format(target_path,
            self.current_timestamp()))
        if type_ == target_type.DIR:
            latest = self.get_latest_backup(path)
            if latest is None:
                target_path_ts.mkdir(parents=True)
            else:
                logger.debug('%s: creating %s from %s',
                        self.__class__.__name__, target_path_ts, latest)
                self._new_from(latest, target_path_ts)
        else:
            raise ValueError('HardlinkStorage supports only directory backups.')
        return BackupTarget(self, target_path_ts, inplace=False)

    def _new_from(self, src, dst):
        args = [self.cp_path, '-al', src, dst]
        subprocess.check_call(args, shell=False)

    def finalize(self, target, error):
        dst = None
        if target.path.endswith('.work'):
            dst = target.path.rsplit('.', 1)[0]
        if error:
            dst = (dst if dst else target.path) + '.fail'
        if dst:
            logger.debug('%s: renaming %s to %s',
                    self.__class__.__name__, target.path, dst)
            target.path.rename(dst)

register(HardlinkStorage)
