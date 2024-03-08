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

#
# SLES12 does not define the dist macro
#
%if 0%{?suse_version} == 1315
%global dist                  .sles12
%endif

%define rpmbuildfiles ice-packaging-%{archive_dir_suffix}/ice/rpm

%define shadow shadow-utils
%define javapackagestools javapackages-tools
%define phpdevel php-devel
# Unfortunately bzip2-devel does not provide pkgconfig(bzip2) as of EL7
%define bzip2devel bzip2-devel
%define phpdir %{_datadir}/php
%define phplibdir %{_libdir}/php/modules
%define phpcommon php-common

%if "%{dist}" != ".el9"
%define pythonname python
%define pythondir %{python_sitearch}
%endif

%if "%{dist}" == ".sles12"
   %define phpdevel php74-devel
   %define bzip2devel libbz2-devel
   %define shadow shadow
   %define phpdir %{_datadir}/php7
   %define phpcommon php74
   %define phplibdir %{_libdir}/php74/extensions
%endif

%if "%{dist}" == ".el8"
   %define pythonname python2
   %define pythondir %{python2_sitearch}
%endif

%if "%{_prefix}" == "/usr"
   %define runpath embedded_runpath=no
%else
   %define runpath embedded_runpath_prefix=%{_prefix}
%endif

%define makebuildopts CONFIGS="shared cpp11-shared" OPTIMIZE=yes V=1 %{runpath} %{?_smp_mflags}
%define makeinstallopts CONFIGS="shared cpp11-shared" OPTIMIZE=yes V=1 %{runpath} DESTDIR=%{buildroot} prefix=%{_prefix} install_bindir=%{_bindir} install_libdir=%{_libdir} install_slicedir=%{_datadir}/ice/slice install_includedir=%{_includedir} install_mandir=%{_mandir} install_configdir=%{_datadir}/ice install_javadir=%{_javadir} install_phplibdir=%{phplibdir} install_phpdir=%{phpdir}

Name: %{?nameprefix}ice
Version: 3.7.10
Summary: Comprehensive RPC framework with support for C++, Java, JavaScript, Python and more.
Release: 2%{?dist}
%if "%{?ice_license}"
License: %{ice_license}
%else
License: GPLv2 with exceptions
%endif
Vendor: ZeroC, Inc.
URL: https://zeroc.com/
Source0: https://github.com/zeroc-ice/ice/archive/%{archive_tag}/%{name}-%{version}.tar.gz
Source1: https://github.com/zeroc-ice/ice-packaging/archive/%{archive_tag}/%{name}-packaging-%{version}.tar.gz
Patch0: 0001-Remove-workaround-for-old-proguard-version-1913.patch

# It's necessary to specify glibc-devel and libstdc++-devel here because gcc/gcc-c++ no longer install
# the 32-bits versions by default on Rhel8 (see https://bugzilla.redhat.com/show_bug.cgi?id=1779597)
BuildRequires: glibc-devel, libstdc++-devel
BuildRequires: pkgconfig(expat), pkgconfig(libedit), pkgconfig(lmdb), pkgconfig(mcpp), pkgconfig(openssl), %{bzip2devel}
BuildRequires: pkgconfig(libsystemd)

%if "%{dist}" == ".el9"
BuildRequires: java-11-openjdk-devel java-11-openjdk-jmods
%endif

%ifarch %{_host_cpu}
BuildRequires: %{phpdevel}, %{javapackagestools}
   %if "%{dist}" != ".el9"
BuildRequires: pkgconfig(python-2.7)
   %endif
   %if "%{dist}" == ".amzn2"
BuildRequires: pkgconfig(python-3.7), python3-rpm-macros
   %endif
   %if "%{dist}" == ".el8" || "%{dist}" == ".el9"
BuildRequires: pkgconfig(python3), python3-rpm-macros
   %endif
%endif

%description
Not used

#
# Enable debug package except if it's already enabled
#
%if %{!?_enable_debug_packages:1}%{?_enable_debug_packages:0}
%debug_package
%endif

%ifarch %{_host_cpu} # We build noarch packages only on %{_host_cpu}

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
# icegridgui package
#
%package -n %{?nameprefix}icegridgui
Summary: IceGrid GUI admin client.
Group: Applications/System
BuildArch: noarch
Obsoletes: ice-utils < 3.6, %{?nameprefix}ice-utils-java < 3.7
Requires: java
%description -n %{?nameprefix}icegridgui
The IceGrid service helps you locate, deploy and manage Ice servers.

IceGridGUI gives you complete control over your deployed applications.
Activities such as starting a server or modifying a configuration setting
are just a mouse click away.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%endif

#
# This "meta" package includes all run-time components and services.
#
%package -n %{?nameprefix}ice-all-runtime
Summary: Ice run-time packages (meta package).
Group: System Environment/Libraries
Requires: %{?nameprefix}icebox%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}icestorm3.7%{?_isa} = %{version}-%{release}
%ifarch %{_host_cpu}
Requires: %{?nameprefix}glacier2%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icegrid%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icepatch2%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icebridge%{?_isa} = %{version}-%{release}
Requires: php-%{?nameprefix}ice%{?_isa} = %{version}-%{release}
   %if "%{dist}" != ".el9"
Requires: %{pythonname}-%{?nameprefix}ice%{?_isa} = %{version}-%{release}
   %endif
   %if "%{dist}" == ".amzn2" || "%{dist}" == ".el8" || "%{dist}" == ".el9"
Requires: python3-%{?nameprefix}ice%{?_isa} = %{version}-%{release}
   %endif
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icegridgui = %{version}-%{release}
%endif # %{_host_cpu}
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
Requires: lib%{?nameprefix}ice-c++-devel%{?_isa} = %{version}-%{release}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
%ifarch %{_host_cpu}
Requires: %{?nameprefix}ice-compilers%{?_isa} = %{version}-%{release}
%else
    %ifarch %{ix86}
Requires: %{?nameprefix}ice-compilers(x86-64) = %{version}-%{release}
    %endif
%endif
Requires: glibc-devel%{?_isa}
%description -n lib%{?nameprefix}ice-c++-devel
This package contains the libraries and headers needed for developing
Ice applications in C++.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%ifarch %{_host_cpu}

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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
# Requirements for the users
Requires(pre): %{shadow}
%{?systemd_requires: %systemd_requires}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires(pre): %{shadow}
%{?systemd_requires: %systemd_requires}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
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
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
%description -n %{?nameprefix}icepatch2
This package contains the IcePatch2 service. With IcePatch2, you can easily
distribute a large set of files to many clients and keep these files
synced with your source set.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# php-ice package
#
%package -n php-%{?nameprefix}ice
Summary: PHP extension for Ice.
Group: System Environment/Libraries
Obsoletes: ice-php < 3.6
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{phpcommon}%{?_isa}

%description -n php-%{?nameprefix}ice
This package contains a PHP extension for communicating with Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if "%{dist}" != ".el9"
#
# python-ice package
#
%package -n %{pythonname}-%{?nameprefix}ice
Summary: Python extension for Ice.
Group: System Environment/Libraries
Obsoletes: ice-python < 3.6
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: %{pythonname}
%description -n %{pythonname}-%{?nameprefix}ice
This package contains a Python extension for communicating with Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.
%endif

%if "%{dist}" == ".amzn2" || "%{dist}" == ".el8" || "%{dist}" == ".el9"
#
# python3-ice package
#
%package -n python3-%{?nameprefix}ice
Summary: Python extension for Ice.
Group: System Environment/Libraries
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: python3
%description -n python3-%{?nameprefix}ice
This package contains a Python extension for communicating with Ice.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.
%endif

%endif #%{_host_cpu}

%prep
%setup -q -n ice-%{archive_dir_suffix} -a 1
cp %{_builddir}/ice-%{archive_dir_suffix}/python %{_builddir}/ice-%{archive_dir_suffix}/python3 -rf

%build
#
# Recommended flags for optimized hardened build
#
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"

%ifarch %{_host_cpu}
    make %{makebuildopts} LANGUAGES="cpp java php" srcs
    %if "%{dist}" != ".el9"
        make %{makebuildopts} PYTHON=%{pythonname} -C python srcs
    %endif
    %if "%{dist}" == ".amzn2" || "%{dist}" == ".el8" || "%{dist}" == ".el9"
        make %{makebuildopts} PYTHON=python3 -C python3 srcs
    %endif
%else
    %ifarch %{ix86}
        make %{makebuildopts} PLATFORMS=x86 LANGUAGES="cpp" srcs
    %endif
%endif

%install

%ifarch %{_host_cpu}
    make           %{?_smp_mflags} %{makeinstallopts} install-slice
    make -C cpp    %{?_smp_mflags} %{makeinstallopts} install
    make -C php    %{?_smp_mflags} %{makeinstallopts} install
    %if "%{dist}" != ".el9"
    make -C python %{?_smp_mflags} %{makeinstallopts} PYTHON=%{pythonname} install_pythondir=%{pythondir} install
    %endif
    %if "%{dist}" == ".amzn2" || "%{dist}" == ".el8" || "%{dist}" == ".el9"
        make -C python3 %{?_smp_mflags} %{makeinstallopts} PYTHON=python3 install_pythondir=%{python3_sitearch} install
    %endif
    make -C java   %{?_smp_mflags} %{makeinstallopts} install-icegridgui
%else
    %ifarch %{ix86}
        make -C cpp    %{?_smp_mflags} %{makeinstallopts} PLATFORMS=x86 install
    %endif
%endif

# Cleanup extra files
rm -f %{buildroot}%{_bindir}/slice2confluence

%ifarch %{_host_cpu}

#
# php ice.ini
#
%if "%{dist}" == ".sles12"
    mkdir -p %{buildroot}%{_sysconfdir}/php74/conf.d
    cp -p %{rpmbuildfiles}/ice.ini %{buildroot}%{_sysconfdir}/php74/conf.d
%else
    mkdir -p %{buildroot}%{_sysconfdir}/php.d
    cp -p %{rpmbuildfiles}/ice.ini %{buildroot}%{_sysconfdir}/php.d
%endif

#
# systemd files (for servers)
#
mkdir -p %{buildroot}%{_sysconfdir}
for i in icegridregistry icegridnode glacier2router
do
    cp %{rpmbuildfiles}/$i.conf %{buildroot}%{_sysconfdir}
    install -m 644 -p -D %{rpmbuildfiles}/$i.service %{buildroot}%{_unitdir}/$i.service
done

#
# IceGridGUI
#
mkdir -p %{buildroot}%{_bindir}
cp -p %{rpmbuildfiles}/icegridgui %{buildroot}%{_bindir}/icegridgui

%else

# These directories and files aren't needed in the x86 build.
rm -f %{buildroot}%{_libdir}/libGlacier2CryptPermissionsVerifier.so*
rm -f %{buildroot}%{_libdir}/libIceXML*.so*
rm -f %{buildroot}%{_bindir}/slice2*
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/ice

%endif # %{_host_cpu}

%ifarch %{_host_cpu}

#
# noarch file packages
#

%files -n %{?nameprefix}ice-slice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%dir %{_datadir}/ice
%{_datadir}/ice/slice

%files -n %{?nameprefix}icegridgui
%license LICENSE
%license ICE_LICENSE
%license %{rpmbuildfiles}/JGOODIES_LICENSE
%doc %{rpmbuildfiles}/README
%attr(755,root,root) %{_bindir}/icegridgui
%{_javadir}/icegridgui.jar

%endif # %{_host_cpu}

#
# arch-specific packages
#

#
# Generate "ice-all-runtime" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-runtime
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README

#
# Generate "ice-all-devel" meta package as arch-specific
#
%files -n %{?nameprefix}ice-all-devel
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README

#
# libice-Mm-c++ package
#
%files -n lib%{?nameprefix}ice3.7-c++
%license LICENSE
%license ICE_LICENSE
%license %{rpmbuildfiles}/LMDB_LICENSE
%license %{rpmbuildfiles}/MCPP_LICENSE
%doc %{rpmbuildfiles}/README
%{_libdir}/libGlacier2.so.*
%{_libdir}/libIce.so.*
%{_libdir}/libIceBox.so.*
%{_libdir}/libIceDiscovery.so.*
%{_libdir}/libIceGrid.so.*
%{_libdir}/libIceLocatorDiscovery.so.*
%{_libdir}/libIcePatch2.so.*
%{_libdir}/libIceSSL.so.*
%{_libdir}/libIceStorm.so.*
%{_libdir}/libIceDB.so.*
%{_libdir}/libGlacier2++11.so.*
%{_libdir}/libIce++11.so.*
%{_libdir}/libIceBox++11.so.*
%{_libdir}/libIceDiscovery++11.so.*
%{_libdir}/libIceGrid++11.so.*
%{_libdir}/libIceLocatorDiscovery++11.so.*
%{_libdir}/libIceSSL++11.so.*
%{_libdir}/libIceStorm++11.so.*
%ifarch %{_host_cpu}
%{_libdir}/libGlacier2CryptPermissionsVerifier.so.*
%{_libdir}/libIceXML.so.*
%endif
%post -n lib%{?nameprefix}ice3.7-c++ -p /sbin/ldconfig
%postun -n lib%{?nameprefix}ice3.7-c++
/sbin/ldconfig
exit 0

#
# icebox package
#
%files -n %{?nameprefix}icebox
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%ifarch %{_host_cpu}
%{_bindir}/icebox
%{_bindir}/icebox++11
%{_mandir}/man1/icebox.1*
%else
    %ifarch %{ix86}
%{_bindir}/icebox32
%{_bindir}/icebox32++11
    %endif
%endif
%post -n %{?nameprefix}icebox -p /sbin/ldconfig
%postun -n %{?nameprefix}icebox
/sbin/ldconfig
exit 0

#
# libice-c++devel package
#
%files -n lib%{?nameprefix}ice-c++-devel
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_libdir}/libGlacier2.so
%{_libdir}/libIce.so
%{_libdir}/libIceBox.so
%{_libdir}/libIceDiscovery.so
%{_libdir}/libIceGrid.so
%{_libdir}/libIceLocatorDiscovery.so
%{_libdir}/libIcePatch2.so
%{_libdir}/libIceSSL.so
%{_libdir}/libIceStorm.so
%{_libdir}/libGlacier2++11.so
%{_libdir}/libIce++11.so
%{_libdir}/libIceBox++11.so
%{_libdir}/libIceDiscovery++11.so
%{_libdir}/libIceGrid++11.so
%{_libdir}/libIceLocatorDiscovery++11.so
%{_libdir}/libIceSSL++11.so
%{_libdir}/libIceStorm++11.so
%ifarch %{_host_cpu}
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%endif

#
# libicestorm-Mm package
#
%files -n lib%{?nameprefix}icestorm3.7
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_libdir}/libIceStormService.so.*
%post -n lib%{?nameprefix}icestorm3.7 -p /sbin/ldconfig
%postun -n lib%{?nameprefix}icestorm3.7
/sbin/ldconfig
exit 0

%ifarch %{_host_cpu}

#
# ice-compilers package
#
%files -n %{?nameprefix}ice-compilers
%license LICENSE
%license ICE_LICENSE
%license %{rpmbuildfiles}/MCPP_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/slice2cpp
%{_mandir}/man1/slice2cpp.1*
%{_bindir}/slice2cs
%{_mandir}/man1/slice2cs.1*
%{_bindir}/slice2html
%{_mandir}/man1/slice2html.1*
%{_bindir}/slice2java
%{_mandir}/man1/slice2java.1*
%{_bindir}/slice2js
%{_mandir}/man1/slice2js.1*
%{_bindir}/slice2matlab
%{_mandir}/man1/slice2matlab.1*
%{_bindir}/slice2objc
%{_mandir}/man1/slice2objc.1*
%{_bindir}/slice2php
%{_mandir}/man1/slice2php.1*
%{_bindir}/slice2py
%{_mandir}/man1/slice2py.1*
%{_bindir}/slice2rb
%{_mandir}/man1/slice2rb.1*
%{_bindir}/slice2swift
%{_mandir}/man1/slice2swift.1*

#
# ice-utils package
#
%files -n %{?nameprefix}ice-utils
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/iceboxadmin
%{_mandir}/man1/iceboxadmin.1*
%{_bindir}/icepatch2calc
%{_mandir}/man1/icepatch2calc.1*
%{_bindir}/icepatch2client
%{_mandir}/man1/icepatch2client.1*
%{_bindir}/icestormadmin
%{_mandir}/man1/icestormadmin.1*
%{_bindir}/icestormdb
%{_mandir}/man1/icestormdb.1*
%{_bindir}/icegridadmin
%{_mandir}/man1/icegridadmin.1*
%{_bindir}/icegriddb
%{_mandir}/man1/icegriddb.1*
%post -n %{?nameprefix}ice-utils -p /sbin/ldconfig
%postun -n %{?nameprefix}ice-utils
/sbin/ldconfig
exit 0

#
# icegrid package
#
%files -n %{?nameprefix}icegrid
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/icegridnode
%{_mandir}/man1/icegridnode.1*
%{_bindir}/icegridregistry
%{_mandir}/man1/icegridregistry.1*
%dir %{_datadir}/ice
%{_datadir}/ice/templates.xml
%attr(644,root,root) %{_unitdir}/icegridregistry.service
%attr(644,root,root) %{_unitdir}/icegridnode.service
%config(noreplace) %{_sysconfdir}/icegridregistry.conf
%config(noreplace) %{_sysconfdir}/icegridnode.conf

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
  %systemd_post icegridregistry.service
  %systemd_post icegridnode.service
%endif

%preun -n %{?nameprefix}icegrid
%if "%{_prefix}" == "/usr"
  %systemd_preun icegridnode.service
  %systemd_preun icegridregistry.service
%endif

%postun -n %{?nameprefix}icegrid
%if "%{_prefix}" == "/usr"
  %systemd_postun_with_restart icegridnode.service
  %systemd_postun_with_restart icegriregistry.service
%endif
/sbin/ldconfig
exit 0

#
# glacier2 package
#
%files -n %{?nameprefix}glacier2
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/glacier2router
%{_mandir}/man1/glacier2router.1*
%attr(644,root,root) %{_unitdir}/glacier2router.service
%config(noreplace) %{_sysconfdir}/glacier2router.conf

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
  %systemd_post glacier2router.service
%endif

%preun -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  %systemd_preun glacier2router.service
%endif

%postun -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  %systemd_postun_with_restart glacier2router.service
%endif
/sbin/ldconfig
exit 0

#
# icebridge package
#
%files -n %{?nameprefix}icebridge
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/icebridge
%{_mandir}/man1/icebridge.1*
%post -n %{?nameprefix}icebridge -p /sbin/ldconfig
%postun -n %{?nameprefix}icebridge
/sbin/ldconfig
exit 0

#
# icepatch2 package
#
%files -n %{?nameprefix}icepatch2
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{_bindir}/icepatch2server
%{_mandir}/man1/icepatch2server.1*
%post -n %{?nameprefix}icepatch2 -p /sbin/ldconfig
%postun -n %{?nameprefix}icepatch2
/sbin/ldconfig
exit 0

#
# php-ice package
#
%files -n php-%{?nameprefix}ice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{phpdir}
%{phplibdir}/ice.so
%if "%{dist}" == ".sles12"
%config(noreplace) %{_sysconfdir}/php74/conf.d/ice.ini
%else
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif

%if "%{dist}" != ".el9"
#
# python-ice package
#
%files -n %{pythonname}-%{?nameprefix}ice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{pythondir}/*

%endif

%if "%{dist}" == ".amzn2" || "%{dist}" == ".el8" || "%{dist}" == ".el9"
#
# python3-ice package
#
%files -n python3-%{?nameprefix}ice
%license LICENSE
%license ICE_LICENSE
%doc %{rpmbuildfiles}/README
%{python3_sitearch}/*
%endif

%endif #%{_host_cpu}

%changelog
* Fri Mar 8 2024 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.10-2
- Fix IceGridGUI JDK 8 builds https://github.com/zeroc-ice/ice/pull/1913

* Tue Nov 7 2023 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.10
- 3.7.10 release

* Tue Mar 14 2023 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.9
- 3.7.9 release

* Mon Jun 27 2022 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.8
- 3.7.8 release

* Tue Nov 30 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.7
- 3.7.7 release

* Thu May 20 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.6
- 3.7.6 release

* Fri Jan 1 2021 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.5
- 3.7.5 release

* Tue Apr 21 2020 José Gutiérrez de la Concha <jose@zeroc.com> 3.7.4
- 3.7.4 release

* Wed Apr 8 2020 Benoit Foucher <benoit@zeroc.com> 3.7.3-2
- Support for x86 multilib build on EL8 platforms

* Wed Jul 17 2019 Bernard Normier <bernard@zeroc.com> 3.7.3
- Updates for the 3.7.3 release.

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
