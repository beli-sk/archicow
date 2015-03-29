Configuration
=============

Invocation
~~~~~~~~~~

::

   usage: archicow [-h] (--config FILE | --version) [--verbose] JOB [JOB ...]

   ArchiCOW - Backup system supporting copy-on-write storage.

   positional arguments:
     JOB                   backup job(s) to execute

   optional arguments:
     -h, --help            show this help message and exit
     --config FILE, -c FILE
                           config file name
     --version, -V         show version and exit
     --verbose, -v         verbose output

For example to start a job named ``server_backup`` defined in the
configuration file (described in later sections), you would use::

   archicow -c /etc/archicow.conf server_backup


Configuration file
~~~~~~~~~~~~~~~~~~

Syntax
------

Configuration file structure is similar to INI files. It consists of sections,
led by a ``[section]`` header and followed by ``name: value`` entries, with
continuations in the style of RFC 822 (see section 3.1.1, "LONG HEADER FIELDS");
``name=value`` is also accepted. Note that leading whitespace is removed from
values.

Values can contain format strings in the form ``%(name)s`` which refer to other
values in the same section, or values in a special DEFAULT section.

Configuration files may include comments, prefixed by specific characters
(``#`` and ``;``). Comments may appear on their own in an otherwise empty line,
or may be entered in lines holding values or section names. In the latter case,
they need to be preceded by a whitespace character to be recognized as a
comment. Only semicolon ``;`` starts an inline comment, while hash-sign ``#``
does not.

Job specification
-----------------

Configuration file consists of a special DEFAULT section and sections
describing individual backup jobs. Parameters in the default section are used
as default values for every job unless they are overriden in the job section.

Sections defining backup jobs are named by the job name with ``JOB:`` prefix.

Job specification contains these common parameters:

``modules``
   Module files to load in Python import format. To load module files that are
   part of the ArchiCOW distribution, prefix the base file name with either
   ``archicow.storage.`` or ``archicow.process.`` for storage and process
   modules respectively, e.g.
   ``modules: archicow.process.rsync archicow.storage.hardlink``

``process``
   One of supported backup modules to use for the job.

``storage``
   Storage module to use.

``source_path``
   Path to directory on remote host to be backed up. If using prepare scripts,
   this value will serve as input to the prepare script which will return the
   real source path. See section on prepare scripts later in this document.

``target_base``
   Base path under which storage module operates.

``target_path``
   Path under target_base directory for the backup. Will be created as either
   file or directory, depending on the process module used. Furthermore,
   storage modules which support history will append a timestamp and possibly
   a status suffix to this name as described in Storage modules section later
   in this document.

``prepare_script``
   Path to remote prepare script. The script is executed before backup. It
   receives ``source_path`` value as command line argument and a new value of
   ``source_path`` is read from the script's standard output, which is then
   used as source of the backup. Scripts supplied with ArchiCOW are described
   in their own section later in this document.

Other parameters are used by the process modules. Please see their respective
sections later in this document.

Configuration file example
--------------------------

::

   [DEFAULT]
   target_base = /var/lib/archicow/backup
   process = RsyncProcess
   storage = HardlinkStorage
   # user defined parameter:
   config_dir = /etc/archicow
   
   [JOB:server_backup]
   
   # remote SSH user (optional)
   user = rbackup
   
   # remote host
   host = example.com
   
   # SSH key to use (optional)
   key_path = %(config_dir)s/keys/example_key
   
   # Source path on remote host
   source_path = /home/rbackup
   
   # Target path below target_base
   target_path = %(host)s/rbackup
   
   # Exclude list for rsync, patterns separated by ||
   exclude = file2||file3
   
   # Use sudo for remote rsync and prepare script
   remote_sudo = 1
   # Same for local rsync
   local_sudo

