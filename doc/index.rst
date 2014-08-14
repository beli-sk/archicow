.. ArchiCOW documentation master file

ArchiCOW documentation
======================

Contents:

.. toctree::
   :maxdepth: 2

   install
   config
   process
   storage
   scripts


Overview
~~~~~~~~

Backup system supporting copy-on-write storage.


Features
--------

* aims to be easy, admin friendly tool

  + runs from cron
  + simple filesystem structure of backups, accessible without need for special tools
  + outputs machine parsable status of your backups for monitoring tools (planned)

* pluggable backup methods

  + rsync over SSH
  + tar over SSH (planned)

* pluggable backup storage modules

  + simple file or directory
  + incremental with hard links between common files
  + BTRFS snapshot incremental storage (planned)

* optional remote helper scripts to prepare data for backup

  + create LVM snapshot for consistency
  + bind-mount root FS for clean backup without other mounts (planned)
  + dump database (planned)

Locations
~~~~~~~~~

The `project page <https://github.com/beli-sk/archicow>`_ is hosted on Github.

If you've never worked with *git* or contributed to a project on Github,
there is a `quick start guide <https://help.github.com/articles/fork-a-repo>`_.

If you find something wrong or know of a missing feature, please
`create an issue <https://github.com/beli-sk/archicow/issues>`_ on the project
page. If you find that inconvenient or have some security concerns, you could
also drop me a line at <devel@beli.sk>.


License
~~~~~~~

Copyright 2014 Michal Belica <devel@beli.sk>

::

    ArchiCOW is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    ArchiCOW is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with ArchiCOW.  If not, see < http://www.gnu.org/licenses/ >.

A copy of the license can be found in the ``LICENSE`` file in the
distribution.

