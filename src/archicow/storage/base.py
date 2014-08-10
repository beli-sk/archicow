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

from ..xenum import XEnum


target_type = XEnum([
        (1, 'FILE'),
        (2, 'DIR'),
        ])

storage_types = {}


def register(storage):
    storage_types[storage.__name__] = storage


class BackupTarget(object):
    def __init__(self, storage, path, inplace=None):
        self.storage = storage
        self.path = path
        # Should use in-place overwrite
        # (True/False or None if doesn't matter)
        self.inplace = inplace

    # context manager interface
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.storage.finalize(self, type_ is not None)


class BaseStorage(object):
    def new_target(self, type_, path):
        """Prepare a target location for new backup.
        Returns BackupTarget instance.
        """
        raise NotImplemented

    def finalize(self, target, error):
        """Finalize the target location after backup."""
        pass

