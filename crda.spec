%define         crda_version    1.1.1
%define         regdb_version   2009.11.25

Name:           crda
Version:        %{crda_version}_%{regdb_version}
Release:        3%{?dist}
Summary:        Regulatory compliance daemon for 802.11 wireless networking

Group:          System Environment/Base
License:        ISC
URL:            http://www.linuxwireless.org/en/developers/Regulatory/CRDA
BuildRoot:      %{_tmppath}/%{name}-%{crda_version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kernel-headers >= 2.6.27
BuildRequires:  libnl-devel >= 1.1
BuildRequires:  libgcrypt-devel
BuildRequires:  pkgconfig python m2crypto

Requires:       udev, iw

Source0:        http://wireless.kernel.org/download/crda/crda-%{crda_version}.tar.bz2
Source1:        http://wireless.kernel.org/download/wireless-regdb/wireless-regdb-%{regdb_version}.tar.bz2
Source2:        setregdomain
Source3:        setregdomain.1

# Add udev rule to call setregdomain on wireless device add
Patch0:         regulatory-rules-setregdomain.patch


%description
CRDA acts as the udev helper for communication between the kernel
and userspace for regulatory compliance. It relies on nl80211
for communication. CRDA is intended to be run only through udev
communication from the kernel.


%prep
%setup -q -c
%setup -q -T -D -a 1

%patch0 -p1 -b .setregdomain


%build

# Use our own signing key to generate regulatory.bin
cd wireless-regdb-%{regdb_version}

make %{?_smp_mflags} CFLAGS="%{optflags}" maintainer-clean
make %{?_smp_mflags} CFLAGS="%{optflags}" REGDB_PRIVKEY=key.priv.pem REGDB_PUBKEY=key.pub.pem

# Build CRDA using the new key and regulatory.bin from above
cd ../crda-%{crda_version}
cp ../wireless-regdb-%{regdb_version}/key.pub.pem pubkeys

make %{?_smp_mflags} CFLAGS="%{optflags}" REG_BIN=../wireless-regdb-%{regdb_version}/regulatory.bin


%install
rm -rf %{buildroot}

cd crda-%{crda_version}
cp README README.crda
make install DESTDIR=%{buildroot} PREFIX='' MANDIR=%{_mandir}

cd ../wireless-regdb-%{regdb_version}
cp README README.wireless-regdb
make install DESTDIR=%{buildroot} PREFIX='' MANDIR=%{_mandir}

install -D -pm 0755 %SOURCE2 %{buildroot}/sbin
install -D -pm 0644 %SOURCE3 %{buildroot}%{_mandir}/man1/setregdomain.1


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/sbin/%{name}
/sbin/regdbdump
/sbin/setregdomain
/lib/udev/rules.d/85-regulatory.rules
# location of database is hardcoded to /lib/%{name}
/lib/%{name}
%{_mandir}/man1/setregdomain.1*
%{_mandir}/man5/regulatory.bin.5*
%{_mandir}/man8/crda.8*
%{_mandir}/man8/regdbdump.8*
%doc crda-%{crda_version}/LICENSE crda-%{crda_version}/README.crda
%doc wireless-regdb-%{regdb_version}/README.wireless-regdb


%changelog
* Thu Feb 25 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-3
- Correct license tag from BSD to ISC
- Comment purpose of regulatory-rules-setregdomain.patch
- Add copyright and license statement to setregdomain
- Add comment for why /lib is hardcoded in files section
- Reformat Dec 21 2009 changelog entry so rpmlint stops complaining

* Tue Jan 26 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-2
- Change RPM_OPT_FLAGS to optflags
- Leave man page compression to rpmbuild
- Correct date in previous changelog entry

* Tue Jan 26 2010 John W. Linville <linville@redhat.com> 1.1.1_2009.11.25-1
- Update for crda version 1.1.1

* Tue Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-5
- Remove unnecessary explicit Requries for libgcrypt and libnl -- oops!

* Tue Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-4
- Add libgcrypt and libnl to Requires

* Mon Dec 21 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-3
- Add man page for setregdomain (from Andrew Hecox <ahecox@redhat.com>)
- Change $RPM_BUILD_ROOT to buildroot

* Fri Dec 18 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-2
- Specify path to iw in setregdomain

* Wed Dec  2 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.25-1
- Update wireless-regdb to version 2009.11.25 

* Wed Nov 11 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.11.10-1
- Update wireless-regdb to version 2009.11.10 

* Wed Oct  1 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-3
- Move regdb to /lib/crda to facilitate /usr mounted over wireless network

* Wed Sep  9 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-2
- Use kernel-headers instead of kernel-devel

* Wed Sep  9 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.09.08-1
- Update wireless-regdb to version 2009.09.08 
- Start resetting release number with version updates

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0_2009.04.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 13 2009 John W. Linville <linville@redhat.com> 1.1.0_2009.04.17-11
- Update crda version to version 1.1.0
- Update wireless-regdb to version 2009.04.17 

* Fri Apr 17 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.04.16-10
- Update wireless-regdb version to pick-up recent updates and fixes (#496392)

* Tue Mar 31 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-9
- Add Requires line for iw package (#492762)
- Update setregdomain script to correctly check if COUNTRY is set

* Thu Mar 19 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-8
- Add setregdomain script to set regulatory domain based on timezone
- Expand 85-regulatory.rules to invoke setregdomain script on device add

* Tue Mar 10 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.03.09-7
- Update wireless-regdb version to pick-up recent updates and fixes (#489560)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1_2009.01.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.01.30-5
- Recognize regulatory.bin files signed with the upstream key (#484982)

* Tue Feb 03 2009 John W. Linville <linville@redhat.com> 1.0.1_2009.01.30-4
- Change version to reflect new wireless-regdb upstream release practices
- Update wireless-regdb version to pick-up recent updates and fixes (#483816)

* Tue Jan 27 2009 John W. Linville <linville@redhat.com> 1.0.1_2009_01_15-3
- Update for CRDA verion 1.0.1
- Account for lack of "v" in upstream release tarball naming
- Add patch to let wireless-regdb install w/o being root

* Thu Jan 22 2009 John W. Linville <linville@redhat.com> v0.9.5_2009_01_15-2
- Revamp based on package review comments

* Tue Jan 20 2009 John W. Linville <linville@redhat.com> v0.9.5_2009_01_15-1
- Initial build
