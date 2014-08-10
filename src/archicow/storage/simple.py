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
from unipath import Path

from .base import BaseStorage, BackupTarget, target_type, register


class SimpleStorage(BaseStorage):
    """Provide a plain file or directory. Creates directories in path if
    needed.
    """
    def __init__(self, basepath):
        self.basepath = Path(basepath)

    def new_target(self, type_, path):
        target_path = Path(self.basepath, path)
        if type_ == target_type.FILE:
            target_path.parent.mkdir(parents=True)
        elif type_ == target_type.DIR:
            target_path.mkdir(parents=True)
        else:
            raise ValueError('Unknown target type')
        return BackupTarget(self, target_path)


register(SimpleStorage)
