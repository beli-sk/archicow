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
from configparser import SafeConfigParser, NoOptionError

class CustomConfigParser(SafeConfigParser):
    current_section = None

    def getc(self, option, default=None, section=None, type_=None):
        if section is None:
            section = self.current_section
        try:
            if type_ is None:
                return self.get(section, option)
            elif type_ is bool:
                return self.getboolean(section, option)
            else:
                return type_(self.get(section, option))
        except NoOptionError:
            return default

    def getlist(self, option, default=None, section=None):
        value = self.getc(option, section=section)
        if value is None:
            return default
        else:
            return value.split('||')

