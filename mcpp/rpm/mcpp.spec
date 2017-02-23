#
# Copyright (c) 2008-2017 ZeroC, Inc. All rights reserved.
#

# the github version tag without v prefix
%define git_tag_version 2.7.2.12

Summary: mcpp, a portable C/C++ preprocessor
Name: mcpp-devel
Version: 2.7.2
Release: 5ice%{?dist}
Source: https://github.com/zeroc-ice/mcpp/archive/v%{git_tag_version}/mcpp-%{version}.tar.gz
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
%setup -q -n mcpp-%{git_tag_version}

%build
make CFLAGS="%{optflags}"

%install
make PREFIX=%{buildroot}%{_prefix} install

%files -n mcpp-devel
%doc LICENSE
%{_libdir}/libmcpp.a

%changelog
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
