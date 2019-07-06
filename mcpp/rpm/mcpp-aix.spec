#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

# the github version tag without v prefix
# TODO replace with line below once tagged
# %define git_tag_version 2.7.2.13
%define git_tag_version master

Summary: mcpp, a portable C/C++ preprocessor
Name: mcpp-devel
Version: 2.7.2
Release: 7ice%{?dist}
#Source: https://github.com/zeroc-ice/mcpp/archive/v%{git_tag_version}/mcpp-%{version}.tar.gz
Source: https://github.com/zeroc-ice/mcpp/archive/master/mcpp-%{version}.tar.gz
URL: http://mcpp.sourceforge.net/
License: BSD
Group: System Environment/Libraries

%description
mcpp is a C/C++ preprocessor with the following features.

    * Implements all of C90, C99 and C++98 specifications.
    * Provides a validation suite to test C/C++ preprocessor's conformance
      and quality comprehensively. When this validation suite is applied,
       mcpp distinguishes itself among many existing preprocessors.
    * Has plentiful and accurate diagnostics to check all the preprocessing
      problems such as latent bug or lack of portability in source code.
    * Has #pragma directives to output debugging information.
    * Is portable and has been ported to many compliler-systems, including
      GCC and Visual C++, on UNIX-like systems and Windows.
    * Preprocessors of various behavior modes are able to be generated from
      the source code.
    * Can be built either as a compiler-specific preprocessor to replace the
      resident preprocessor of a particular compiler system, or as a
      compiler-independent command, or even as a subroutine called from some
      other main program.
    * Provides comprehensive documents both in Japanese and in English.
    * Is an open source software released under BSD-style-license.

# disable debuginfo package
%define debug_package %{nil}

%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n mcpp-%{git_tag_version}

%build
# 32-bit first
make CC=xlc_r AR="ar -X32" CFLAGS="%{optflags} -qpic -q32 -D_LARGE_FILES"

# Remove 32-bit object files and add 64-bit objects
rm -f *.o
make CC=xlc_r AR="ar -X64" CFLAGS="%{optflags} -qpic -q64"

%install
make PREFIX=%{buildroot}%{_prefix} install
mkdir -p %{buildroot}/usr/lib
ln -s %{_libdir}/libmcpp.a %{buildroot}/usr/lib/libmcpp.a

# create pkgconfig file
mkdir %{buildroot}%{_libdir}/pkgconfig
cat << "EOF" > %{buildroot}%{_libdir}/pkgconfig/mcpp.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=/usr/lib

Name: mcpp
Version: %{version}
Description: %{summary}
URL: %{url}
Libs: -lmcpp
EOF

%files -n mcpp-devel
%doc LICENSE
%{_libdir}/libmcpp.a
/usr/lib/libmcpp.a
%{_libdir}/pkgconfig/mcpp.pc

%changelog
* Tue Jul 02 2019 Bernard Normier <bernard@zeroc.com> 2.7.2-7ice
- AIX fork of Linux spec file.

* Fri Mar 10 2017 Bernard Normier <bernard@zeroc.com> 2.7.2-6ice
- Added pkgconfig file

* Tue Feb 21 2017 Bernard Normier <bernard@zeroc.com> 2.7.2-5ice
- Simplified spec file
- Build with optflags

* Tue Apr 7 2015 Bernard Normier <bernard@zeroc.com>
- Update to use source from https://github:zeroc-ice/mcpp

* Wed Jan 14 2009 Dwayne Boone <dwayne@zeroc.com>
- mcpp 2.7.2 update

* Wed Apr 30 2008 Bernard Normier <bernard@zeroc.com>
- mcpp 2.7 update

* Thu Feb 7 2008  Bernard Normier <bernard@zeroc.com>
- Initial version
