# **********************************************************************
#
# Copyright (c) 2015 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

setup(
  name = 'zeroc-icehashpassword',
  packages = [""],
  package_dir = {"": "lib"},
  version = '1.0.2',
  description = 'ZeroC Ice hash password utility',
  author = 'ZeroC, Inc.',
  author_email = 'info@zeroc.com',
  url = 'https://github.com/zeroc-ice/ice',
  download_url = 'https://github.com/zeroc-ice/ice/archive/v1.0.2-icehashpassword.tar.gz',
  keywords = ['ice', 'hash', 'password'],
  install_requires = (["passlib >= 1.6.2"]),
  license='BSD',
  entry_points = {
      'console_scripts' : ["icehashpassword=icehashpassword:main"],
  },
  classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
  ],
)
