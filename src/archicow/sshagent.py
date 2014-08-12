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
import os
import logging
import subprocess

_logger = logging.getLogger(__name__)


class SSHAgent(object):
    AGENT_PATH = '/usr/bin/ssh-agent'

    def start(self):
        self.agent_process = subprocess.Popen([self.AGENT_PATH, '-d', '-s', '>&2'],
                bufsize=1, stdout=subprocess.PIPE, shell=True)
        self.SSH_AGENT_PID = self.agent_process.pid
        while True:
            line = self.agent_process.stdout.readline()
            print 'line', line
            if line.startswith('SSH_AUTH_SOCK'):
                self.SSH_AUTH_SOCK = line.split('=')[1].split(';')[0]
                break
            elif not line:
                break
        os.environ['SSH_AUTH_SOCK'] = self.SSH_AUTH_SOCK
        os.environ['SSH_AGENT_PID'] = str(self.SSH_AGENT_PID)
        _logger.debug('SSH agent started with PID %d', self.SSH_AGENT_PID)
        return self

    def stop(self):
        self.agent_process.terminate()
        del(os.environ['SSH_AUTH_SOCK'])
        del(os.environ['SSH_AGENT_PID'])
        del(self.SSH_AUTH_SOCK)
        waitcount = 0
        while self.agent_process.poll() is None and waitcount < 30:
            waitcount += 1
            time.sleep(0.1)
        if self.agent_process.poll() is None:
            _logger.warning('SSH agent PID %d did not terminate in time, killing it',
                    self.SSH_AGENT_PID)
            self.agent_process.kill()
            del(self.agent_process)
        _logger.warning('SSH agent PID %d stopped', self.SSH_AGENT_PID)
        del(self.SSH_AGENT_PID)

    # context manager interface
    def __enter__(self):
        return self.start()

    def __exit__(self, type_, value_, traceback_):
        self.stop()
