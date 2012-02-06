# Copyright (c) 2010 by Yaco Sistemas <pmartin@yaco.es>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README')
    + '\n' +
    'Authors\n'
    '************\n'
    + '\n' +
    read('AUTHORS')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES')
    + '\n' +
   'Download\n'
    '********\n')

setup(
    name="django-transmeta",
    version="0.6.6",
    author="Yaco Sistemas S.L.",
    author_email="garcia.marc@gmail.com",
    description="Transmeta is an application for translatable content in Django's models.",
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
    license="LGPL 3",
    keywords="django,translation,internationalization,i18n,transmeta,models,translation models",
    url='http://code.google.com/p/django-transmeta/',
    packages=find_packages('.'),
    package_dir= {'': '.'},
    zip_safe=False,
)
