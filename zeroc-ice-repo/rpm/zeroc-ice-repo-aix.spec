#
# Copyright (c) ZeroC, Inc. All rights reserved.
#

Name: zeroc-ice-repo
Version: 3.7
Summary: Yum repo configuration for ZeroC Ice
Release: 1%{?dist}
License: GPLv2 with exceptions
Vendor: ZeroC, Inc.
URL: https://zeroc.com
Source0: https://zeroc.com/download/ice/%{version}/%{suffix:%{dist}}/zeroc-ice3.7.repo
Group: System Environment/Base
BuildArch: noarch

%description
This package installs the yum repo file for the ZeroC Ice RPC framework.

%prep
%setup -q -T -c

%install
mkdir -p %{buildroot}%{_sysconfdir}/yum/repos.d
installbsd -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum/repos.d

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum/repos.d/*

%changelog
* Thu Sep 5 2019 Bernard Normier <bernard@zeroc.com> - 3.7-1
- AIX fork
* Thu Feb 28 2019 Bernard Normier <bernard@zeroc.com> - 3.7-1
- Initial package
