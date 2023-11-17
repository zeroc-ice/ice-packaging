#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

Name: ice-repo
Version: 3.7
Summary: Dnf / yum repo configuration for ZeroC Ice
Release: 2%{?dist}
License: GPLv2 with exceptions
Vendor: ZeroC, Inc.
URL: https://zeroc.com/
Source0: https://download.zeroc.com/ice/%{version}/%{suffix:%{dist}}/zeroc-ice3.7.repo
Group: System Environment/Base
BuildArch: noarch

%description
This package installs the dnf / yum repo file for the ZeroC Ice RPC framework.

%prep
%setup -q -T -c

%install
/opt/freeware/bin/install -dm 755 %{buildroot}%{_sysconfdir}/yum/repos.d
/opt/freeware/bin/install -pm 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum/repos.d

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum/repos.d/*

%changelog
* Fri Nov 17 2023 Bernard Normier <bernard@zeroc.com> - 3.7-2
- Update repo file and description.
* Thu Sep 5 2019 Bernard Normier <bernard@zeroc.com> - 3.7-1
- AIX fork
* Thu Feb 28 2019 Bernard Normier <bernard@zeroc.com> - 3.7-1
- Initial package
