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
def reverse_dict(d):
    "Return reverse dict with key-value pairs reversed."
    d2 = dict()
    for k, v in d.iteritems():
        d2[v] = k
    return d2

class XEnum(dict):
    def __init__(self, *a, **kw):
        super(XEnum, self).__init__(*a, **kw)
        # to bypass custom __setattr__()
        super(XEnum, self).__setattr__('rev', reverse_dict(self))

    def __setitem__(self, key, value):
        try:
            del(self.rev[self[key]])
        except KeyError:
            pass
        super(XEnum, self).__setitem__(key, value)
        self.rev[value] = key

    def __delitem__(self, key):
        del(self.rev[self[key]])
        super(XEnum, self).__delitem__(key)

    def __getattr__(self, name):
        try:
            return self.rev[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        try:
            del(self[self.rev[name]])
        except KeyError:
            pass
        self[value] = name

    def __delattr__(self, name):
        try:
            del(self[self.rev[name]])
        except KeyError:
            raise AttributeError

