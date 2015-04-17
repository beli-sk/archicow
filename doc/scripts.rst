Prepare scripts
===============

ArchiCOW supports a method of preparing the source location for backup allowing
for a backup job to execute a script on the remote server which prepares the
data for backup and passes back a path to the prepared data.

This setup can be used for example for creating snapshots of volumes, dumping
database contents before backup, etc.

The script, specified by ``prepare_script`` configuration parameter, is called
through SSH on the remote host, with command line argument ``PREPARE`` followed
by value of ``source_path``. Standard output of the script is read back as the
new value for ``source_path`` parameter used for the backup process.

After the backup (succesful or not) the script is called with an argument
``CLEANUP`` followed by the original ``source_path`` value. However in case of
abrupt termination of the backup process the CLEANUP call may not get through.

The synopsis for calling the scripts is as follows::

   prepare_script ("PREPARE" | "CLEANUP") source_path

The script should print just one line on standard output, which will be used
as a value for ``source_path``.

In case of error, the script should terminate with non-zero exit code, printing
error description on standard error.

Scripts included in ArchiCOW distribution are covered in following sections.

Mount bind -- ``prepare_mountbind.sh``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bind-mount (``mount -o bind``) the source filesystem to another path before
backup. This may be needed mostly for the root filesystem to get a clean
view, without other filesystems mounted over it.

Expects ``source_path`` value with these components, separated by spaces::

   ORIGPATH NEWPATH

ORIGPATH
   The original mount moint.

NEWPATH
   New mount point to bind-mount to.

LVM snapshot -- ``prepare_lvmsnap.sh``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a snapshot of LVM volume for consistency before backup. The snapshot
will be mounted to a new directory under ``/mnt/archicow/`` and it's path will
be returned.

Expects ``source_path`` value with three components, separated by spaces::

   VG LV MAX_PE

VG
   Volume group name.

LV
   Logical volume name.

MAX_PE
   Maximum size of the snapshot, in physical extents. The actual size will be
   limited by free space in the volume group.

