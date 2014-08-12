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
# ArchiCOW LVM snapshot prepare script
# ====================================
#
ACT="$1"
VG="$2"
LV="$3"
MAXSNAP="$4" # PEs

LVSNAP="${LV}-archicow"
LVDEV="/dev/${VG}/${LV}"
SNAPDEV="/dev/${VG}/${LVSNAP}"
MNTDIR="/mnt/archicow-lvmsnap/${VG}/${LV}"

LVC="/sbin/lvcreate"
LVR="/sbin/lvremove"
VGD="/sbin/vgdisplay"
MNT="/bin/mount"
UMNT="/bin/umount"

PROG="$0"
function fail {
  echo "${PROG}: $2" >&2
  exit $1
}

# *** create snapshot
function create_snap {
  # get free PEs on VG
  VGFREE=$( vgdisplay -c "$VG" | cut -d: -f16 )
  [[ -z "$VGFREE" ]] && fail 1 "no free space in volume group ${VG}"
  if (( VGFREE > MAXSNAP )) ; then
    # limit snapshot size
    VGFREE="$MAXSNAP"
  fi
  # create snapshot
  $LVC -s -pr -l "${VGFREE}" -n "${LVSNAP}" "${LVDEV}" > /dev/null \
    || fail 1 "error creating snapshot"
  # create mountdir if it does not exist
  if [[ ! -d "${MNTDIR}" ]] ; then
    mkdir -p "${MNTDIR}" || fail 1 "error creating ${MNTDIR}"
  fi
  # mount the snapshot
  $MNT "${SNAPDEV}" "${MNTDIR}" -o ro || fail 1 "error mounting ${SNAPDEV}"
  echo "$MNTDIR"
}

# *** remove snapshot
function remove_snap {
  # unmount snapshot
  if [[ -d "${MNTDIR}" ]] ; then
    $UMNT "${MNTDIR}"
  fi
  # remove snapshot volume
  $LVR -f "${SNAPDEV}" >&2 || fail 1 "error removing snapshot ${SNAPDEV}"
  # remove snapshots mount dir
  rmdir "${MNTDIR}"
}

function show_help {
  echo "ArchiCOW LVM snapshot prepare script"
  echo ""
  echo "use: $PROG (\"PREPARE\" | \"CLEANUP\") VG LV MAX_PE"
  echo ""
  echo "where MAX_PE is the maximal size of the snapshot in physical extents."
  exit 1
}

if [[ "$ACT" == "CLEANUP" ]] ; then
  remove_snap
elif [[ "$ACT" == "PREPARE" ]] ; then
  create_snap
else
  show_help
fi
