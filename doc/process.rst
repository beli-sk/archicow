Process modules
===============

RsyncProcess
~~~~~~~~~~~~

Module file: ``archicow.process.rsync``

Use rsync over SSH to backup a directory on remote host to local target
directory (provided by a storage module).

Configuration parameters
------------------------

``user``
   Remote SSH user name.

``host``
   SSH host name/address to connect to.

``port``
   SSH port on remote host.

``key_path``
   Path to SSH key to use for the connection.

``exclude``
   Patterns to exclude from backup. Separate multiple patterns with two pipe
   symbols (``||``) without any extra whitespace. The patterns are passed to
   rsync as ``--exclude`` parameter. For details please see rsync
   documentation.

``rsync_args``
   Extra command line arguments for rsync.

``remote_sudo``
   Use sudo when running rsync on remote side.

``local_sudo``
   Run local rsync process with sudo.

