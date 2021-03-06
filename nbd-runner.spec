%global _hardened_build 1

# without glusterfs dependency
# if you wish to exclude gluster handler in RPM, use below command
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without gluster
%{?_without_gluster:%global _without_gluster --with-gluster=no}

# without tirpc dependency
# if you wish to build without tirpc library, use below command
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without tirpc
%{?_without_tirpc:%global _without_tirpc --with-tirpc=no}

%if ( 0%{?fedora} && 0%{?fedora} <= 27 ) || ( 0%{?rhel} && 0%{?rhel} <= 7 )
%global _without_tirpc --with-tirpc=no
%endif

Name:          nbd-runner
Summary:       A daemon that handles the NBD device's IO requests in server side
Group:         System Environment/Daemons
License:       ASL 2.0 or LGPLv2+
Version:       0.3
URL:           https://github.com/gluster/nbd-runner.git

Release:       rc1%{?dist}
BuildRoot:     %(mktemp -udp %{_tmppath}/%{name}-%{version}%)
Source:        %{name}-%{version}.tar.gz
ExclusiveOS:   Linux

BuildRequires: autoconf automake libtool kmod-devel libnl3-devel libevent-devel glib2-devel json-c-devel

%if ( 0%{!?_without_tirpc:1} )
BuildRequires: libtirpc-devel rpcgen
Requires:      libtirpc
%endif

Requires:      kmod, libevent, libnl3, glib2, json-c, rsyslog

%description
A daemon that handles the userspace side of the NBD(Network Block Device) backstore.

%if ( 0%{!?_without_gluster:1} )
%package gluster-handler
Summary:       Gluster backstore handler
BuildRequires: glusterfs-api-devel
Requires:      glusterfs-api
Requires:      %{name} = %{version}-%{release}

%description gluster-handler
Gluster backend handler for processing IO requests from the NBD device.
%endif

%global debug_package %{nil}

%prep
%setup -q -n %{name}-%{version}

%build
./autogen.sh
%configure %{?_without_tirpc} %{?_without_gluster}

%install
%{__make} DESTDIR=%{buildroot} install

%files
%{_sbindir}/nbd-runner
%{_sbindir}/nbd-cli
%{_unitdir}/nbd-runner.service
%doc README.md COPYING-GPLV2 COPYING-LGPLV3
%config(noreplace) %{_sysconfdir}/sysconfig/nbd-runner

%if ( 0%{!?_without_gluster:1} )
%files gluster-handler
%dir %{_libdir}/nbd-runner/
%{_libdir}/nbd-runner/libgluster_handler.*
%endif

%changelog
* Wed Apr 24 2019 Xiubo Li <xiubli@redhat.com> - 0.3
- Initial spec file
