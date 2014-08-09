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
import sys
import pkgutil

from unipath import Path

from .base import BaseProcess, process_types


process_lib_paths = [Path(__file__).parent]
for importer, package_name, _ in pkgutil.iter_modules(process_lib_paths):
    full_package_name = 'archicow.process.%s' % package_name
    if full_package_name not in sys.modules:
        module = importer.find_module(package_name
                ).load_module(full_package_name)
