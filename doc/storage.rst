Storage modules
===============

HardlinkStorage
~~~~~~~~~~~~~~~

Module file: ``archicow.storage.hardlink``

Incremental storage implemented using hardlinks on local filesystem. This
module requires that the underlying filesystem supports hard links with
``cp -l`` command.

Incremental means that only changes between backups are recorded, common files
do not add to the total space used at the target filesystem.

Versions of the same backup job are named by appending an at-sign (``@``) and
timestamp to ``target_path`` directory in format ``YYYY-MM-DD_HH-MM-SS`` and
eventually a ``.fail`` suffix to failed backups.

A backup in progress is denoted by ``.work`` suffix, which is removed after
succesful backup or changed to ``.fail`` on error. If the backup process is
interrupted without a chance to clean up, the ``.work`` suffix will remain on
the incomplete backup.

BtrfsStorage
~~~~~~~~~~~~

Module file: ``archicow.storage.btrfs``

Incremental storage implemented using snapshots on Btrfs filesystem.

Incremental means that only changes between backups are recorded, common files
do not add to the total space used at the target filesystem.

Versions of the same backup job are named by appending an at-sign (``@``) and
timestamp to ``target_path`` subvolume in format ``YYYY-MM-DD_HH-MM-SS`` and
eventually a ``.fail`` suffix to failed backups.

A backup in progress is denoted by ``.work`` suffix, which is removed after
succesful backup or changed to ``.fail`` on error. If the backup process is
interrupted without a chance to clean up, the ``.work`` suffix will remain on
the incomplete backup.
