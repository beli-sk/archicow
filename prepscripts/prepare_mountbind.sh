#!/bin/bash
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
#----------------------------------------------------------------------
#
# ArchiCOW bind-mount prepare script
# ==================================
#
ACT="$1"
ORIGPATH="$2"
NEWPATH="$3"

MNT="/bin/mount"
UMNT="/bin/umount"

PROG="$0"
function fail {
  echo "${PROG}: $2" >&2
  exit $1
}

# *** bind-mount orig path to new path
function bind_mount {
  # create new path if it does not exist
  if [[ ! -d "${NEWPATH}" ]] ; then
    mkdir -p "${NEWPATH}" || fail 1 "error creating ${NEWPATH}"
  fi
  $MNT "${ORIGPATH}" "${NEWPATH}" -o bind || fail 1 "error mounting ${NEWPATH}"
  echo "$NEWPATH"
}

# *** remove snapshot
function bind_umount {
  $UMNT "${NEWPATH}" || fail 1 "error unmounting ${NEWPATH}"
  # remove snapshots mount dir
  rmdir "${NEWPATH}"
}

function show_help {
  echo "ArchiCOW bind-mount prepare script"
  echo ""
  echo "use: $PROG (\"PREPARE\" | \"CLEANUP\") ORIGPATH NEWPATH"
  exit 1
}

if [[ "$ACT" == "CLEANUP" ]] ; then
  bind_umount
elif [[ "$ACT" == "PREPARE" ]] ; then
  bind_mount
else
  show_help
fi
