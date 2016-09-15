# **********************************************************************
#
# Copyright (c) 2003-2016 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************

%define systemd 1
%define systemdpkg systemd
%define shadow shadow-utils
%define javapackagestools jpackage-utils
%define phpdevel php-devel
%define expatdevel expat-devel
%define bzip2devel bzip2-devel
%define phpdir %{_datadir}/php
%define phplibdir %{_libdir}/php/modules
%define jarVersion 3.7.0-alpha3

%if "%{dist}" == ".el7"
  %define javapackagestools javapackages-tools
%endif
%if "%{dist}" == ".amzn1"
  %define systemd 0
%endif
%if "%{dist}" == ".sles12"
  %define systemdpkg systemd-rpm-macros
  %define phpdevel php5-devel
  %define expatdevel libexpat-devel
  %define bzip2devel libbz2-devel
  %define liblmdb liblmdb-0_9_11
  %define shadow shadow
  %define phpdir %{_datadir}/php5
  %define phplibdir %{_libdir}/php5/extensions
%endif

%if "%{_prefix}" == "/usr"
%define runpath embedded_runpath=no
%else
%define runpath embedded_runpath_prefix=%{_prefix}
%endif

%define rpmbuildfiles $RPM_BUILD_DIR/Ice-rpmbuild-%{version}


%define makebuildopts CONFIGS="shared cpp11-shared" OPTIMIZE=yes %{runpath} %{?_smp_mflags}
%define makeinstallopts CONFIGS="shared cpp11-shared" OPTIMIZE=yes %{runpath} DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} install_bindir=%{_bindir} install_libdir=%{_libdir} install_slicedir=%{_datadir}/Ice-%{version}/slice install_docdir=%{_datadir}/Ice-%{version}  install_includedir=%{_includedir} install_mandir=%{_mandir} install_configdir=%{_datadir}/Ice-%{version} install_javadir=%{_javadir} install_phplibdir=%{phplibdir} install_phpdir=%{phpdir}

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
Version: 3.7a3
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

BuildRequires: openssl-devel, mcpp-devel, lmdb-devel, %{bzip2devel} %{expatdevel} %{phpdevel} %{javapackagestools}
%if 0%{?biarch}
BuildRequires: openssl-devel(x86-32), mcpp-devel(x86-32), lmdb-devel(x86-32), %{bzip2devel}(x86-32), %{expatdevel}(x86-32)
%endif

%description
Ice is a comprehensive RPC framework that helps you build
distributed applications with minimal effort using familiar
object-oriented idioms.

#
# Arch-independent packages
#
%ifarch noarch

#
# ice-slice package
#
%package -n %{?nameprefix}ice-slice
Summary: Slice files for Ice.
Group: System Environment/Libraries
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
Summary: IceGrid Admin graphical client.
Group: Applications/System
Obsoletes: ice-utils < 3.6, ice-utils-java
Requires: java
%description -n %{?nameprefix}icegridgui
The IceGrid service helps you locate, deploy and manage Ice servers.

The IceGrid GUI give you complete control over your deployed applications.
Activities such as starting a server or modifying a configuration setting
are just a mouse click away.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

#
# libice-java package
#
%package -n lib%{?nameprefix}ice-java
Summary: Ice for Java run-time libraries.
Group: System Environment/Libraries
Obsoletes: ice-java-devel < 3.6, ice-java < 3.6
%description -n lib%{?nameprefix}ice-java
This package contains Ice for Java run-time libraries.

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
Requires: %{?nameprefix}icebox%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}icestorm3.7%{?_isa} = %{version}-%{release}
%if ! %{cppx86}
Requires: %{?nameprefix}glacier2%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icegrid%{?_isa} = %{version}-%{release}
Requires: %{?nameprefix}icepatch2%{?_isa} = %{version}-%{release}
Requires: php-%{?nameprefix}ice%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
Requires: lib%{?nameprefix}ice-java = %{version}-%{release}
Requires: %{?nameprefix}icegridgui = %{version}-%{release}
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
Requires: bzip2
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

#
# libicestormMm package
#
%package -n lib%{?nameprefix}icestorm3.7
Summary: IceStorm publish-subscribe event distribution service.
Group: System Environment/Libraries
%if "%{?liblmdb}" != ""
Requires: %{?liblmdb}
%endif
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
Requires: %{?nameprefix}ice-compilers(x86-64) = %{version}-%{release}
Requires: glibc-devel%{?_isa}
%description -n lib%{?nameprefix}ice-c++-devel
This package contains the libraries and headers needed for developing
Ice applications in C++.

Ice is a comprehensive RPC framework that helps you network your software
with minimal effort. Ice takes care of all interactions with low-level
network programming interfaces and allows you to focus your efforts on
your application logic.

%if ! %{cppx86}

#
# ice-compilers package
#
%package -n %{?nameprefix}ice-compilers
Summary: Slice compilers for developing Ice applications
Group: Development/Tools
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
Obsoletes: ice-utils < 3.6
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
Requires: %{?nameprefix}ice-utils = %{version}-%{release}
%if "%{?liblmdb}" != ""
Requires: %{?liblmdb}
%endif
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

#
# glacier2 package
#
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

#
# icepatch2 package
#
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

#
# php-ice package
#
%package -n php-%{?nameprefix}ice
Summary: PHP extension for Ice.
Group: System Environment/Libraries
Obsoletes: ice-php < 3.6
Requires: lib%{?nameprefix}ice3.7-c++%{?_isa} = %{version}-%{release}
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

%endif # ! cppx86

%endif # core_arches

%prep

%setup -n Ice-%{version} -q
%setup -n Ice-rpmbuild-%{version} -T -b 1

%build

cd $RPM_BUILD_DIR/Ice-%{version}

%ifarch %{core_arches}
    %if %{cppx86}
        make %{makebuildopts} PLATFORMS=x86 LANGUAGES="cpp" srcs
    %else
        make %{makebuildopts} PLATFORMS=x64 LANGUAGES="cpp php" srcs
    %endif
%endif

%ifarch noarch
    (cd cpp; make %{makebuildopts} slice2java)
    make %{makebuildopts} LANGUAGES="java java-compat" srcs
%endif


%install

rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/Ice-%{version}

%ifarch %{core_arches}
    PACKAGES="%{?nameprefix}ice-all-runtime \
              %{?nameprefix}icebox \
              %{?nameprefix}ice-all-devel \
              lib%{?nameprefix}ice3.7-c++ \
              lib%{?nameprefix}ice-c++-devel \
              lib%{?nameprefix}icestorm3.7"

    %if %{cppx86}
        make %{?_smp_mflags} %{makeinstallopts} PLATFORMS=x86 LANGUAGES="cpp" install
    %else
        PACKAGES="$PACKAGES \
                  %{?nameprefix}glacier2 \
                  %{?nameprefix}icebox  \
                  %{?nameprefix}icegrid \
                  %{?nameprefix}icepatch2 \
                  %{?nameprefix}ice-utils \
                  %{?nameprefix}ice-compilers \
                  php-%{?nameprefix}ice"

        make %{?_smp_mflags} %{makeinstallopts} PLATFORMS=x64 LANGUAGES="cpp php" install
    %endif
%endif

%ifarch noarch
    # Just install what is necessary for icegridgui
    PACKAGES="%{?nameprefix}icegridgui \
              %{?nameprefix}ice-slice \
              lib%{?nameprefix}ice-java"

    make %{makeinstallopts} LANGUAGES="java java-compat" install
%endif

#
# Doc & license files
#
for i in $PACKAGES
do
    mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
    cp -p %{rpmbuildfiles}/README.Linux $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}/README
    cp -p $RPM_BUILD_DIR/Ice-%{version}/LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
    cp -p $RPM_BUILD_DIR/Ice-%{version}/ICE_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/$i-%{version}
done

%ifarch %{core_arches}

# Cleanup extra files
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceStormService.so
rm -f $RPM_BUILD_ROOT%{_libdir}/libGlacier2CryptPermissionsVerifier.so
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2cs
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2confluence
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2js
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2objc
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2py
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2rb
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2js.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2objc.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2py.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/slice2rb.1

# The files below are packaged with the noarch RPM
rm -f $RPM_BUILD_ROOT/%{_javadir}/icegridgui.jar
rm -f $RPM_BUILD_ROOT%{_datadir}/slice
rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}/slice
rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}/LICENSE
rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}/ICE_LICENSE

%if %{cppx86}

# These directories and files aren't needed in the x86 build.
rm -f $RPM_BUILD_ROOT%{_libdir}/libGlacier2CryptPermissionsVerifier.so*
rm -f $RPM_BUILD_ROOT%{_libdir}/libIceXML*.so*
rm -f $RPM_BUILD_ROOT%{_bindir}/slice2*
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_mandir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}

%else
#
# php ice.ini
#
%if "%{dist}" == ".sles12"
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
    cp -p %{rpmbuildfiles}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php5/conf.d
%else
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
    cp -p %{rpmbuildfiles}/ice.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%endif

#
# initrd files (for servers)
#
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{rpmbuildfiles}/*.conf $RPM_BUILD_ROOT%{_sysconfdir}
for i in icegridregistry icegridnode glacier2router
do
    %if %{systemd}
        install -p -D %{rpmbuildfiles}/$i.service $RPM_BUILD_ROOT%{_unitdir}/$i.service
    %else
        install -p -D %{rpmbuildfiles}/$i.%{_vendor} $RPM_BUILD_ROOT%{_initrddir}/$i
    %endif
done

cp -p %{rpmbuildfiles}/MCPP_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/lib%{?nameprefix}ice3.7-c++-%{version}

%endif # ! cppx86

%endif

#
# Arch-independent packages
#
%ifarch noarch

cp -p %{rpmbuildfiles}/JGOODIES_LICENSE $RPM_BUILD_ROOT%{_defaultdocdir}/%{?nameprefix}icegridgui-%{version}

#
# IceGridGUI
#
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{rpmbuildfiles}/icegridgui $RPM_BUILD_ROOT%{_bindir}/icegridgui
if [ -n "$JARSIGNER_KEYSTORE" ]; then
    jarsigner -keystore $JARSIGNER_KEYSTORE -storepass "$JARSIGNER_KEYSTORE_PASSWORD" $RPM_BUILD_ROOT%{_javadir}/icegridgui.jar $JARSIGNER_KEYSTORE_ALIAS -tsa http://timestamp.digicert.com
fi

#
# Java links
#
for i in glacier2 ice icebox icediscovery icelocatordiscovery icegrid icepatch2 icestorm \
    glacier2-compat ice-compat icebox-compat icebt-compat icediscovery-compat icelocatordiscovery-compat \
    icegrid-compat icepatch2-compat icestorm-compat
do
    ln -s $i-%{jarVersion}.jar $RPM_BUILD_ROOT%{_javadir}/$i.jar
    ln -s $i-%{jarVersion}-sources.jar $RPM_BUILD_ROOT%{_javadir}/$i-sources.jar
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}/LICENSE
rm -rf $RPM_BUILD_ROOT%{_datadir}/Ice-%{version}/ICE_LICENSE
rm -f $RPM_BUILD_ROOT/%{_javadir}/*.pom

%endif # noarch

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

%files -n %{?nameprefix}icegridgui
%defattr(-, root, root, -)
%attr(755,root,root) %{_bindir}/icegridgui
%{_javadir}/icegridgui.jar
%{_defaultdocdir}/%{?nameprefix}icegridgui-%{version}

#
# libice-java package
#
%files -n lib%{?nameprefix}ice-java
%defattr(-, root, root, -)
%{_javadir}/ice-%{jarVersion}.jar
%{_javadir}/ice.jar
%{_javadir}/ice-%{jarVersion}-sources.jar
%{_javadir}/ice-sources.jar
%{_javadir}/glacier2-%{jarVersion}.jar
%{_javadir}/glacier2.jar
%{_javadir}/glacier2-%{jarVersion}-sources.jar
%{_javadir}/glacier2-sources.jar
%{_javadir}/icebox-%{jarVersion}.jar
%{_javadir}/icebox.jar
%{_javadir}/icebox-%{jarVersion}-sources.jar
%{_javadir}/icebox-sources.jar
#%{_javadir}/icebt-%{jarVersion}.jar
#%{_javadir}/icebt.jar
#%{_javadir}/icebt-%{jarVersion}-sources.jar
#%{_javadir}/icebt-sources.jar
%{_javadir}/icegrid-%{jarVersion}.jar
%{_javadir}/icegrid.jar
%{_javadir}/icegrid-%{jarVersion}-sources.jar
%{_javadir}/icegrid-sources.jar
%{_javadir}/icepatch2-%{jarVersion}.jar
%{_javadir}/icepatch2.jar
%{_javadir}/icepatch2-%{jarVersion}-sources.jar
%{_javadir}/icepatch2-sources.jar
%{_javadir}/icestorm-%{jarVersion}.jar
%{_javadir}/icestorm.jar
%{_javadir}/icestorm-%{jarVersion}-sources.jar
%{_javadir}/icestorm-sources.jar
%{_javadir}/icediscovery-%{jarVersion}.jar
%{_javadir}/icediscovery.jar
%{_javadir}/icediscovery-%{jarVersion}-sources.jar
%{_javadir}/icediscovery-sources.jar
%{_javadir}/icelocatordiscovery-%{jarVersion}.jar
%{_javadir}/icelocatordiscovery.jar
%{_javadir}/icelocatordiscovery-%{jarVersion}-sources.jar
%{_javadir}/icelocatordiscovery-sources.jar
%{_javadir}/ice-compat-%{jarVersion}.jar
%{_javadir}/ice-compat.jar
%{_javadir}/ice-compat-%{jarVersion}-sources.jar
%{_javadir}/ice-compat-sources.jar
%{_javadir}/glacier2-compat-%{jarVersion}.jar
%{_javadir}/glacier2-compat.jar
%{_javadir}/glacier2-compat-%{jarVersion}-sources.jar
%{_javadir}/glacier2-compat-sources.jar
%{_javadir}/icebox-compat-%{jarVersion}.jar
%{_javadir}/icebox-compat.jar
%{_javadir}/icebox-compat-%{jarVersion}-sources.jar
%{_javadir}/icebox-compat-sources.jar
%{_javadir}/icebt-compat-%{jarVersion}.jar
%{_javadir}/icebt-compat.jar
%{_javadir}/icebt-compat-%{jarVersion}-sources.jar
%{_javadir}/icebt-compat-sources.jar
%{_javadir}/icegrid-compat-%{jarVersion}.jar
%{_javadir}/icegrid-compat.jar
%{_javadir}/icegrid-compat-%{jarVersion}-sources.jar
%{_javadir}/icegrid-compat-sources.jar
%{_javadir}/icepatch2-compat-%{jarVersion}.jar
%{_javadir}/icepatch2-compat.jar
%{_javadir}/icepatch2-compat-%{jarVersion}-sources.jar
%{_javadir}/icepatch2-compat-sources.jar
%{_javadir}/icestorm-compat-%{jarVersion}.jar
%{_javadir}/icestorm-compat.jar
%{_javadir}/icestorm-compat-%{jarVersion}-sources.jar
%{_javadir}/icestorm-compat-sources.jar
%{_javadir}/icediscovery-compat-%{jarVersion}.jar
%{_javadir}/icediscovery-compat.jar
%{_javadir}/icediscovery-compat-%{jarVersion}-sources.jar
%{_javadir}/icediscovery-compat-sources.jar
%{_javadir}/icelocatordiscovery-compat-%{jarVersion}.jar
%{_javadir}/icelocatordiscovery-compat.jar
%{_javadir}/icelocatordiscovery-compat-%{jarVersion}-sources.jar
%{_javadir}/icelocatordiscovery-compat-sources.jar
%{_defaultdocdir}/lib%{?nameprefix}ice-java-%{version}

%endif # noarch

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

#
# libice-Mm-c++ package
#
%files -n lib%{?nameprefix}ice3.7-c++
%defattr(-, root, root, -)
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
%if ! %{cppx86}
%{_libdir}/libGlacier2CryptPermissionsVerifier.so.*
%{_libdir}/libIceXML.so.*
%endif
%{_defaultdocdir}/lib%{?nameprefix}ice3.7-c++-%{version}
%post -n lib%{?nameprefix}ice3.7-c++ -p /sbin/ldconfig
%postun -n lib%{?nameprefix}ice3.7-c++
/sbin/ldconfig
exit 0

#
# icebox package
#
%files -n %{?nameprefix}icebox
%defattr(-, root, root, -)
%if %{cppx86}
%{_bindir}/icebox32
%{_bindir}/icebox32++11
%else
%{_bindir}/icebox
%{_bindir}/icebox++11
%{_mandir}/man1/icebox.1*
%endif
%{_defaultdocdir}/%{?nameprefix}icebox-%{version}
%post -n %{?nameprefix}icebox -p /sbin/ldconfig
%postun -n %{?nameprefix}icebox
/sbin/ldconfig
exit 0

#
# libice-c++devel package
#
%files -n lib%{?nameprefix}ice-c++-devel
%defattr(-, root, root, -)
%{_libdir}/libGlacier2.so
%{_libdir}/libIce.so
%{_libdir}/libIceBox.so
%{_libdir}/libIceDiscovery.so
%{_libdir}/libIceGrid.so
%{_libdir}/libIceLocatorDiscovery.so
%{_libdir}/libIcePatch2.so
%{_libdir}/libIceSSL.so
%{_libdir}/libIceStorm.so
%{_libdir}/libIceDB.so
%{_libdir}/libGlacier2++11.so
%{_libdir}/libIce++11.so
%{_libdir}/libIceBox++11.so
%{_libdir}/libIceDiscovery++11.so
%{_libdir}/libIceGrid++11.so
%{_libdir}/libIceLocatorDiscovery++11.so
%{_libdir}/libIceSSL++11.so
%{_libdir}/libIceStorm++11.so
%if ! %{cppx86}
%{_includedir}/Glacier2
%{_includedir}/Ice
%{_includedir}/IceBox
%{_includedir}/IceGrid
%{_includedir}/IcePatch2
%{_includedir}/IceSSL
%{_includedir}/IceStorm
%{_includedir}/IceUtil
%{_libdir}/libIceXML.so
%endif
%{_defaultdocdir}/lib%{?nameprefix}ice-c++-devel-%{version}

#
# libicestorm-Mm package
#
%files -n lib%{?nameprefix}icestorm3.7
%defattr(-, root, root, -)
%{_libdir}/libIceStormService.so.*
%{_defaultdocdir}/lib%{?nameprefix}icestorm3.7-%{version}
%post -n lib%{?nameprefix}icestorm3.7 -p /sbin/ldconfig
%postun -n lib%{?nameprefix}icestorm3.7
/sbin/ldconfig
exit 0

%if ! %{cppx86}

#
# ice-compilers package
#
%files -n %{?nameprefix}ice-compilers
%defattr(-, root, root, -)
%{_bindir}/slice2cpp
%{_mandir}/man1/slice2cpp.1*
%{_bindir}/slice2java
%{_mandir}/man1/slice2java.1*
%{_bindir}/slice2html
%{_mandir}/man1/slice2html.1*
%{_bindir}/slice2php
%{_mandir}/man1/slice2php.1*
%{_defaultdocdir}/%{?nameprefix}ice-compilers-%{version}

#
# ice-utils package
#
%files -n %{?nameprefix}ice-utils
%defattr(-, root, root, -)
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
%{_defaultdocdir}/%{?nameprefix}ice-utils-%{version}
%post -n %{?nameprefix}ice-utils -p /sbin/ldconfig
%postun -n %{?nameprefix}ice-utils
/sbin/ldconfig
exit 0

#
# icegrid package
#
%files -n %{?nameprefix}icegrid
%defattr(-, root, root, -)
%{_bindir}/icegridnode
%{_mandir}/man1/icegridnode.1*
%{_bindir}/icegridregistry
%{_mandir}/man1/icegridregistry.1*
%dir %{_datadir}/Ice-%{version}
%{_datadir}/Ice-%{version}/templates.xml
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
    /sbin/chkconfig --add icegridregistry
    /sbin/chkconfig --add icegridnode
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
    /sbin/service icegridnode stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del icegridnode
    /sbin/service icegridregistry stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del icegridregistry
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
exit 0

#
# glacier2 package
#
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
    /sbin/chkconfig --add glacier2router
  %endif
%endif

%preun -n %{?nameprefix}glacier2
%if "%{_prefix}" == "/usr"
  if [ $1 = 0 ]; then
  %if %{systemd}
    /bin/systemctl --no-reload disable glacier2router.service >/dev/null 2>&1 || :
    /bin/systemctl stop glacier2router.service >/dev/null 2>&1 || :
  %else
    /sbin/service glacier2router stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del glacier2router
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
exit 0

#
# icepatch2 package
#
%files -n %{?nameprefix}icepatch2
%defattr(-, root, root, -)
%{_bindir}/icepatch2server
%{_mandir}/man1/icepatch2server.1*
%{_defaultdocdir}/%{?nameprefix}icepatch2-%{version}
%post -n %{?nameprefix}icepatch2 -p /sbin/ldconfig
%postun -n %{?nameprefix}icepatch2
/sbin/ldconfig
exit 0

#
# php-ice package
#
%files -n php-%{?nameprefix}ice
%defattr(-, root, root, -)
%{phpdir}
%{phplibdir}/IcePHP.so
%if "%{dist}" == ".sles12"
%config(noreplace) %{_sysconfdir}/php5/conf.d/ice.ini
%else
%config(noreplace) %{_sysconfdir}/php.d/ice.ini
%endif
%{_defaultdocdir}/php-%{?nameprefix}ice-%{version}

%endif # ! cppx86

%endif # core_arches

%changelog

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
