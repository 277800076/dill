#!/usr/bin/env python
#
# Michael McKerns
# mmckerns@caltech.edu

from __future__ import with_statement
import os

# set version numbers
stable_version = '0.1a1'
target_version = '0.2a'
is_release = False

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('dill/info.py'):
    # is a source distribution, so use existing version
    from dill.info import this_version
elif stable_version == target_version:
    # we are building a stable release
    this_version = target_version
else:
    # we are building a distribution
    this_version = target_version + '.dev'
    if is_release:
      from datetime import date
      today = "".join(date.isoformat(date.today()).split('-'))
      this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""---------------------------------------------------
dill: a utility for serialization of python objects
---------------------------------------------------

Dill extends python's 'pickle' module for serializing and de-serializing
python objects to the majority of the built-in python types. Serialization
is the process of converting an object to a byte stream, and the inverse
of which is converting a byte stream back to on python object hierarchy.

Dill provides the user the same interface as the 'pickle' module, and
also includes some additional features. In addition to pickling python
objects, dill provides the ability to save the state of an interpreter
session in a single command.  Hence, it would be feasable to save a
interpreter session, close the interpreter, ship the pickled file to
another computer, open a new interpreter, unpickle the session and
thus continue from the 'saved' state of the original interpreter
session.

Dill can be used to store python objects to a file, but the primary
usage is to send python objects across the network as a byte stream.
Dill is quite flexible, and allows arbitrary user defined classes
and funcitons to be serialized.  Thus dill is not intended to be
secure against erroneously or maliciously constructed data. It is
left to the user to decide whether the data they unpickle is from
a trustworthy source.

Dill is part of pathos, a python framework for heterogeneous computing.
Dill is in the early development stages, and any user feedback is
highly appreciated. Contact Mike McKerns [mmckerns at caltech dot edu]
with comments, suggestions, and any bugs you may find.  A list of known
issues is maintained at http://dev.danse.us/trac/pathos/query.


Major Features
==============

Dill is capable of pickling the following standard types::

    - none, type, bool, int, long, float, complex, str, unicode,
    - tuple, list, dict, file, buffer, builtin,
    - both old and new style classes,
    - instances of old and new style classes,
    - set, frozenset, array, lambda,
    - standard functions, functions with yields, nested functions
    - cell, method, unboundmethod, module, code,
    - dictproxy, methoddescriptor, getsetdescriptor, memberdescriptor,
    - wrapperdescriptor, xrange, slice,
    - notimplemented, ellipsis, quit

Dill also provides the capability to::

    - save and load python interpreter sessions


Current Release
===============

The latest stable release version is dill-%(relver)s. You can download it here.
The latest stable version of dill is always available at:

    http://dev.danse.us/trac/pathos


Development Release
===================

If you like living on the edge, and don't mind the promise
of a little instability, you can get the latest development
release with all the shiny new features at:

    http://dev.danse.us/packages.


Installation
============

Dill is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf dill-%(thisver)s.tgz
    $ cd dill-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above. 

Alternately, dill can be installed with easy_install::

    [download]
    $ easy_install -f . dill


Requirements
============

Dill requires::

    - python, version >= 2.5, version < 3.0

Optional requirements::

    - setuptools, version >= 0.6


Usage Notes
===========

Probably the best way to get started is to look at the tests
that are provide within dill. See `dill.tests` for a set of scripts
that test dill's ability to serialize different python objects.
Since dill conforms to the 'pickle' interface, the examples and
documentation at http://docs.python.org/library/pickle.html also
apply to dill if one will `import dill as pickle`.


License
=======

Dill is distributed under a modified BSD license.

    >>> import dill
    >>> print dill.license()


Citation
========

If you use dill to do research that leads to publication,
we ask that you acknowledge use of dill by citing the
following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://dev.danse.us/trac/pathos


More Information
================

Please see http://dev.danse.us/trac/pathos or http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='dill/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# build the 'setup' call
setup_code = """
setup(name='dill',
      version='%s',
      description='a utility for serialization of python objects',
      long_description = '''%s''',
      author = 'Mike McKerns',
      maintainer = 'Mike McKerns',
      maintainer_email = 'mmckerns@caltech.edu',
      license = 'BSD',
      platforms = ['any'],
      url = 'http://www.cacr.caltech.edu/~mmckerns',
      classifiers = ('Intended Audience :: Developers',
                     'Programming Language :: Python',
                     'Topic :: Physics Programming'),

      packages = ['dill'],
      package_dir = {'dill':'dill'},
""" % (target_version, long_description)

# add dependencies
ctypes_version = '>=1.0.1'
import sys
if has_setuptools and hex(sys.hexversion) < '0x20500f0':
    setup_code += """
        install_requires = ['ctypes%s'],
""" % (ctypes_version)

# add the scripts, and close 'setup' call
setup_code += """    
      zip_safe=False,
      scripts=['scripts/unpickle.py'])
"""

# exec the 'setup' code
exec setup_code

# if dependencies are missing, print a warning
try:
    import ctypes
except ImportError:
    print "\n***********************************************************"
    print "WARNING: One of the following dependencies is unresolved:"
    print "    ctypes %s" % ctypes_version
    print "***********************************************************\n"


if __name__=='__main__':
    pass

# end of file
