# **********************************************************************
#
# Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
#
# **********************************************************************

# Always prefer setuptools over distutils
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from distutils.extension import Extension
import sys, os, shutil, fnmatch

platform = sys.platform
if platform[:6] == 'darwin':
    platform = 'darwin'
elif platform[:5] == 'linux':
    platform = 'linux'
elif platform[:7] == 'freebsd':
    platform = 'freebsd'

use_ice = False
if "--with-installed-ice" in sys.argv:
    use_ice = True
    sys.argv.remove("--with-installed-ice")

#
# Sort out packages, package_dir and package_data from the lib dir.
#
packages = ['']
package_dir={'' : 'lib'}
for f in os.listdir('lib'):
    p = os.path.join('lib', f)
    if os.path.isdir(p):
        package_dir[f] = p
        packages.append(f)
package_data = { 'slice' : ['*/*.ice'] }

extra_compile_args=[]
if use_ice:
    include_dirs=['src']
    define_macros=[]
else:
    include_dirs=['src', 'src/ice/cpp/include', 'src/ice/cpp/src']
    define_macros=[('ICE_STATIC_LIBS', None)]

if platform == 'darwin':
    if not 'ARCHFLAGS' in os.environ:
        os.environ['ARCHFLAGS'] = '-arch x86_64'
    extra_compile_args.append('-w')
    if use_ice:
        libraries = ["IceSSL", "Ice", "Slice", "IceUtil"]
        extra_link_args = []
    else:
        libraries=['iconv']
        extra_link_args = ['-framework','Security', '-framework','CoreFoundation']

    def filterName(path):
        d = os.path.dirname(path)
        if use_ice and d.find("src/ice/") != -1:
            return False
        if d.find('bzip2') != -1:
            return False # Don't compile the bzip2 source under darwin or linux.
        return True

elif platform == 'win32':
    extra_link_args = []
    libraries=[]
    define_macros.append(('WIN32_LEAN_AND_MEAN', None))
    define_macros.append(('ICE_BUILDING_ICE_UTIL', None))
    define_macros.append(('ICE_BUILDING_SLICE', None))
    define_macros.append(('ICE_BUILDING_ICE', None))
    define_macros.append(('ICE_BUILDING_ICE_SSL', None))
    define_macros.append(('_WIN32_WINNT', '0x601'))
    include_dirs.append('src/ice/bzip2')
    extra_compile_args.append('/EHsc')
    extra_compile_args.append('/wd4250')
    extra_compile_args.append('/wd4251')
    extra_compile_args.append('/wd4275')
    extra_compile_args.append('/wd4996')
    libraries=['dbghelp', 'Shlwapi', 'rpcrt4','advapi32','Iphlpapi','secur32','crypt32','ws2_32']
    # SysLoggerI.cpp shouldn't be built under Windows.
    def filterName(path):
        b = os.path.basename(path)
        if b == 'SysLoggerI.cpp':
            return False
        return True

else:
    #
    # TODO: Get rid of this hack to remove -Wstrict-prototypes from the compiler options
    # when http://bugs.python.org/issue1222585 is fixed. Note that this hack doesn't work
    # with recent distutils versions which no longer allow overriding OPT in the env.
    #
    from distutils.sysconfig import get_config_vars
    (opt,) = get_config_vars('OPT')
    os.environ['OPT'] = " ".join(flag for flag in opt.split() if flag != '-Wstrict-prototypes')

    extra_compile_args.append('-w')
    extra_link_args = []
    if use_ice:
        libraries = ["IceSSL", "Ice", "Slice", "IceUtil"]
    else:
        libraries=['ssl', 'crypto', 'bz2', 'rt']
        if platform is not 'freebsd':
            libraries.append('dl')

    def filterName(path):
        d = os.path.dirname(path)
        if use_ice and d.find("src/ice/") != -1:
            return False
        if d.find('bzip2') != -1:
            return False # Don't compile the bzip2 source under darwin or linux.
        return True


# Gather the list of sources to compile.
sources = []
for root, dirnames, filenames in os.walk('src'):
  for filename in fnmatch.filter(filenames, '*.cpp'):
        n = os.path.join(root, filename)
        if filterName(n):
            sources.append(n)
  for filename in fnmatch.filter(filenames, '*.c'):
        n = os.path.join(root, filename)
        if filterName(n):
            sources.append(n)

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='zeroc-ice',

    version='3.6.3',

    description="Ice is a comprehensive RPC framework with support for Python, C++, .NET, Java, JavaScript and more.",

    long_description=long_description,

    # The project's main homepage.
    url='https://zeroc.com',

    # Author details
    author='ZeroC, Inc.',
    author_email='info@zeroc.com',

    # Choose your license
    license='GPL v2 with exceptions',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='RPC distributed systems development',

    packages = packages,
    package_dir = package_dir,
    package_data = package_data,

    entry_points = {
        'console_scripts': ['slice2py=slice2py:main'],
    },

    ext_modules=[
        Extension('IcePy', sources,
          extra_link_args=extra_link_args,
          define_macros=define_macros,
          include_dirs=include_dirs,
          extra_compile_args=extra_compile_args,
          libraries=libraries)
        ]
)
