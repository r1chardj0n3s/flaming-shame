===========================
xstatic packages from bower
===========================

To create an xstatic package from a bower package, clone this repository
and run::

   tox -e xstatic <name of bower package>

The result should be a directory in `xstatic_packages/<name of package>`
which contains a PyPI-compatible xstatic package ready for release.

So, for example, to release an xstatic version of angular-smart-table:

    $ git clone https://github.com/r1chardj0n3s/flaming-shame.git
    [install "tox" if you don't have it already]
    $ tox -e xstatic angular-smart-table
    $ cd xstatic_packages/angular_smart_table/
    $ python setup.py sdist bdist_wheel upload --sign

----------

Copyright 2014, Rackspace, US, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
