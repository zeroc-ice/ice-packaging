# The files themselves are in several subdirectories and need to be prefixed wit this.
%global archive_path libraries/lib%{name}

Name:           lmdb
Version:        0.9.22
Release:        1ice%{?dist}
Summary:        Memory-mapped key-value database

License:        OpenLDAP
URL:            http://symas.com/mdb/
Source:         https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz

%description
LMDB is an ultra-fast, ultra-compact key-value embedded data
store developed by Symas for the OpenLDAP Project. By using memory-mapped files,
it provides the read performance of a pure in-memory database while still
offering the persistence of standard disk-based databases, and is only limited
to the size of the virtual address space.

# disable debuginfo package
%define debug_package %{nil}

# Need bash shell
%define _buildshell /usr/bin/bash

%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
export PATH=/opt/freeware/bin:$PATH
%setup -q -n %{name}-LMDB_%{version}

%build
cp -rp %{archive_path} %{archive_path}-64

LDFLAGS="%{?__global_ldflags}"
export LDFLAGS

pushd %{archive_path}
# build 32-bit static libraries and exes
make CC=xlc_r AR="ar -X32" ILIBS=liblmdb.a W="-qhalt=i" THREADS= OPT= XCFLAGS="%{optflags} -qpic -q32 -qmaxmem=-1 -D_LARGE_FILES -DMDB_USE_ROBUST=0" %{?_smp_mflags}
popd

pushd %{archive_path}-64
# build 64-bit static libraries and exes  
make CC=xlc_r AR="ar -X64" ILIBS=liblmdb.a W="-qhalt=i" THREADS= OPT= XCFLAGS="%{optflags} -qpic -q64 -qmaxmem=-1 -DMDB_USE_ROBUST=0" %{?_smp_mflags}
popd

%install
pushd %{archive_path}
# make install expects existing directory tree
mkdir -m 0755 -p %{buildroot}%{_prefix}{/bin,/include}
mkdir -m 0755 -p %{buildroot}{%{_libdir},%{_mandir}/man1}
make ILIBS=liblmdb.a DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} mandir=%{_mandir} install
for f in %{buildroot}%{_prefix}/bin/mdb_* ; do mv $f "$f"_32; done
popd
pushd %{archive_path}-64
# 64-bit additions
ar -X64 rs %{buildroot}%{_libdir}/liblmdb.a mdb.o midl.o
for f in mdb_copy mdb_dump mdb_load mdb_stat; do cp $f %{buildroot}%{_prefix}/bin/"$f"_64; done 
popd

# strip exes
strip -X32_64 %{buildroot}%{_prefix}/bin/mdb_*

# create pkgconfig file
mkdir -m 0755 -p %{buildroot}%{_libdir}/pkgconfig
cat << "EOF" > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=${prefix}/include

Name: %{name}
Version: %{version}
Description: LMDB embedded data store
URL: %{url}
Libs: -L${libdir} -l%{name}
Cflags: -I${includedir}
EOF

%check
pushd %{archive_path}
rm -rf testdb
make ILIBS=liblmdb.a test
popd

%files
%doc %{archive_path}/COPYRIGHT
%doc %{archive_path}/CHANGES
%license %{archive_path}/LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%doc %{archive_path}/COPYRIGHT
%doc %{archive_path}/CHANGES
%license %{archive_path}/LICENSE
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jul 02 2019 Bernard Normier <bernard@zeroc.com> 0.9.22-1ice
- AIX fork

* Fri Mar 10 2017 Bernard Normier <bernard@zeroc.com> 0.9.18-3ice
- Added pkgconfig file

* Mon Feb 20 2017 Bernard Normier <bernard@zeroc.com> 0.9.18-2ice
- Fork of EPEL-7 packaging to create only static library and statically
  linked tools.

* Wed Feb 10 2016 Jan Stanek <jstanek@redhat.com> - 0.9.18-1
- Update to 0.9.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Jan Vcelak <jvcelak@fedoraproject.org> 0.9.17-2
- Make liblmdb.so a symbolic link to (not a copy of) the versioned DSO

* Thu Dec 03 2015 Jan Staněk <jstanek@redhat.com> - 0.9.17-1
- Update to 0.9.17

* Wed Nov 25 2015 Jan Staněk <jstanek@redhat.com> - 0.9.16-2
- Return the name 'Symas' into description

* Fri Aug 14 2015 Jan Staněk <jstanek@redhat.com> - 0.9.16-1
- Updated to 0.9.16

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 11 2014 Jan Staněk <jstanek@redhat.com> - 0.9.14-1
- Updated to 0.9.14

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Jan Stanek <jstanek@redhat.com> - 0.9.13-1
- Updated to 0.9.13

* Mon Jul 14 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-4
- Changed install instruction to be compatible with older coreutils (#1119084)

* Thu Jun 26 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-3
- Added delay in testing which was needed on s390* arches (#1104232)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Jan Stanek <jstanek@redhat.com> - 0.9.11-1
- Initial Package
