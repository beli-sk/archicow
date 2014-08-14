Installation
============

This section covers installation methods supported by ArchiCOW.

.. note::

   Some content, specifically example prepare scripts are included only in the
   source distribution and are not installed on the target system.

   Therefore you need to extract them either from source file downloaded from
   PyPI or from a Git repository clone.

   It is planned to include them in a separate package for distributing on
   remote (backup source) hosts.

Install as a Python distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Easiest way to install ArchiCOW is from a release using `pip <https://pip.pypa.io/en/latest/>`_.

Either download the source distribution from
`ArchiCOW page <https://pypi.python.org/pypi/archicow>`_ at PyPI, download
and verify the PGP signature of the file, and use *pip* to install::

   pip install ./archicow-0.0.1.dev0.tar.gz

(replace the file name with the version you downloaded)

Or use *pip* to download and install the software directly from PyPI::

   pip install --pre archicow

.. note::

   The ``--pre`` parameter is needed to download a development or pre-release
   version as the final release is not available yet.


Install from Git repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you would like to contribute to the development or see the versioned
sources, you can visit `ArchiCOW project page <https://github.com/beli-sk/archicow>`_
at Github and clone or the repository from there.

If you've never worked with *git* or contributed to a project on Github,
there is a `quick start guide <https://help.github.com/articles/fork-a-repo>`_.

After you have cloned the repository to your local machine, from there you can run::

   python setup.py install

to install the package on your system, or run::

   python setup.py develop

to install in `development mode <http://pythonhosted.org/setuptools/setuptools.html#development-mode>`_
to be able to edit the sources while testing it.

You can use `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_
to install the distribution under a virtual environment separate from your
live system.

