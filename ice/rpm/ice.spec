# **********************************************************************
#
# Copyright (c) 2003-2017 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

%if "%{dist}" == ".sles12"
# SLES 12 should only be built on x86_64
ExcludeArch: %{ix86}
%endif

%define cpp11 0

%define systemd 0
%define systemdpkg bogus

%define shadow bogus

# Define slice2cs=1 to generate an RPM package containing the Slice-to-C# compiler.
%if "%{?slice2cs}" == ""
  %define slice2cs 0
%endif

%if "%{dist}" == ".el6"
  %define shadow shadow-utils
%endif
%if "%{dist}" == ".el7"
  %define systemd 1
  %define systemdpkg systemd
  %define cpp11 1
  %define shadow shadow-utils
%endif
%if "%{dist}" == ".amzn1"
  %define shadow shadow-utils
%endif
%if "%{dist}" == ".sles11"
  %define shadow pwdutils
%endif
%if "%{dist}" == ".sles12"
  %define systemd 1
  %define systemdpkg systemd-rpm-macros
  %define cpp11 1
  %define shadow shadow
%endif

%define buildall 1
%define runpath embedded_runpath=no

%define core_arches %{ix86} x86_64

#
# cppx86 indicates whether we're building x86 binaries on an x64 platform
#
%define cppx86 0

%ifarch %{ix86}
%if 0%{?biarch}
%define cppx86 1
%endif
%endif

Name: %{?nameprefix}ice
Version: 3.6.4
Summary: Comprehensive RPC framework with support for C++, .NET, Java, Python, JavaScript and more.
Release: 1%{?dist}
%if "%{?ice_license}"
License: %{ice_license}
%else
License: GPL v2 with exceptions
%endif
Group: System Environment/Libraries
Vendor: ZeroC, Inc.
URL: https://zeroc.com/
Source0: Ice-%{version}.tar.gz
Source1: Ice-rpmbuild-%{version}.tar.gz

BuildRoot: %{_tmppath}/ice-%{version}-%{release}-root-%(%{__id_u} -n)

%define soversion 36
%define mmversion 3.6

%define commonversion 1.8.0
%define formsversion 1.8.0
%define looksversion 2.6.0

#
# RHEL7 includes Berkeley DB 5.3.21, on other platforms we supply 5.3.28.
#
%if "%{dist}" == ".el7"
%define dbversion 5.3.21
%else
%define dbversion 5.3.28
%endif

BuildRequires: openssl-devel >= 0.9.7a
BuildRequires: mcpp-devel >= 2.7.2
%if 0%{?biarch}
BuildRequires: openssl-devel(x86-32) >= 0.9.7a
BuildRequires: mcpp-devel(x86-32) >= 2.7.2
%endif

%if "%{dist}" == ".el7"
BuildRequires: libdb-cxx-devel >= %{dbversion}, libdb-java >= %{dbversion}
%if 0%{?biarch}
BuildRequires: libdb-cxx-devel(x86-32) >= %{dbversion}
%endif
BuildRequires: javapackages-tools
%else
BuildRequires: db53-devel >= %{dbversion}, db53-java >= %{dbversion}
%if "%{dist}" != ".sles12"
BuildRequires: jpackage-utils
%endif
%endif

%if "%{dist}" == ".el6"
BuildRequires: bzip2-devel >= 1.0.5
BuildRequires: expat-devel >= 2.0.1
%if 0%{?biarch}
BuildRequires: bzip2-devel(x86-32) >= 1.0.5
BuildRequires: expat-devel(x86-32) >= 2.0.1
%endif
BuildRequires: php-devel >= 5.3.2
%endif
%if "%{dist}" == ".el7"
BuildRequires: bzip2-devel >= 1.0.6
BuildRequires: expat-devel >= 2.1
%if 0%{?biarch}
BuildRequires: bzip2-devel(x86-32) >= 1.0.6
BuildRequires: expat-devel(x86-32) >= 2.1
%endif
BuildRequires: php-devel >= 5.4
%endif
%if "%{dist}" == ".amzn1"
BuildRequires: bzip2-devel >= 1.0.6
BuildRequires: expat-devel >= 2.0.1
BuildRequires: php-devel >= 5.3.2
BuildRequires: php-devel < 5.4
%endif
%if "%{dist}" == ".sles11"
BuildRequires: libbz2-devel >= 1.0.5
BuildRequires: php53-devel >= 5.3.0
BuildRequires: libexpat-devel >= 2.0
%endif
%if "%{dist}" == ".sles12"
BuildRequires: libbz2-devel >= 1.0.6
BuildRequires: libexpat-devel >= 2.1
BuildRequires: php5-devel >= 5.5
%endif

%description
Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# Arch-independent packages
#
%ifarch noarch

%package -n %{?nameprefix}ice-slice
Summary: Slice files for Ice.
Group: System Environment/Libraries
%description -n %{?nameprefix}ice-slice
This package contains Slice files used by the Ice framework.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}ice-utils-java
Summary:  IceGrid Admin graphical client.
Group: Applications/System
Obsoletes: ice-utils < 3.6
Requires: java
%description -n %{?nameprefix}ice-utils-java
The IceGrid service helps you locate, deploy and manage Ice servers.

The IceGrid GUI give you complete control over your deployed applications.
Activities such as starting a server or modifying a configuration setting
are just a mouse click away.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.
%endif

#
# Arch-dependent packages
#
%ifarch %{core_arches}

#
# This "meta" package includes all run-time components and services.
#
%package -n %{?nameprefix}ice-all-runtime
Summary: Ice run-time packages (meta package).
Group: System Environment/Libraries
%if %{cppx86}
Requires: %{?nameprefix}icebox%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}icestorm3.6%{?_isa} = %{version}-%{release}
%else
Requires: %{?nameprefix}glacier2%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icegrid%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icepatch2%{?_isa} = %{version}-%{release}
Requires: php-%{?nameprefix}ice%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}ice3.6-c++%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}freeze3.6-c++%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}ice-utils-java = %{version}-%{release}
Requires: %{?nameprefix}icebox%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}icestorm3.6%{?_isa} = %{version}-%{release}
%endif # cppx86
%description -n %{?nameprefix}ice-all-runtime
This is a meta package that depends on all run-time packages for Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# This "meta" package includes all development kits.
#
%package -n %{?nameprefix}ice-all-devel
Summary: Ice development packages (meta package)
Group: System Environment/Libraries
%if %{cppx86}
Requires: lib%{?nameprefix}ice-c++-devel%{?_isa} = %{version}-%{release}
%else
Requires: lib%{?nameprefix}ice-c++-devel%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}ice-java%{?_isa} = %{version}-%{release}
Requires: php-%{?nameprefix}ice-devel%{?_isa} = %{version}-%{release}
%if %{slice2cs}
Requires: %{?nameprefix}ice-slice2cs%{?_isa} = %{version}-%{release}
%endif # slice2cs
%endif # cppx86
%description -n %{?nameprefix}ice-all-devel
This is a meta package that depends on all development packages for Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n lib%{?nameprefix}ice3.6-c++
Summary: Ice for C++ run-time libraries.
Group: System Environment/Libraries
Requires: bzip2
%description -n lib%{?nameprefix}ice3.6-c++
This package contains the C++ run-time libraries for the Ice framework.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n lib%{?nameprefix}freeze3.6-c++
Summary: C++ run-time libraries for the Freeze persistence service.
Group: System Environment/Libraries
Requires: lib%{?nameprefix}ice3.6-c++%{?_isa} = %{version}-%{release}
%if "%{dist}" == ".el7"
Requires: libdb%{?_isa} >= %{dbversion}
%else
Requires: db53%{?_isa} >= %{dbversion}
%endif
%description -n lib%{?nameprefix}freeze3.6-c++
This package contains the C++ run-time libraries for the Freeze persistence
service.

The Freeze persistence service allows you to store Ice objects in Oracle
Berkeley DB, with all the features you expect from a robust database -
transactions, hot backups, indexing, and more.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}icebox
Summary: IceBox server, a framework for Ice application services.
Group: System Environment/Daemons
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
Obsoletes: ice-servers < 3.6
# Requirements for the users
Requires(pre): %{shadow}
%if %{systemd}
BuildRequires:    %{systemdpkg}
Requires(post):   %{systemdpkg}
Requires(preun):  %{systemdpkg}
Requires(postun): %{systemdpkg}
%else
# Requirements for the init.d services
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
%description -n %{?nameprefix}icebox
This package contains the IceBox server, an easy-to-use framework for
developing and deploying Ice application services.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if ! %{cppx86}

%package -n lib%{?nameprefix}ice-java
Summary: Ice for Java run-time libraries and development tools.
Group: System Environment/Libraries
Obsoletes: ice-java-devel < 3.6, ice-java < 3.6
%if "%{dist}" == ".el7"
Requires: libdb-java%{?_isa} >= %{dbversion}
%else
Requires: db53-java%{?_isa} >= %{dbversion}
%endif
%description -n lib%{?nameprefix}ice-java
This package contains Ice for Java run-time libraries and development tools.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}ice-utils
Summary: Ice utilities and admin tools.
Group: Applications/System
Obsoletes: ice-utils < 3.6
Requires: lib%{?nameprefix}freeze3.6-c++%{?_isa} = %{version}-%{release}
%description -n %{?nameprefix}ice-utils
This package contains Ice utilities and admin tools.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}icegrid
Summary: Locate, deploy, and manage Ice servers.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
Requires: lib%{?nameprefix}freeze3.6-c++%{?_isa} = %{version}-%{release}, %{?nameprefix}ice-utils = %{version}-%{release}
# Requirements for the users
Requires(pre): %{shadow}
%if %{systemd}
BuildRequires:    %{systemdpkg}
Requires(post):   %{systemdpkg}
Requires(preun):  %{systemdpkg}
Requires(postun): %{systemdpkg}
%else
# Requirements for the init.d services
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
%description -n %{?nameprefix}icegrid
This package contains the IceGrid service. IceGrid helps you locate,
deploy and manage Ice servers.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}glacier2
Summary: Glacier2 router.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
# Requirements for the users
Requires(pre): %{shadow}
%if %{systemd}
BuildRequires:    %{systemdpkg}
Requires(post):   %{systemdpkg}
Requires(preun):  %{systemdpkg}
Requires(postun): %{systemdpkg}
%else
# Requirements for the init.d services
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
%description -n %{?nameprefix}glacier2
This package contains the Glacier2 router. A Glacier2 router allows you to
securely route Ice communications across networks, such as the public Internet
and a private network behind a firewall. With Glacier2, you only need to open
one port in your firewall to make multiple back-end Ice servers reachable by
remote Ice clients on the Internet.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n %{?nameprefix}icepatch2
Summary: File distribution and patching.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
Requires: %{?nameprefix}ice-utils%{?_isa} = %{version}-%{release}
# Requirements for the users
Requires(pre): %{shadow}
%if %{systemd}
BuildRequires:    %{systemdpkg}
Requires(post):   %{systemdpkg}
Requires(preun):  %{systemdpkg}
Requires(postun): %{systemdpkg}
%else
# Requirements for the init.d services
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
%endif
%description -n %{?nameprefix}icepatch2
This package contains the IcePatch2 service. With IcePatch2, you can easily
distribute a large set of files to many clients and keep these files
synced with your source set.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if %{slice2cs}
%package -n %{?nameprefix}ice-slice2cs
Summary: Slice-to-C# compiler.
Group: Development/Tools
Obsoletes: ice-mono-devel < 3.6
Requires: lib%{?nameprefix}ice3.6-c++%{?_isa} = %{version}-%{release}
%description -n %{?nameprefix}ice-slice2cs
This package contains the Slice-to-C# compiler.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.
%endif # slice2cs

%endif # ! cppx86

%package -n lib%{?nameprefix}icestorm3.6
Summary: IceStorm publish-subscribe event distribution service.
Group: System Environment/Libraries
Requires: lib%{?nameprefix}freeze3.6-c++%{?_isa} = %{version}-%{release}
%description -n lib%{?nameprefix}icestorm3.6
This package contains the IceStorm publish-subscribe event distribution
service.

IceStorm helps you create push applications. Your Ice client (the publisher)
sends a request to a topic managed by IceStorm, and IceStorm delivers this
request to all the subscribers (Ice objects) that you registered with this
topic.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n lib%{?nameprefix}ice-c++-devel
Summary: Tools, libraries and headers for developing Ice applications in C++.
Group: Development/Tools
Obsoletes: ice-c++-devel < 3.6
Requires: lib%{?nameprefix}ice3.6-c++%{?_isa} = %{version}-%{release}, %{?nameprefix}ice-slice = %{version}-%{release}
%if %{cppx86}
Requires: lib%{?nameprefix}ice-c++-devel(x86-64) = %{version}-%{release}
%endif
%if 0%{?biarch}
Requires: glibc-devel%{?_isa}
%endif
%description -n lib%{?nameprefix}ice-c++-devel
This package contains the tools, libraries and headers for developing Ice
applications in C++.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if ! %{cppx86}

%package -n php-%{?nameprefix}ice
Summary: PHP extension for Ice.
Group: System Environment/Libraries
Obsoletes: ice-php < 3.6
Requires: lib%{?nameprefix}ice3.6-c++%{?_isa} = %{version}-%{release}
%if "%{dist}" == ".sles11"
Requires: php53%{?_isa}
%endif
%if "%{dist}" == ".sles12"
Requires: php5%{?_isa}
%endif
%if "%{dist}" == ".el6"
Requires: php-common%{?_isa}
%endif
%if "%{dist}" == ".el7"
Requires: php-common%{?_isa}
%endif
%if "%{dist}" == ".amzn1"
Requires: php-common%{?_isa} < 5.4
%endif
%description -n php-%{?nameprefix}ice
This package contains a PHP extension for communicating with Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%package -n php-%{?nameprefix}ice-devel
Summary: Tools for developing Ice applications in PHP.
Group: Development/Tools
Obsoletes: ice-php-devel < 3.6
Requires: php-%{?nameprefix}ice%{?_isa} = %{version}-%{release}, %{?nameprefix}ice-slice = %{version}-%{release}
%description -n php-%{?nameprefix}ice-devel
This package contains the tools for developing Ice applications in PHP.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%endif

%endif # ! cppx86

%prep

%if %{buildall}
%setup -n Ice-%{version} -q
%setup -n Ice-rpmbuild-%{version} -T -b 1
%endif

%build

%ifarch %{core_arches}

%if %{cpp11}
cd $RPM_BUILD_DIR/Ice-%{version}
mkdir tmp
tar cf - cpp | (cd tmp; tar xf -)
mv tmp/cpp cpp11
rmdir tmp
%endif

cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src
%if %{cppx86}
make %{?_smp_mflags} CXXARCHFLAGS="-m32" LP64=no OPTIMIZE=yes %{runpath}
%else
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}
%endif

%if %{cpp11}
cd $RPM_BUILD_DIR/Ice-%{version}
mv cpp cpp.sav
mv cpp11 cpp
cd cpp/src
%if %{cppx86}
make %{?_smp_mflags} CXXARCHFLAGS="-m32" LP64=no CPP11=yes OPTIMIZE=yes %{runpath}
%else
make %{?_smp_mflags} CPP11=yes OPTIMIZE=yes %{runpath}
%endif
cd $RPM_BUILD_DIR/Ice-%{version}
mv cpp cpp11
mv cpp.sav cpp
%endif

%if ! %{cppx86}

cd $RPM_BUILD_DIR/Ice-%{version}/php
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}

cd $RPM_BUILD_DIR/Ice-%{version}/java
make dist

%endif # ! cppx86

%else

#
# Build only what we need in C++.
#
cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src/IceUtil
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}

cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src/Slice
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}

cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src/slice2java
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}

cd $RPM_BUILD_DIR/Ice-%{version}/cpp/src/slice2freezej
make %{?_smp_mflags} OPTIMIZE=yes %{runpath}

cd $RPM_BUILD_DIR/Ice-%{version}/java
make dist

%endif


%install

rm -rf $RPM_BUILD_ROOT

#
# Arch-specific packages
#
%ifarch %{core_arches}

#
# C++
#
mkdir -p $RPM_BUILD_ROOT/lib

%if %{cppx86}

cd $RPM_BUILD_DIR/Ice-%{version}/cpp
make prefix=$RPM_BUILD_ROOT LP64=no install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/bin/icebox32 $RPM_BUILD_ROOT%{_bindir}
rm $RPM_BUILD_ROOT/bin/*

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%_lib/* $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT/include/*

%else

cd $RPM_BUILD_DIR/Ice-%{version}/cpp
make prefix=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_bindir}
%ifarch %{ix86}
mv $RPM_BUILD_ROOT/bin/icebox32 $RPM_BUILD_ROOT%{_bindir}
%endif
mv $RPM_BUILD_ROOT/bin/* $RPM_BUILD_ROOT%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/%_lib/* $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/include/* $RPM_BUILD_ROOT%{_includedir}

%endif # cppx86

%if %{cpp11}
cd $RPM_BUILD_DIR/Ice-%{version}
mv cpp cpp.sav
mv cpp11 cpp
cd cpp/src
mkdir -p $RPM_BUILD_ROOT/%_lib/c++11
%if %{cppx86}
make CPP11=yes prefix=$RPM_BUILD_ROOT LP64=no install
%else
make CPP11=yes prefix=$RPM_BUILD_ROOT install
%endif
cd $RPM_BUILD_DIR/Ice-%{version}
mv cpp cpp11
mv cpp.sav cpp

rm -f $RPM_BUILD_ROOT/%_lib/libGlacier2CryptPermissionsVerifier++11.so*
rm -f $RPM_BUILD_ROOT/%_lib/libSlice++11.so*
rm -f $RPM_BUILD_ROOT/%_lib/libIceXML++11.so*
rm -f $RPM_BUILD_ROOT/%_lib/c++11/libGlacier2CryptPermissionsVerifier.so
rm -f $RPM_BUILD_ROOT/%_lib/c++11/libSlice.so
rm -f $RPM_BUILD_ROOT/%_lib/c++11/libIceStormService.so
rm -f $RPM_BUILD_ROOT/%_lib/c++11/libIceXML.so
mv $RPM_BUILD_ROOT/%_lib/* $RPM_BUILD_ROOT%{_libdir}
%if %{cppx86}
mv $RPM_BUILD_ROOT/bin/icebox32++11 $RPM_BUILD_ROOT%{_bindir}
%else
%ifarch %{ix86}
mv $RPM_BUILD_ROOT/bin/icebox++11 $RPM_BUILD_ROOT%{_bindir}/icebox32++11
%else
mv $RPM_BUILD_ROOT/bin/icebox++11 $RPM_BUILD_ROOT%{_bindir}
%endif
%endif
rm -f $RPM_BUILD_ROOT/bin/*
rm -rf $RPM_BUILD_ROOT/include/*
%endif

%if %{cppx86}

#
# Doc & license files
#

for i in %{?nameprefix}ice-all-runtime %{?nameprefix}icebox %{?nameprefix}ice-all-devel lib%{?nameprefix}freeze3.6-c++ lib%{?nameprefix}ice3.6-c++ lib%{?nameprefix}ice-c++-devel lib%{?nameprefix}icestorm3.6
do
  mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/README.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}/README
  cp -p $RPM_BUILD_DIR/Ice-%{version}/ICE_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-%{version}/LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
done

%else

#
# PHP
#
cd $RPM_BUILD_DIR/Ice-%{version}/php
make prefix=$RPM_BUILD_ROOT install

%if "%{dist}" == ".el6"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php/modules
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php/modules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{_datadir}/php
%endif

%if "%{dist}" == ".el7"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php/modules
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php/modules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{_datadir}/php
%endif

%if "%{dist}" == ".amzn1"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php/modules
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php/modules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{_datadir}/php
%endif

%if "%{dist}" == ".sles11"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php5/extensions
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php5/extensions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php5
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{_datadir}/php5
%endif

%if "%{dist}" == ".sles12"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/php5/extensions
mv $RPM_BUILD_ROOT/php/IcePHP.so $RPM_BUILD_ROOT%{_libdir}/php5/extensions
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php5
mv $RPM_BUILD_ROOT/php/* $RPM_BUILD_ROOT%{_datadir}/php5
%endif

#
# Java install (using jpackage conventions)
#
cd $RPM_BUILD_DIR/Ice-%{version}/java
make prefix=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_javadir}

for i in freeze glacier2 ice icebox icediscovery icelocatordiscovery icegrid icepatch2 icestorm
do
  mv $RPM_BUILD_ROOT/lib/$i-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
  ln -s $i-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$i.jar
  mv $RPM_BUILD_ROOT/lib/$i-%{version}-sources.jar $RPM_BUILD_ROOT%{_javadir}
  ln -s $i-%{version}-sources.jar $RPM_BUILD_ROOT%{_javadir}/$i-sources.jar
done

#
# initrd files (for servers)
#
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}

for i in icegridregistry icegridnode glacier2router
do
%if %{systemd}
  install -p -D $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/$i.service $RPM_BUILD_ROOT%{_unitdir}/$i.service
%else
  install -p -D $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/$i.%{_vendor} $RPM_BUILD_ROOT%{_initrddir}/$i
%endif
done

#
# Some python scripts and related files
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
mv $RPM_BUILD_ROOT/config/* $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}

#
# Man pages
#
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
# TODO: We should really do this:
#mv -f $RPM_BUILD_ROOT/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
rm -r $RPM_BUILD_ROOT/man
cp -p $RPM_BUILD_DIR/Ice-%{version}/man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

rm -f $RPM_BUILD_ROOT%{_bindir}/slice2py
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2py.1

rm -f $RPM_BUILD_ROOT%{_bindir}/slice2rb
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2rb.1

rm -f $RPM_BUILD_ROOT%{_bindir}/slice2js
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2js.1

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2objc.1

#
# Doc & license files
#

PACKAGES="%{?nameprefix}glacier2 %{?nameprefix}ice-all-runtime %{?nameprefix}icebox %{?nameprefix}ice-all-devel %{?nameprefix}icegrid %{?nameprefix}icepatch2 %{?nameprefix}ice-utils lib%{?nameprefix}freeze3.6-c++ lib%{?nameprefix}ice3.6-c++ lib%{?nameprefix}ice-c++-devel lib%{?nameprefix}ice-java lib%{?nameprefix}icestorm3.6 php-%{?nameprefix}ice php-%{?nameprefix}ice-devel"

%if %{slice2cs}
PACKAGES="$PACKAGES %{?nameprefix}ice-slice2cs"
%endif

for i in $PACKAGES
do
  mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/README.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}/README
  cp -p $RPM_BUILD_DIR/Ice-%{version}/ICE_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-%{version}/LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
done

cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/MCPP_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/lib%{?nameprefix}ice3.6-c++-%{version}

%endif # ! cppx86

#
# Cleanup extra files
#
rm -f $RPM_BUILD_ROOT/bin/*
rm -f $RPM_BUILD_ROOT/ICE_LICENSE
rm -f $RPM_BUILD_ROOT/LICENSE
rm -fr $RPM_BUILD_ROOT/doc/reference
rm -fr $RPM_BUILD_ROOT/slice
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceStormService.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libGlacier2CryptPermissionsVerifier.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceXML.so
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/iceboxnet.1
%if !%{slice2cs}
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2cs
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2cs.1
%endif # ! slice2cs

%if %{cppx86}

#
# These directories and files aren't needed in the x86 build.
#
rm -rf $RPM_BUILD_ROOT/config
rm -rf $RPM_BUILD_ROOT/man
rm -f $RPM_BUILD_ROOT%{_libdir}/libGlacier2CryptPermissionsVerifier.so*
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceXML.so*
rm -f $RPM_BUILD_ROOT%{_libdir}/libSlice.so*

%else # cppx86

rm -f $RPM_BUILD_ROOT/lib/icegridgui.jar
rm -f $RPM_BUILD_ROOT/lib/*.pom
#rm -rf $RPM_BUILD_ROOT/node_modules

%endif # cppx86

%endif

#
# Arch-independent packages
#
%ifarch noarch

cd $RPM_BUILD_DIR/Ice-%{version}/java

#
# Doc & license files
#
for i in ice-utils-java ice-slice
do
  mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/README.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}$i-%{version}/README
  cp -p $RPM_BUILD_DIR/Ice-%{version}/ICE_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}$i-%{version}
  cp -p $RPM_BUILD_DIR/Ice-%{version}/LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}$i-%{version}
done

cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/JGOODIES_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}ice-utils-java-%{version}

#
# IceGridGUI
#
# We do not keep the version in the file name for icegridgui.jar in the RPM distribution.
#
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p $RPM_BUILD_DIR/Ice-%{version}/java/lib/icegridgui.jar $RPM_BUILD_ROOT%{_javadir}/icegridgui.jar
cp -p $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/icegridgui $RPM_BUILD_ROOT%{_bindir}/icegridgui
if [ -n "$JARSIGNER_KEYSTORE" ]; then
  jarsigner -keystore $JARSIGNER_KEYSTORE -storepass "$JARSIGNER_KEYSTORE_PASSWORD" $RPM_BUILD_ROOT%{_javadir}/icegridgui.jar $JARSIGNER_KEYSTORE_ALIAS -tsa http://timestamp.digicert.com
fi

#
# Slice files
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
cp -rp $RPM_BUILD_DIR/Ice-%{version}/slice $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}
ln -s %{_datadir}/Ice-%{version}/slice $RPM_BUILD_ROOT%{_datadir}/slice
%endif

%clean
rm -rf $RPM_BUILD_ROOT

#
# noarch file packages
#
%ifarch noarch

%files -n %{?nameprefix}ice-slice
%defattr(-, root, root, -)
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/slice
%{_datadir}/slice
%{_defaultdocdir}/%{?nameprefix}ice-slice-%{version}

%files -n %{?nameprefix}ice-utils-java
%defattr(-, root, root, -)
%attr(755,root,root) %{_bindir}/icegridgui
%{_javadir}/icegridgui.jar
%{_defaultdocdir}/%{?nameprefix}ice-utils-java-%{version}

%endif

#
# arch-specific packages
#
%ifarch %{core_arches}

#
# Empty list for main "ice" package
#
%files

#
# Generate "ice-all-runtime" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-runtime
%defattr(-, root, root, -)
%{_defaultdocdir}/%{?nameprefix}ice-all-runtime-%{version}

#
# Generate "ice-all-devel" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-devel
%defattr(-, root, root, -)
%{_defaultdocdir}/%{?nameprefix}ice-all-devel-%{version}

%files -n lib%{?nameprefix}ice3.6-c++
%defattr(-, root, root, -)
%{_libdir}/libGlacier2.so.%{version}
%{_libdir}/libGlacier2.so.%{soversion}
%{_libdir}/libIce.so.%{version}
%{_libdir}/libIce.so.%{soversion}
%{_libdir}/libIceBox.so.%{version}
%{_libdir}/libIceBox.so.%{soversion}
%{_libdir}/libIceDiscovery.so.%{version}
%{_libdir}/libIceDiscovery.so.%{soversion}
%{_libdir}/libIceGrid.so.%{version}
%{_libdir}/libIceGrid.so.%{soversion}
%{_libdir}/libIceLocatorDiscovery.so.%{version}
%{_libdir}/libIceLocatorDiscovery.so.%{soversion}
%{_libdir}/libIcePatch2.so.%{version}
%{_libdir}/libIcePatch2.so.%{soversion}
%{_libdir}/libIceSSL.so.%{version}
%{_libdir}/libIceSSL.so.%{soversion}
%{_libdir}/libIceStorm.so.%{version}
%{_libdir}/libIceStorm.so.%{soversion}
%{_libdir}/libIceUtil.so.%{version}
%{_libdir}/libIceUtil.so.%{soversion}
%if ! %{cppx86}
%{_libdir}/libGlacier2CryptPermissionsVerifier.so.%{version}
%{_libdir}/libGlacier2CryptPermissionsVerifier.so.%{soversion}
%{_libdir}/libSlice.so.%{version}
%{_libdir}/libSlice.so.%{soversion}
%endif

%if %{cpp11}
%{_libdir}/libGlacier2++11.so.%{version}
%{_libdir}/libGlacier2++11.so.%{soversion}
%{_libdir}/libIce++11.so.%{version}
%{_libdir}/libIce++11.so.%{soversion}
%{_libdir}/libIceBox++11.so.%{version}
%{_libdir}/libIceBox++11.so.%{soversion}
%{_libdir}/libIceDiscovery++11.so.%{version}
%{_libdir}/libIceDiscovery++11.so.%{soversion}
%{_libdir}/libIceGrid++11.so.%{version}
%{_libdir}/libIceGrid++11.so.%{soversion}
%{_libdir}/libIceLocatorDiscovery++11.so.%{version}
%{_libdir}/libIceLocatorDiscovery++11.so.%{soversion}
%{_libdir}/libIcePatch2++11.so.%{version}
%{_libdir}/libIcePatch2++11.so.%{soversion}
%{_libdir}/libIceSSL++11.so.%{version}
%{_libdir}/libIceSSL++11.so.%{soversion}
%{_libdir}/libIceStorm++11.so.%{version}
%{_libdir}/libIceStorm++11.so.%{soversion}
%{_libdir}/libIceUtil++11.so.%{version}
%{_libdir}/libIceUtil++11.so.%{soversion}
%endif
%{_defaultdocdir}/lib%{?nameprefix}ice3.6-c++-%{version}

%post -n lib%{?nameprefix}ice3.6-c++ -p /sbin/ldconfig
%postun -n lib%{?nameprefix}ice3.6-c++ -p /sbin/ldconfig

%files -n lib%{?nameprefix}freeze3.6-c++
%defattr(-, root, root, -)
%{_libdir}/libFreeze.so.%{version}
%{_libdir}/libFreeze.so.%{soversion}
%if ! %{cppx86}
%{_libdir}/libIceXML.so.%{version}
%{_libdir}/libIceXML.so.%{soversion}
%endif
%if %{cpp11}
%{_libdir}/libFreeze++11.so.%{version}
%{_libdir}/libFreeze++11.so.%{soversion}
%endif
%{_defaultdocdir}/lib%{?nameprefix}freeze3.6-c++-%{version}

%post -n lib%{?nameprefix}freeze3.6-c++ -p /sbin/ldconfig
%postun -n lib%{?nameprefix}freeze3.6-c++ -p /sbin/ldconfig

%files -n lib%{?nameprefix}icestorm3.6
%defattr(-, root, root, -)
%{_libdir}/libIceStormService.so.%{version}
%{_libdir}/libIceStormService.so.%{soversion}
%if %{cpp11}
%{_libdir}/libIceStormService++11.so.%{version}
%{_libdir}/libIceStormService++11.so.%{soversion}
%endif
%{_defaultdocdir}/lib%{?nameprefix}icestorm3.6-%{version}

%post -n lib%{?nameprefix}icestorm3.6 -p /sbin/ldconfig
%postun -n lib%{?nameprefix}icestorm3.6 -p /sbin/ldconfig

%if ! %{cppx86}

%files -n lib%{?nameprefix}ice-java
%defattr(-, root, root, -)
%{_bindir}/slice2java
%{_mandir}/man1/slice2java.1*
%{_bindir}/slice2freezej
%{_mandir}/man1/slice2freezej.1*
%{_javadir}/ice-%{version}.jar
%{_javadir}/ice.jar
%{_javadir}/ice-%{version}-sources.jar
%{_javadir}/ice-sources.jar
%{_javadir}/glacier2-%{version}.jar
%{_javadir}/glacier2.jar
%{_javadir}/glacier2-%{version}-sources.jar
%{_javadir}/glacier2-sources.jar
%{_javadir}/icebox-%{version}.jar
%{_javadir}/icebox.jar
%{_javadir}/icebox-%{version}-sources.jar
%{_javadir}/icebox-sources.jar
%{_javadir}/icegrid-%{version}.jar
%{_javadir}/icegrid.jar
%{_javadir}/icegrid-%{version}-sources.jar
%{_javadir}/icegrid-sources.jar
%{_javadir}/icepatch2-%{version}.jar
%{_javadir}/icepatch2.jar
%{_javadir}/icepatch2-%{version}-sources.jar
%{_javadir}/icepatch2-sources.jar
%{_javadir}/icestorm-%{version}.jar
%{_javadir}/icestorm.jar
%{_javadir}/icestorm-%{version}-sources.jar
%{_javadir}/icestorm-sources.jar
%{_javadir}/icediscovery-%{version}.jar
%{_javadir}/icediscovery.jar
%{_javadir}/icediscovery-%{version}-sources.jar
%{_javadir}/icediscovery-sources.jar
%{_javadir}/icelocatordiscovery-%{version}.jar
%{_javadir}/icelocatordiscovery.jar
%{_javadir}/icelocatordiscovery-%{version}-sources.jar
%{_javadir}/icelocatordiscovery-sources.jar
%{_javadir}/freeze-%{version}.jar
%{_javadir}/freeze.jar
%{_javadir}/freeze-%{version}-sources.jar
%{_javadir}/freeze-sources.jar
%{_defaultdocdir}/lib%{?nameprefix}ice-java-%{version}

%files -n %{?nameprefix}ice-utils
%defattr(-, root, root, -)
%{_bindir}/dumpdb
%{_mandir}/man1/dumpdb.1*
%{_bindir}/transformdb
%{_mandir}/man1/transformdb.1*
%{_bindir}/iceboxadmin
%{_mandir}/man1/iceboxadmin.1*
%{_bindir}/icepatch2calc
%{_mandir}/man1/icepatch2calc.1*
%{_bindir}/icepatch2client
%{_mandir}/man1/icepatch2client.1*
%{_bindir}/icestormadmin
%{_mandir}/man1/icestormadmin.1*
%{_bindir}/icestormmigrate
%{_mandir}/man1/icestormmigrate.1*
%{_bindir}/icestormdb
%{_mandir}/man1/icestormdb.1*
%{_bindir}/slice2html
%{_mandir}/man1/slice2html.1*
%{_bindir}/icegridadmin
%{_mandir}/man1/icegridadmin.1*
%{_bindir}/icegriddb
%{_mandir}/man1/icegriddb.1*
%{_defaultdocdir}/%{?nameprefix}ice-utils-%{version}

%post -n %{?nameprefix}ice-utils -p /sbin/ldconfig
%postun -n %{?nameprefix}ice-utils -p /sbin/ldconfig

%files -n %{?nameprefix}icegrid
%defattr(-, root, root, -)
%{_bindir}/icegridnode
%{_mandir}/man1/icegridnode.1*
%{_bindir}/icegridregistry
%{_mandir}/man1/icegridregistry.1*
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/templates.xml
%attr(755,root,root) %{_datadir}/Ice-%{version}/upgradeicegrid36.py*
%{_datadir}/Ice-%{version}/icegrid-slice.3.5.ice.gz
%{_datadir}/Ice-%{version}/icegrid-slice.3.6.ice.gz
%if %{systemd}
%attr(755,root,root) %{_unitdir}/icegridregistry.service
%attr(755,root,root) %{_unitdir}/icegridnode.service
%else
%attr(755,root,root) %{_initrddir}/icegridregistry
%attr(755,root,root) %{_initrddir}/icegridnode
%endif
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf
%{_defaultdocdir}/%{?nameprefix}icegrid-%{version}

%pre -n %{?nameprefix}icegrid
%if "%{_prefix}" == "/usr"
getent group ice > /dev/null || groupadd -r ice
getent passwd ice > /dev/null || \
  useradd -r -g ice -d %{_localstatedir}/lib/ice -s /sbin/nologin -c "Ice Service account" ice
test -d %{_localstatedir}/lib/ice/icegrid/registry || \
  mkdir -p %{_localstatedir}/lib/ice/icegrid/registry; chown -R ice.ice %{_localstatedir}/lib/ice
test -d %{_localstatedir}/lib/ice/icegrid/node1 || \
  mkdir -p %{_localstatedir}/lib/ice/icegrid/node1; chown -R ice.ice %{_localstatedir}/lib/ice
exit 0
%endif

%post -n %{?nameprefix}icegrid
/sbin/ldconfig
%if "%{_prefix}" == "/usr"
  %if %{systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1  || :
  %else
    %if "%{dist}" != ".sles11"
      /sbin/chkconfig --add icegridregistry
      /sbin/chkconfig --add icegridnode
    %endif
  %endif
%endif

%preun -n %{?nameprefix}icegrid
%if "%{_prefix}" == "/usr"
  if [ $1 = 0 ]; then
  %if %{systemd}
    /bin/systemctl --no-reload disable icegridnode.service >/dev/null 2>&1 || :
    /bin/systemctl stop icegridnode.service >/dev/null 2>&1 || :

    /bin/systemctl --no-reload disable icegridregistry.service >/dev/null 2>&1 || :
    /bin/systemctl stop icegridregistry.service >/dev/null 2>&1 || :
  %else
    %if "%{dist}" == ".sles11"
      /sbin/service icegridnode stop >/dev/null 2>&1 || :
      /sbin/insserv -r icegridnode
      /sbin/service icegridregistry stop >/dev/null 2>&1 || :
      /sbin/insserv -r icegridregistry
    %else
      /sbin/service icegridnode stop >/dev/null 2>&1 || :
      /sbin/chkconfig --del icegridnode
      /sbin/service icegridregistry stop >/dev/null 2>&1 || :
      /sbin/chkconfig --del icegridregistry
    %endif
  %endif
  fi
%endif

%postun -n %{?nameprefix}icegrid
%if "%{_prefix}" == "/usr"
  %if %{systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    if [ "$1" -ge "1" ]; then
      /bin/systemctl try-restart icegridnode.service >/dev/null 2>&1 || :
      /bin/systemctl try-restart icegridregistry.service >/dev/null 2>&1 || :
    fi
  %else
    if [ "$1" -ge "1" ]; then
      /sbin/service icegridnode condrestart >/dev/null 2>&1 || :
    	/sbin/service icegridregistry condrestart >/dev/null 2>&1 || :
    fi
  %endif
%endif
/sbin/ldconfig

%files -n %{?nameprefix}glacier2
%defattr(-, root, root, -)
%{_bindir}/glacier2router
%{_mandir}/man1/glacier2router.1*
%if %{systemd}
  %attr(755,root,root) %{_unitdir}/glacier2router.service
%else
  %attr(755,root,root) %{_initrddir}/glacier2router
%endif
%config(noreplace) %{_sysconfdir}/glacier2router.conf
%{_defaultdocdir}/%{?nameprefix}glacier2-%{version}

%pre -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  getent group ice > /dev/null || groupadd -r ice
  getent passwd ice > /dev/null || \
         useradd -r -g ice -d %{_localstatedir}/lib/ice \
         -s /sbin/nologin -c "Ice Service account" ice
  exit 0
%endif

%post -n %{?nameprefix}glacier2
/sbin/ldconfig
%if "%{_prefix}" == "/usr"
  %if %{systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1  || :
  %else
    %if "%{dist}" != ".sles11"
      /sbin/chkconfig --add glacier2router
    %endif
  %endif
%endif

%preun -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  if [ $1 = 0 ]; then
  %if %{systemd}
    /bin/systemctl --no-reload disable glacier2router.service >/dev/null 2>&1 || :
    /bin/systemctl stop glacier2router.service >/dev/null 2>&1 || :
  %else
    %if "%{dist}" == ".sles11"
      /sbin/service glacier2router stop >/dev/null 2>&1 || :
      /sbin/insserv -r glacier2router
    %else
      /sbin/service glacier2router stop >/dev/null 2>&1 || :
      /sbin/chkconfig --del glacier2router
    %endif
  %endif
  fi
%endif

%postun -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  %if %{systemd}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
    if [ "$1" -ge "1" ]; then
      /bin/systemctl try-restart glacier2router.service >/dev/null 2>&1 || :
    fi
  %else
    if [ "$1" -ge "1" ]; then
      /sbin/service glacier2router condrestart >/dev/null 2>&1 || :
    fi
  %endif
%endif
/sbin/ldconfig

%files -n %{?nameprefix}icepatch2
%defattr(-, root, root, -)
%{_bindir}/icepatch2server
%{_mandir}/man1/icepatch2server.1*
%{_defaultdocdir}/%{?nameprefix}icepatch2-%{version}

%post -n %{?nameprefix}icepatch2 -p /sbin/ldconfig
%postun -n %{?nameprefix}icepatch2 -p /sbin/ldconfig

%if %{slice2cs}
%files -n %{?nameprefix}ice-slice2cs
%defattr(-, root, root, -)
%{_bindir}/slice2cs
%{_mandir}/man1/slice2cs.1*
%{_defaultdocdir}/%{?nameprefix}ice-slice2cs-%{version}

%post -n %{?nameprefix}ice-slice2cs -p /sbin/ldconfig
%postun -n %{?nameprefix}ice-slice2cs -p /sbin/ldconfig
%endif # slice2cs

%endif # ! cppx86

%files -n %{?nameprefix}icebox
%defattr(-, root, root, -)
%if %{cppx86}
%{_bindir}/icebox32
%else
%ifarch %{ix86}
%{_bindir}/icebox32
%else
%{_bindir}/icebox
%endif
%{_mandir}/man1/icebox.1*
%endif
%if %{cpp11}
%if %{cppx86}
%{_bindir}/icebox32++11
%else
%ifarch %{ix86}
%{_bindir}/icebox32++11
%else
%{_bindir}/icebox++11
%endif
%endif
%endif
%{_defaultdocdir}/%{?nameprefix}icebox-%{version}

%post -n %{?nameprefix}icebox -p /sbin/ldconfig
%postun -n %{?nameprefix}icebox -p /sbin/ldconfig

%files -n lib%{?nameprefix}ice-c++-devel
%defattr(-, root, root, -)

%if ! %{cppx86}
%{_bindir}/slice2cpp
%{_mandir}/man1/slice2cpp.1*
%{_bindir}/slice2freeze
%{_mandir}/man1/slice2freeze.1*
%{_includedir}/Freeze
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_includedir}/Slice
%endif
%{_libdir}/libFreeze.so
%{_libdir}/libGlacier2.so
%{_libdir}/libIce.so
%{_libdir}/libIceBox.so
%{_libdir}/libIceDiscovery.so
%{_libdir}/libIceGrid.so
%{_libdir}/libIceLocatorDiscovery.so
%{_libdir}/libIcePatch2.so
%{_libdir}/libIceSSL.so
%{_libdir}/libIceStorm.so
%{_libdir}/libIceUtil.so
%if ! %{cppx86}
%{_libdir}/libSlice.so
%endif
%if %{cpp11}
%{_libdir}/c++11/libFreeze.so
%{_libdir}/c++11/libGlacier2.so
%{_libdir}/c++11/libIce.so
%{_libdir}/c++11/libIceBox.so
%{_libdir}/c++11/libIceDiscovery.so
%{_libdir}/c++11/libIceGrid.so
%{_libdir}/c++11/libIceLocatorDiscovery.so
%{_libdir}/c++11/libIcePatch2.so
%{_libdir}/c++11/libIceSSL.so
%{_libdir}/c++11/libIceStorm.so
%{_libdir}/c++11/libIceUtil.so
%endif
%{_defaultdocdir}/lib%{?nameprefix}ice-c++-devel-%{version}

%if ! %{cppx86}

%files -n php-%{?nameprefix}ice
%defattr(-, root, root, -)

%if "%{dist}" == ".el6"
%{_datadir}/php
%{_libdir}/php/modules/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif

%if "%{dist}" == ".el7"
%{_datadir}/php
%{_libdir}/php/modules/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif

%if "%{dist}" == ".amzn1"
%{_datadir}/php
%{_libdir}/php/modules/IcePHP.so
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif

%if "%{dist}" == ".sles11"
%{_datadir}/php5
%{_libdir}/php5/extensions
%config(noreplace) %{_sysconfdir}/php5/conf.d/ice.ini
%endif

%if "%{dist}" == ".sles12"
%{_datadir}/php5
%{_libdir}/php5/extensions
%config(noreplace) %{_sysconfdir}/php5/conf.d/ice.ini
%endif

%{_defaultdocdir}/php-%{?nameprefix}ice-%{version}

%files -n php-%{?nameprefix}ice-devel
%defattr(-, root, root, -)
%{_bindir}/slice2php
%{_mandir}/man1/slice2php.1*
%{_defaultdocdir}/php-%{?nameprefix}ice-devel-%{version}
%endif

%endif # ! cppx86

%changelog

* Thu Apr 14 2016 Mark Spruiell <mes@zeroc.com> 3.6.3
- x86-32 dependencies should only be required when building x86 packages on
  a bi-arch platform.

* Mon Feb 29 2016 Benoit Foucher <benoit@zeroc.com> 3.6.2
- Made the signing of the IceGridGUI jar file optional if JARSIGNER_KEYSTORE
  is not set.
- Added ice_license macro to allow customizing the licence.
- Added nameprefix macro to allow adding a prefix to the rpm package name.

* Fri Oct 31 2014 Mark Spruiell <mes@zeroc.com> 3.6b
- Updates for the Ice 3.6b release.

* Thu Jul 18 2013 Mark Spruiell <mes@zeroc.com> 3.5.1
- Adding man pages.

* Thu Feb 7 2013 Mark Spruiell <mes@zeroc.com> 3.5.0
- Updates for the Ice 3.5.0 release.

* Mon Nov 19 2012 Mark Spruiell <mes@zeroc.com> 3.5b
- Updates for the Ice 3.5b release.

* Tue Dec 15 2009 Mark Spruiell <mes@zeroc.com> 3.4b
- Updates for the Ice 3.4b release.

* Wed Mar 4 2009 Bernard Normier <bernard@zeroc.com> 3.3.1
- Minor updates for the Ice 3.3.1 release.

* Wed Feb 27 2008 Bernard Normier <bernard@zeroc.com> 3.3b-1
- Updates for Ice 3.3b release:
 - Split main ice rpm into ice noarch (license and Slice files), ice-libs
   (C++ runtime libraries), ice-utils (admin tools & utilities), ice-servers
   (icegridregistry, icebox etc.). This way, ice-libs 3.3.0 can coexist with
    ice-libs 3.4.0. The same is true for ice-mono, and to a lesser extent
    other ice runtime packages
- Many updates derived from Mary Ellen Foster (<mefoster at gmail.com>)'s
  Fedora RPM spec for Ice.
 - The Ice jar files are now installed in %{_javalibdir}, with
   jpackage-compliant names
 - New icegridgui shell script to launch the IceGrid GUI
 - The .NET files are now packaged using gacutil with the -root option.
 - ice-servers creates a new user (ice) and installs three init.d services:
   icegridregistry, icegridnode and glacier2router.
 - Python, Ruby and PHP files are now installed in the correct directories.

* Fri Jul 27 2007 Bernard Normier <bernard@zeroc.com> 3.2.1-1
- Updated for Ice 3.2.1 release

* Wed Jun 13 2007 Bernard Normier <bernard@zeroc.com>
- Added patch with new IceGrid.Node.AllowRunningServersAsRoot property.

* Wed Dec 6 2006 ZeroC Staff <support@zeroc.com>
- See source distributions or the ZeroC website for more information
  about the changes in this release
