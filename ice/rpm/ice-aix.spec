#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

#
# git_tag, when defined, is typically a branch, for example master
#
%if 0%{?git_tag:1}
   %define archive_tag %{git_tag}
   %define archive_dir_suffix %{git_tag}
%else
   # git_tag_version is the git tag vX.Y.Z[...] less the v prefix
   # if not defined, we default to the version provided below
   %{!?git_tag_version:%define git_tag_version 3.7.10}
   %define archive_tag v%{git_tag_version}
   %define archive_dir_suffix %{git_tag_version}
%endif

# By default, build with xlC_r (C++98 only, no Python)
%{!?cppcompiler:%global cppcompiler xlC_r}

%define _libdir32 %{_prefix}/lib32

%define rpmbuildfiles ice-packaging-%{archive_dir_suffix}/ice/rpm

%define pythonname python3
%define pythondir /opt/freeware/lib/python3.7/site-packages

%if "%{_prefix}" == "%{_usr}" && "%{cppcompiler}" == "g++"
   %define runpath embedded_runpath=no
%else
   %define runpath embedded_runpath_prefix=%{_prefix}
%endif

%if "%{cppcompiler}" == "xlC_r"
   %define configs shared
%else
   %define configs shared cpp11-shared
%endif

%define makebuildopts COMPILER=%{cppcompiler} CONFIGS="%{configs}" OPTIMIZE=yes V=1 %{runpath} -j10
%define makeinstallopts COMPILER=%{cppcompiler} CONFIGS="%{configs}" OPTIMIZE=yes V=1 %{runpath} DESTDIR=%{buildroot} prefix=%{_prefix} install_bindir=%{_bindir} install_libdir=%{_libdir} install_slicedir=%{_datadir}/ice/slice install_includedir=%{_includedir} install_mandir=%{_mandir} install_configdir=%{_datadir}/ice

Name: %{?nameprefix}ice
Version: 3.7.10
Summary: Comprehensive RPC framework with support for C++, Java, JavaScript, Python and more.
Release: 1%{?dist}
%if "%{?ice_license}"
License: %{ice_license}
%else
License: GPLv2 with exceptions
%endif
Vendor: ZeroC, Inc.
URL: https://zeroc.com/
Source0: https://github.com/zeroc-ice/ice/archive/%{archive_tag}/%{name}-%{version}.tar.gz
Source1: https://github.com/zeroc-ice/ice-packaging/archive/%{archive_tag}/%{name}-packaging-%{version}.tar.gz

BuildRequires: bzip2-devel, expat-static-devel, lmdb-devel, mcpp-devel, coreutils

%description
Not used

#
# ice-slice package
#
%package -n %{?nameprefix}ice-slice
Summary: Slice files for Ice.
Group: System Environment/Libraries
BuildArch: noarch
%description -n %{?nameprefix}ice-slice
This package contains Slice files used by the Ice framework.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# This "meta" package includes all run-time components and services.
#
%package -n %{?nameprefix}ice-all-runtime
Summary: Ice run-time packages (meta package).
Group: System Environment/Libraries
Requires: %{?nameprefix}icebox = %{version}-%{release}
Requires: lib%{?nameprefix}icestorm3.7 = %{version}-%{release}
Requires: %{?nameprefix}glacier2 = %{version}-%{release}
Requires: %{?nameprefix}icegrid = %{version}-%{release}
Requires: %{?nameprefix}icepatch2 = %{version}-%{release}
Requires: %{?nameprefix}icebridge = %{version}-%{release}
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
%if "%{cppcompiler}" == "g++"
Requires: %{pythonname}-%{?nameprefix}ice = %{version}-%{release}
%endif
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
Summary: Ice development packages (meta package).
Group: Development/Tools
Requires: lib%{?nameprefix}ice-c++-devel = %{version}-%{release}
%description -n %{?nameprefix}ice-all-devel
This is a meta package that depends on all development packages for Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# libiceMm-c++ package
#
%package -n lib%{?nameprefix}ice3.7-c++
Summary: Ice for C++ run-time libraries.
Group: System Environment/Libraries
%description -n lib%{?nameprefix}ice3.7-c++
This package contains the C++ run-time libraries for the Ice framework.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# icebox package
#
%package -n %{?nameprefix}icebox
Summary: IceBox server, a framework for Ice application services.
Group: System Environment/Daemons
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
Obsoletes: ice-servers < 3.6
%description -n %{?nameprefix}icebox
This package contains the IceBox server, an easy-to-use framework for
developing and deploying Ice application services.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# libicestormMm package
#
%package -n lib%{?nameprefix}icestorm3.7
Summary: IceStorm publish-subscribe event distribution service.
Group: System Environment/Libraries
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
%description -n lib%{?nameprefix}icestorm3.7
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

#
# libice-c++-devel package
#
%package -n lib%{?nameprefix}ice-c++-devel
Summary: Libraries and headers for developing Ice applications in C++.
Group: Development/Tools
Obsoletes: ice-c++-devel < 3.6
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
Requires: %{?nameprefix}ice-compilers = %{version}-%{release}
%description -n lib%{?nameprefix}ice-c++-devel
This package contains the libraries and headers needed for developing
Ice applications in C++.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# ice-compilers package
#
%package -n %{?nameprefix}ice-compilers
Summary: Slice compilers for developing Ice applications
Group: Development/Tools
Obsoletes: %{?nameprefix}libice-java < 3.7, %{?nameprefix}php-ice-devel < 3.7, %{?nameprefix}ice-utils < 3.7
Obsoletes: ice-php-devel < 3.6, ice-python-devel < 3.6, ice-java-devel < 3.6, ice-ruby-devel < 3.6
Requires: %{?nameprefix}ice-slice = %{version}-%{release}
%description -n %{?nameprefix}ice-compilers
This package contains Slice compilers for developing Ice applications.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# ice-utils package
#
%package -n %{?nameprefix}ice-utils
Summary: Ice utilities and admin tools.
Group: Applications/System
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
%description -n %{?nameprefix}ice-utils
This package contains Ice utilities and admin tools.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# icegrid package
#
%package -n %{?nameprefix}icegrid
Summary: Locate, deploy, and manage Ice servers.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
%description -n %{?nameprefix}icegrid
This package contains the IceGrid service. IceGrid helps you locate,
deploy and manage Ice servers.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# glacier2 package
#
%package -n %{?nameprefix}glacier2
Summary: Glacier2 router.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
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

#
# icebridge package
#
%package -n %{?nameprefix}icebridge
Summary: Ice bridge.
Group: System Environment/Daemons
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
%description -n %{?nameprefix}icebridge
This package contains the Ice bridge. The Ice bridge allows you to bridge
connections securely between one or multiple clients and a server. It
relays requests from clients to a target server and makes every effort
to be as transparent as possible.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# icepatch2 package
#
%package -n %{?nameprefix}icepatch2
Summary: File distribution and patching.
Group: System Environment/Daemons
Obsoletes: ice-servers < 3.6
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
%description -n %{?nameprefix}icepatch2
This package contains the IcePatch2 service. With IcePatch2, you can easily
distribute a large set of files to many clients and keep these files
synced with your source set.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if "%{cppcompiler}" == "g++"
#
# python-ice package
#
%package -n %{pythonname}-%{?nameprefix}ice
Summary: Python extension for Ice.
Group: System Environment/Libraries
Obsoletes: ice-python < 3.6
Requires: lib%{?nameprefix}ice3.7-c++ = %{version}-%{release}
Requires: %{pythonname}
%description -n %{pythonname}-%{?nameprefix}ice
This package contains a Python extension for communicating with Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.
%endif

%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n ice-%{archive_dir_suffix} -a 1

%build
export PATH=/opt/freeware/bin:$PATH
make %{makebuildopts} PLATFORMS="ppc64 ppc" LANGUAGES="cpp" srcs
%if "%{cppcompiler}" == "g++"
   make %{makebuildopts} PYTHON=%{pythonname} LANGUAGES="python" srcs
%endif

%install
export PATH=/opt/freeware/bin:$PATH
make           %{makeinstallopts} install-slice
make -C cpp    %{makeinstallopts} PLATFORMS="ppc64 ppc" install
%if "%{cppcompiler}" == "g++"
   make -C python %{makeinstallopts} PYTHON=%{pythonname} install_pythondir=%{pythondir} install
%endif

# Put lib32 content into main lib
(
    cd %{buildroot}%{_libdir32}
    for i in lib*.a
    do
        /usr/bin/ar -X32 -x $i
        /usr/bin/ar -X32 -qs %{buildroot}%{_libdir}/$i lib*.so.*
        rm -f lib*.so.*
    done
)

# Cleanup extra files
rm -f %{buildroot}%{_bindir}/slice2confluence
mv %{buildroot}%{_bindir}/icebox_32 %{buildroot}%{_bindir}/icebox32
rm -f %{buildroot}%{_bindir}/*_32
mv %{buildroot}%{_bindir}/icebox32 %{buildroot}%{_bindir}/icebox_32

# Create symlink to /usr/bin
(
    mkdir -p %{buildroot}/usr/bin
    cd %{buildroot}%{_bindir}
    for i in *; do ln -s %{_bindir}/$i %{buildroot}/usr/bin/$i; done
)

#
# noarch file packages
#

%files -n %{?nameprefix}ice-slice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%dir %{_datadir}/ice
%{_datadir}/ice/slice

#
# arch-specific packages
#

#
# Generate "ice-all-runtime" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-runtime
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix

#
# Generate "ice-all-devel" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-devel
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix

#
# libice-Mm-c++ package
#
%files -n lib%{?nameprefix}ice3.7-c++
%license LICENSE
%license ICE_LICENSE
%license %{rpmbuildfiles}/EXPAT_LICENSE
%license %{rpmbuildfiles}/LMDB_LICENSE
%license %{rpmbuildfiles}/MCPP_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_libdir}/libGlacier2.a
%{_libdir}/libIce.a
%{_libdir}/libIceBox.a
%{_libdir}/libIceDiscovery.a
%{_libdir}/libIceGrid.a
%{_libdir}/libIceLocatorDiscovery.a
%{_libdir}/libIcePatch2.a
%{_libdir}/libIceSSL.a
%{_libdir}/libIceStorm.a
%{_libdir}/libIceDB.a
%{_libdir}/libGlacier2CryptPermissionsVerifier.a
%{_libdir}/libIceXML.a
%if "%{cppcompiler}" != "xlC_r"
%{_libdir}/libGlacier2++11.a
%{_libdir}/libIce++11.a
%{_libdir}/libIceBox++11.a
%{_libdir}/libIceDiscovery++11.a
%{_libdir}/libIceGrid++11.a
%{_libdir}/libIceLocatorDiscovery++11.a
%{_libdir}/libIceSSL++11.a
%{_libdir}/libIceStorm++11.a
%endif

#
# icebox package
#
%files -n %{?nameprefix}icebox
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/icebox
%{_bindir}/icebox_32
/usr/bin/icebox
/usr/bin/icebox_32
%{_mandir}/man1/icebox.1*

#
# libice-c++devel package
#
%files -n lib%{?nameprefix}ice-c++-devel
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil

#
# libicestorm-Mm package
#
%files -n lib%{?nameprefix}icestorm3.7
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_libdir}/libIceStormService.a

#
# ice-compilers package
#
%files -n %{?nameprefix}ice-compilers
%license LICENSE
%license ICE_LICENSE
%license %{rpmbuildfiles}/MCPP_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/slice2cpp
/usr/bin/slice2cpp
%{_mandir}/man1/slice2cpp.1*
%{_bindir}/slice2cs
/usr/bin/slice2cs
%{_mandir}/man1/slice2cs.1*
%{_bindir}/slice2html
/usr/bin/slice2html
%{_mandir}/man1/slice2html.1*
%{_bindir}/slice2java
/usr/bin/slice2java
%{_mandir}/man1/slice2java.1*
%{_bindir}/slice2js
/usr/bin/slice2js
%{_mandir}/man1/slice2js.1*
%{_bindir}/slice2matlab
/usr/bin/slice2matlab
%{_mandir}/man1/slice2matlab.1*
%{_bindir}/slice2objc
/usr/bin/slice2objc
%{_mandir}/man1/slice2objc.1*
%{_bindir}/slice2php
/usr/bin/slice2php
%{_mandir}/man1/slice2php.1*
%{_bindir}/slice2py
/usr/bin/slice2py
%{_mandir}/man1/slice2py.1*
%{_bindir}/slice2rb
/usr/bin/slice2rb
%{_mandir}/man1/slice2rb.1*
%{_bindir}/slice2swift
/usr/bin/slice2swift
%{_mandir}/man1/slice2swift.1*

#
# ice-utils package
#
%files -n %{?nameprefix}ice-utils
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/iceboxadmin
/usr/bin/iceboxadmin
%{_mandir}/man1/iceboxadmin.1*
%{_bindir}/icepatch2calc
/usr/bin/icepatch2calc
%{_mandir}/man1/icepatch2calc.1*
%{_bindir}/icepatch2client
/usr/bin/icepatch2client
%{_mandir}/man1/icepatch2client.1*
%{_bindir}/icestormadmin
/usr/bin/icestormadmin
%{_mandir}/man1/icestormadmin.1*
%{_bindir}/icestormdb
/usr/bin/icestormdb
%{_mandir}/man1/icestormdb.1*
%{_bindir}/icegridadmin
/usr/bin/icegridadmin
%{_mandir}/man1/icegridadmin.1*
%{_bindir}/icegriddb
/usr/bin/icegriddb
%{_mandir}/man1/icegriddb.1*

#
# icegrid package
#
%files -n %{?nameprefix}icegrid
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/icegridnode
/usr/bin/icegridnode
%{_mandir}/man1/icegridnode.1*
%{_bindir}/icegridregistry
/usr/bin/icegridregistry
%{_mandir}/man1/icegridregistry.1*
%dir %{_datadir}/ice
%{_datadir}/ice/templates.xml

#
# glacier2 package
#
%files -n %{?nameprefix}glacier2
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/glacier2router
/usr/bin/glacier2router
%{_mandir}/man1/glacier2router.1*

#
# icebridge package
#
%files -n %{?nameprefix}icebridge
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/icebridge
/usr/bin/icebridge
%{_mandir}/man1/icebridge.1*

#
# icepatch2 package
#
%files -n %{?nameprefix}icepatch2
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{_bindir}/icepatch2server
/usr/bin/icepatch2server
%{_mandir}/man1/icepatch2server.1*

%if "%{cppcompiler}" == "g++"
#
# python-ice package
#
%files -n %{pythonname}-%{?nameprefix}ice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README.aix
%{pythondir}/*
%endif

%changelog
* Tue Mar 14 2023 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.9
- 3.7.9 release

* Tue Jun 27 2022 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.8
- 3.7.8 release

* Tue Nov 30 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.7
- 3.7.7 release

* Thu May 20 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.6
- 3.7.6 release

* Fri Jan 1 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.5
- 3.7.5 release

* Tue Apr 21 2020 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.4
- 3.7.4 release

* Tue Jul 16 2019 Bernard Normier <bernard@zeroc.com> 3.7.3
- AIX fork.

* Thu Nov 29 2018 Bernard Normier <bernard@zeroc.com> 3.7.2
- Updates for the 3.7.2 release, see ice/CHANGELOG-3.7.md.

* Fri Apr 13 2018 Bernard Normier <bernard@zeroc.com> 3.7.1
- Updates for the 3.7.1 release, see ice/CHANGELOG-3.7.md.

* Fri Jul 21 2017 Bernard Normier <bernard@zeroc.com> 3.7.0
- Updates for the 3.7.0 release, see ice/CHANGELOG-3.7.md.

* Thu Apr 13 2017 José Gutiérrez de la Concha <jose@zeroc.com> 3.7b0
- Added slice2js, slice2rb and slice2obj to ice-compilers

* Fri Mar 10 2017 Benoit Foucher <benoit@zeroc.com> 3.7b0
- Added icebridge package

* Tue Mar 7 2017 Benoit Foucher <benoit@zeroc.com> 3.7b0
- Version bump

* Fri Feb 17 2017 Bernard Normier <bernard@zeroc.com> 3.7a4
- Updates for Ice 3.7
 - Added python-ice package
 - Added slice2cs and slice2py to ice-compilers
 - Removed libice-java package
 - Build with recommended compiler flags
 - Enable debuginfo packages

* Wed Sep 14 2016 José Gutiérrez de la Concha <jose@zeroc.com> 3.7a3
- Rename ice-utils-java as icegridgui

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
 - The Ice jar files are now installed in _javalibdir, with
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
