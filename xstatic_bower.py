import gitconfig
import json
import os
import shutil
import subprocess
import sys
from os.path import join

__INIT__TEMPLATE = '''
"""
XStatic resource package

See package 'XStatic' for documentation and basic tools.
"""

# official name, upper/lowercase allowed, no spaces
DISPLAY_NAME = '{display_name}'

# name used for PyPi
PACKAGE_NAME = 'XStatic-%s' % DISPLAY_NAME

NAME = __name__.split('.')[-1] # package name (e.g. 'foo' or 'foo_bar')
                               # please use a all-lowercase valid python
                               # package name

VERSION = '{version}' # version of the packaged files, please use the upstream
                  # version number
BUILD = '1' # our package build number, so we can release new builds
             # with fixes for xstatic stuff.
PACKAGE_VERSION = VERSION + '.' + BUILD # version used for PyPi

DESCRIPTION = "%s %s (XStatic packaging standard)" % (DISPLAY_NAME, VERSION)

PLATFORMS = 'any'
CLASSIFIERS = []
KEYWORDS = '{keywords}'

# XStatic-* package maintainer:
{maintainer}

# this refers to the project homepage of the stuff we packaged:
HOMEPAGE = '{homepage}'

# this refers to all files:
LICENSE = '(same as %s)' % DISPLAY_NAME

from os.path import join, dirname
BASE_DIR = join(dirname(__file__), 'data')
# linux package maintainers just can point to their file locations like this:
#BASE_DIR = '/usr/share/javascript/' + NAME

# location of the Javascript file that's the entry point for this package, if
# one exists, relative to BASE_DIR
{main}

LOCATIONS = {{
    # CDN locations (if no public CDN exists, use an empty dict)
    # if value is a string, it is a base location, just append relative
    # path/filename. if value is a dict, do another lookup using the
    # relative path/filename you want.
    # your relative path/filenames should usually be without version
    # information, because either the base dir/url is exactly for this
    # version or the mapping will care for accessing this version.
    {cdn_locations}
}}
'''

README_TEMPLATE = '''
XStatic-{display_name}
{underline}

{display_name} javascript library packaged for setuptools (easy_install) / pip.

This package is intended to be used by **any** project that needs these files.

It intentionally does **not** provide any extra code except some metadata
**nor** has any extra requirements. You MAY use some minimal support code from
the XStatic base package, if you like.

You can find more info about the xstatic packaging way in the package
`XStatic`.
'''

SETUP_PY_TEMPLATE = '''
from xstatic.pkg import {name} as xs

# The README.txt file should be written in reST so that PyPI can use
# it to generate your project's PyPI page.
long_description = open('README.txt').read()

from setuptools import setup, find_packages

setup(
    name=xs.PACKAGE_NAME,
    version=xs.PACKAGE_VERSION,
    description=xs.DESCRIPTION,
    long_description=long_description,
    classifiers=xs.CLASSIFIERS,
    keywords=xs.KEYWORDS,
    maintainer=xs.MAINTAINER,
    maintainer_email=xs.MAINTAINER_EMAIL,
    license=xs.LICENSE,
    url=xs.HOMEPAGE,
    platforms=xs.PLATFORMS,
    packages=find_packages(),
    namespace_packages=['xstatic', 'xstatic.pkg', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
'''

MANIFEST_IN_TEMPLATE = '''include README.txt
recursive-include xstatic/pkg/{name} *

global-exclude *.pyc
global-exclude *.pyo
global-exclude *.orig
global-exclude *.rej
'''


def main():
    bower_package = sys.argv[1]
    if subprocess.call('node_modules/.bin/bower install {}'.format(
            bower_package), shell=True):
        return
    name = bower_package.lower()

    with open(join('bower_components', bower_package, '.bower.json')) as f:
        bower_json = json.load(f)

    display_name = bower_json['name']
    version = bower_json['version']
    underline = '-' * len('xstatic-' + display_name)
    homepage = bower_json['homepage']
    if 'main' in bower_json:
        main = "MAIN='{}'".format(bower_json['main'])
    else:
        main = ''
    keywords = ' '.join(bower_json.get('keywords', []) + [name, 'xstatic'])

    # TODO? (I'm not sure this stuff even exists in bower)
    cdn_locations = ''

    # grab maintainer info from git config
    git = gitconfig.config("~/.gitconfig")
    maintainer = "MAINTAINER = '{}'\nMAINTAINER_EMAIL = '{}'".format(
        git.user.name, git.user.email)

    # make that deep directory
    xstatic_dir = join('xstatic_packages', name, 'xstatic')
    shutil.rmtree(xstatic_dir)
    os.makedirs(join(xstatic_dir, 'pkg', name))
    with open(join(xstatic_dir, '__init__.py'), 'w') as f:
        f.write("__import__('pkg_resources').declare_namespace(__name__)\n")
    with open(join(xstatic_dir, 'pkg', '__init__.py'), 'w') as f:
        f.write("__import__('pkg_resources').declare_namespace(__name__)\n")

    # copy over the data
    shutil.copytree(join('bower_components', bower_package),
        join(xstatic_dir, 'pkg', name, 'data'))

    # write the package meta-data
    with open(join('xstatic_packages', name, 'README.txt'), 'w') as f:
        f.write(README_TEMPLATE.format(**locals()))
    with open(join('xstatic_packages', name, 'setup.py'), 'w') as f:
        f.write(SETUP_PY_TEMPLATE.format(**locals()))
    with open(join('xstatic_packages', name, 'MANIFEST.in'), 'w') as f:
        f.write(MANIFEST_IN_TEMPLATE.format(**locals()))
    with open(join(xstatic_dir, 'pkg', name, '__init__.py'), 'w') as f:
        f.write(__INIT__TEMPLATE.format(**locals()))

    print '\nCongratulations, please find your new XStatic-{} package in' \
        .format(display_name)
    print join('xstatic_packages', name), '\n'


if __name__ == '__main__':
    main()
