import logging
import os
import posixpath
import re
from subprocess import Popen
from subprocess import PIPE
from subprocess import CalledProcessError

try:
    from cStringIO import StringIO
    StringIO  # quiet "redefinition of unused ..." warning from pyflakes
except ImportError:
    from StringIO import StringIO

from mrjob.fs.local import LocalFilesystem
from mrjob.parse import is_uri
from mrjob.parse import urlparse
from mrjob.util import cmd_line
from mrjob.util import read_file


log = logging.getLogger('mrjob.fs.hadoop')

# used by mkdir()
HADOOP_FILE_EXISTS_RE = re.compile(r'.*File exists.*')

# used by ls()
HADOOP_LSR_NO_SUCH_FILE = re.compile(
    r'^lsr: Cannot access .*: No such file or directory.')

# used by rm() (see below)
HADOOP_RMR_NO_SUCH_FILE = re.compile(r'^rmr: hdfs://.*$')


class HadoopFilesystem(LocalFilesystem):

    def __init__(self, hadoop_bin):
        super(HadoopFilesystem, self).__init__()
        self._hadoop_bin = hadoop_bin

    def invoke_hadoop(self, args, ok_returncodes=None, ok_stderr=None,
                       return_stdout=False):
        """Run the given hadoop command, raising an exception on non-zero
        return code. This only works for commands whose output we don't
        care about.

        Args:
        ok_returncodes -- a list/tuple/set of return codes we expect to
            get back from hadoop (e.g. [0,1]). By default, we only expect 0.
            If we get an unexpected return code, we raise a CalledProcessError.
        ok_stderr -- don't log STDERR or raise CalledProcessError if stderr
            matches a regex in this list (even if the returncode is bad)
        return_stdout -- return the stdout from the hadoop command rather
            than logging it. If this is False, we return the returncode
            instead.
        """
        args = self._hadoop_bin + args

        log.debug('> %s' % cmd_line(args))

        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()

        log_func = log.debug if proc.returncode == 0 else log.error
        if not return_stdout:
            for line in StringIO(stdout):
                log_func('STDOUT: ' + line.rstrip('\r\n'))

        # check if STDERR is okay
        stderr_is_ok = False
        if ok_stderr:
            for stderr_re in ok_stderr:
                if stderr_re.match(stderr):
                    stderr_is_ok = True
                    break

        if not stderr_is_ok:
            for line in StringIO(stderr):
                log_func('STDERR: ' + line.rstrip('\r\n'))

        ok_returncodes = ok_returncodes or [0]

        if not stderr_is_ok and proc.returncode not in ok_returncodes:
            raise CalledProcessError(proc.returncode, args)

        if return_stdout:
            return stdout
        else:
            return proc.returncode

    def du(self, path_glob):
        """Get the size of a file, or None if it's not a file or doesn't
        exist."""
        if not is_uri(path_glob):
            return super(HadoopFilesystem, self).du(path_glob)

        stdout = self.invoke_hadoop(['fs', '-du', path_glob],
                                     return_stdout=True)

        try:
            return int(stdout.split()[1])
        except (ValueError, TypeError, IndexError):
            raise Exception(
                'Unexpected output from hadoop fs -du: %r' % stdout)

    def ls(self, path_glob):
        if not is_uri(path_glob):
            for path in super(HadoopFilesystem, self).ls(path_glob):
                yield path
            return

        components = urlparse(path_glob)
        hdfs_prefix = '%s://%s' % (components.scheme, components.netloc)

        stdout = self.invoke_hadoop(
            ['fs', '-lsr', path_glob],
            return_stdout=True,
            ok_stderr=[HADOOP_LSR_NO_SUCH_FILE])

        for line in StringIO(stdout):
            fields = line.rstrip('\r\n').split()
            # expect lines like:
            # -rw-r--r--   3 dave users       3276 2010-01-13 14:00 /foo/bar
            if len(fields) < 8:
                raise Exception('unexpected ls line from hadoop: %r' % line)
            # ignore directories
            if fields[0].startswith('d'):
                continue
            # not sure if you can have spaces in filenames; just to be safe
            path = ' '.join(fields[7:])
            yield hdfs_prefix + path

    def _cat_file(self, filename):
        if is_uri(filename):
            # stream from HDFS
            cat_args = self._hadoop_bin + ['fs', '-cat', filename]
            log.debug('> %s' % cmd_line(cat_args))

            cat_proc = Popen(cat_args, stdout=PIPE, stderr=PIPE)

            def stream():
                for line in cat_proc.stdout:
                    yield line

                # there shouldn't be any stderr
                for line in cat_proc.stderr:
                    log.error('STDERR: ' + line)

                returncode = cat_proc.wait()

                if returncode != 0:
                    raise CalledProcessError(returncode, cat_args)

            return read_file(filename, stream())
        else:
            # read from local filesystem
            return super(HadoopFilesystem, self)._cat_file(filename)

    def mkdir(self, path):
        self.invoke_hadoop(
            ['fs', '-mkdir', path], ok_stderr=[HADOOP_FILE_EXISTS_RE])

    def path_exists(self, path_glob):
        """Does the given path exist?

        If dest is a directory (ends with a "/"), we check if there are
        any files starting with that path.
        """
        if not is_uri(path_glob):
            return super(HadoopFilesystem, self).path_exists(path_glob)

        return bool(self.invoke_hadoop(['fs', '-test', '-e', path_glob],
                                        ok_returncodes=(0, 1)))

    def path_join(self, dirname, filename):
        if is_uri(dirname):
            return posixpath.join(dirname, filename)
        else:
            return os.path.join(dirname, filename)

    def rm(self, path_glob):
        if not is_uri(path_glob):
            super(HadoopFilesystem, self).rm(path_glob)

        if self.path_exists(path_glob):
            # hadoop fs -rmr will print something like:
            # Moved to trash: hdfs://hdnamenode:54310/user/dave/asdf
            # to STDOUT, which we don't care about.
            #
            # if we ask to delete a path that doesn't exist, it prints
            # to STDERR something like:
            # rmr: <path>
            # which we can safely ignore
            self.invoke_hadoop(
                ['fs', '-rmr', path_glob],
                return_stdout=True, ok_stderr=[HADOOP_RMR_NO_SUCH_FILE])

    def touchz(self, dest):
        if not is_uri(dest):
            super(HadoopFilesystem, self).touchz(dest)

        self.invoke_hadoop(['fs', '-touchz', dest])
