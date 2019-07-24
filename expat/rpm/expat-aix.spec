# rpm -ba --define 'dotests 0' expat-2.1.1-1.spec ...
%{!?dotests:%define DO_TESTS 1}
%{?dotests:%define DO_TESTS 0}


Summary: An XML parser library
Name: expat
Version: 2.2.6
Release: 2ice
Group: System Environment/Libraries
Source: https://github.com/libexpat/libexpat/archive/expat-%{version}.tar.gz
URL: http://www.libexpat.org/
License: MIT
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

%define _libdir64 %{_prefix}/lib64

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

The library is available as 32-bit and 64-bit.

%package static-devel
Summary: Libraries and header files to develop applications using expat
Group: Development/Libraries

%description static-devel
The expat-static-devel package contains the static library, include files and
documentation to develop XML applications with expat.

If you are compiling a 32-bit program, no special compiler options are
needed.

If you are compiling a 64-bit program, you have to compile and link your
application with "xlc_r -q64".

%prep
%setup -q
export PATH=/opt/freeware/bin:$PATH

# Duplicate source for 32 & 64 bits
rm -rf /tmp/%{name}-%{version}-32bit
mkdir  /tmp/%{name}-%{version}-32bit
mv *   /tmp/%{name}-%{version}-32bit
mkdir 32bit
mv     /tmp/%{name}-%{version}-32bit/* 32bit
rm -rf /tmp/%{name}-%{version}-32bit
mkdir 64bit
cp -pr 32bit/* 64bit/

%build
# setup environment for 32-bit and 64-bit builds
export PATH=/opt/freeware/bin:/usr/bin:/etc:/usr/sbin:/usr/bin/X11:/sbin:.
export RM="/usr/bin/rm -f"
export CONFIG_SHELL=/opt/freeware/bin/bash
CONFIG_ENV_ARGS=/opt/freeware/bin/bash
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"

# first build the 64-bit version
cd 64bit
export OBJECT_MODE=64
export CC="/opt/IBM/xlC/16.1.0/bin/xlc_r -q64 -qpic -O2"
export CXX="/opt/IBM/xlC/16.1.0/bin/xlC_r -q64 -qpic -O2"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir64} \
    --enable-static --disable-shared

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
#    /usr/sbin/slibclean
fi


# now build the 32-bit version
cd ../32bit
export OBJECT_MODE=32
export CC="/opt/IBM/xlC/16.1.0/bin/xlc_r -q32 -qpic -O2 -D_LARGE_FILES"
export CXX="/opt/IBM/xlC/16.1.0/bin/xlC_r -q32 -qpic -O2 -D_LARGE_FILES"
export LDFLAGS="-Wl,-bmaxdata:0x80000000"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-static --disable-shared

gmake %{?_smp_mflags}

if [ "%{DO_TESTS}" == 1 ]
then
    ( gmake -k check || true )
#    /usr/sbin/slibclean
fi


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

# setup environment for 32-bit and 64-bit builds
export AR="/usr/bin/ar -X32_64"
export NM="/usr/bin/nm -X32_64"
export RM="/usr/bin/rm -f"


# install 64-bit version

export OBJECT_MODE=64
cd 64bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install

# Save 64bits version of xmlwf
mv ${RPM_BUILD_ROOT}%{_bindir}/xmlwf ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64
# Strip 64bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_64 || :

# install 32-bit version

export OBJECT_MODE=32
cd ../32bit
gmake V=0 DESTDIR=${RPM_BUILD_ROOT} install
mv ${RPM_BUILD_ROOT}%{_bindir}/xmlwf ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_32
cd ${RPM_BUILD_ROOT}%{_bindir}
ln -sf xmlwf_64 xmlwf
cd -

# Strip 32bits version of xmlwf
/usr/bin/strip ${RPM_BUILD_ROOT}%{_bindir}/xmlwf_32 || :

# rename library to libexpat-static.a
mv ${RPM_BUILD_ROOT}%{_libdir}/libexpat.a ${RPM_BUILD_ROOT}%{_libdir}/libexpat-static.a

# Add 64 bit objects to static library
(
  cd ${RPM_BUILD_ROOT}/%{_libdir64}
  /usr/bin/ar -X64 -x libexpat.a
  /usr/bin/ar -X64 -qs ${RPM_BUILD_ROOT}%{_libdir}/libexpat-static.a *.o
)

rm -f examples/*.dsp
chmod 644 COPYING Changes doc/* examples/*

(
  cd ${RPM_BUILD_ROOT}
  for dir in bin include lib lib64
  do
    mkdir -p usr/${dir}
    cd usr/${dir}
    ln -sf ../..%{_prefix}/${dir}/* .
    cd -
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
#echo ${RPM_BUILD_ROOT}


#%files
#%defattr(-,root,system)
#%doc 32bit/COPYING
#%{_bindir}/*
#%{_datadir}/man/man?/*
#/usr/bin/*


%files static-devel
%defattr(-,root,system)
%doc 32bit/Changes 32bit/doc 32bit/examples
%{_libdir}/*.a
%{_includedir}/*.h
/usr/include/*
/usr/lib/*.a


%changelog
* Wed Jul 24 2019 Bernard Normier <bernard@zeroc.com> 2.2.6-2ice
- Fork to create a static library with xlc_r

* Wed Feb 20 2019 Reshma V Kumar <reskumar@in.ibm.com> 2.2.6-1
- Update to 2.2.6

* Thu Sep 01 2016 Nitish K Mishra <nitismis@in.ibm.com> 2.2.0-1
- Update to 2.2.0-1

* Wed May 18 2016 Reshma V Kumar <reskumar@in.ibm.com> 2.1.1-1
- updated to the latest version

* Fri Apr 29 2016 Tony Reix <tony.reix@bull.net> 2.1.1-1
- Update and Initial port on AIX 6.1

* Thu Jul 04 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.1.0-2
- Building on Aix5.3

* Wed Mar 06 2013 Gerard Visiedo <gerard.visiedo@bull.net> 2.1.0-1
- update to version 2.1.0

* Thu Feb 02 2012 Gerard Visiedo <gerard.visiedo@bull.net> 2.0.1-4
- Initial port on Aix6.1

* Fri Sep 23 2011 Patricia Cugny <patricia.cugny@bull.net> 2.0.1-3
- rebuild for compatibility with new libiconv.a 1.13.1-2

* Thu Jun 23 2011 Gerard Visiedo <gerard.visiedo@bull.net> -2.0.1-2
- Insert libexpat missing

* Mon Mar 20 2011  Patricia Cugny <patricia.cugny@bull.net> - 2.0.1-1
- update to version 2.0.1

*  Fri Dec 23 2005  BULL
 - Release 4
 - Prototype gtk 64 bit
*  Wed Nov 16 2005  BULL
 - Release  3
*  Mon May 30 2005  BULL
 - Release  2
 - .o removed from lib
