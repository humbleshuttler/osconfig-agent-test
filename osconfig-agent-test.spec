# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name: osconfig-agent-test
Version: %{_version}
Release: 1%{?dist}
Summary: Google osconfig agent test package.
License: ASL 2.0
Url: https://github.com/iamsubratp/osconfig-agent-test
Source0: %{name}_%{version}.orig.tar.gz

BuildArch: %{_arch}
%if 0%{?el7}
BuildRequires: systemd
%endif

%description
Contains the OSConfig agent test binary

%prep
%autosetup

%build
GOPATH=%{_gopath} CGO_ENABLED=0 %{_go} build -ldflags="-s -w -X main.version=%{_version}" -mod=readonly -o osconfig_agent_test

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 osconfig_agent_test %{buildroot}%{_bindir}/osconfig_agent_test
%if 0%{?el7}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_presetdir}
install -p -m 0644 %{name}.service %{buildroot}%{_unitdir}
install -p -m 0644 90-%{name}.preset %{buildroot}%{_presetdir}/90-%{name}.preset
%else
install -d %{buildroot}/etc/init
install -p -m 0644 %{name}.conf %{buildroot}/etc/init
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/osconfig_agent_test
%if 0%{?el7}
%{_unitdir}/%{name}.service
%{_presetdir}/90-%{name}.preset
%else
/etc/init/%{name}.conf
%endif

%post
%if 0%{?el6}
if [ $1 -eq 1 ]; then
  # Start the service on first install
  start -q -n osconfig-agent-test
fi
if [ $1 -eq 2 ]; then
  # Restart on upgrade
  restart -q -n osconfig-agent-test
fi
%endif

%if 0%{?el7}
%systemd_post osconfig-agent-test.service
if [ $1 -eq 1 ]; then
  # Start the service on first install
  systemctl start osconfig-agent-test.service
fi

%preun
%systemd_preun osconfig-agent-test.service

%postun
%systemd_postun_with_restart osconfig-agent-test.service

%endif