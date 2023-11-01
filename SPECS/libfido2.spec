Name:           libfido2

Version:        1.6.0
Release:        7%{?dist}
Summary:        FIDO2 library

License:        BSD
URL:            https://github.com/Yubico/%{name}
Source0:        https://developers.yubico.com/%{name}/Releases/%{name}-%{version}.tar.gz
Source1:        https://developers.yubico.com/%{name}/Releases/%{name}-%{version}.tar.gz.sig
Source2:        yubico-release-gpgkeys.asc
# Work around false positive from gcc-11 until its fixed upstream
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=97631
Patch0002:      %{name}-gcc11.patch
Patch0003:      %{name}-openssl30.patch

BuildRequires:  cmake
BuildRequires:  hidapi-devel
BuildRequires:  libcbor-devel
BuildRequires:  libudev-devel
BuildRequires:  openssl-devel
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
Requires:       (u2f-hidraw-policy if systemd-udev)

%description
%{name} is an open source library to support the FIDO2 protocol.  FIDO2 is
an open authentication standard that consists of the W3C Web Authentication
specification (WebAuthn API), and the Client to Authentication Protocol
(CTAP).  CTAP is an application layer protocol used for communication
between a client (browser) or a platform (operating system) with an external
authentication device (for example the Yubico Security Key).

################################################################################

%package devel

Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
%{name}-devel contains development libraries and header files for %{name}.

################################################################################

%package -n fido2-tools

Summary:        FIDO2 tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n fido2-tools
FIDO2 command line tools to access and configure a FIDO2 compliant
authentication device.

################################################################################


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n %{name}-%{version}


%build
%cmake
%cmake_build


%install
%cmake_install
# Remove static files per packaging guidelines
find %{buildroot} -type f -name "*.a" -delete -print


%files
%doc NEWS README.adoc
%license LICENSE
%{_libdir}/libfido2.so.1{,.*}

%files devel
%{_libdir}/pkgconfig/*
%{_libdir}/libfido2.so
%{_includedir}/*
%{_mandir}/man3/*

%files -n fido2-tools
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.6.0-7
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.6.0-6
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Fri Jun 04 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1.6.0-5
- rebuilt

* Tue May 25 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 1.6.0-4
- OpenSSL 3.0 compatibility. Related: rhbz#1961051

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.6.0-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.6.0-1
- 1.6.0 release (#1910101)

* Thu Dec 17 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-4
- Use gpgverify macro and ascii armored yubico release keys

* Wed Nov 04 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-3
- add BR make
- fix typo in changelog day (Tuu -> Thu) to make rpmlint happy

* Thu Oct 29 2020 Jeff Law <law@redhat.com> 1.5.0-2
- Work around false positive diagnostic in gcc-11

* Fri Sep 11 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.5.0-1
- 1.5.0 release (#1824326)
- include upstream patch to fix 32-bit platform compile, reported at
  https://github.com/Yubico/libfido2/issues/210

* Tue Sep 08 2020 Kalev Lember <klember@redhat.com> - 1.4.0-4
- Rebuilt for libcbor soname bump

* Wed Jul 29 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.4.0-3
- adapt to new Fedora cmake rpm macros

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 15 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.4.0-1
- 1.4.0 release (#1824326)

* Sat Apr 11 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.1-2
- change to require u2f-hidraw-policy only if systemd-udev (#1823002)

* Thu Feb 20 2020 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.1-1
- 1.3.1 release

* Mon Dec 16 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-3
- use yubico corp release site for sources and gpg signature

* Sat Dec 14 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-2
- packaging cleanups

* Sat Nov 30 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.3.0-1
- 1.3.0 release

* Mon Jul 29 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.2.0-1
- 1.2.0 release

* Sat May 11 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.1.0-1
- 1.1.0 release

* Fri Apr 05 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.0.0-2
- include backported upstream patches for compiler dependencies and soname version
- modify libdir glob to meet newer packaging recommendations

* Thu Mar 21 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 1.0.0-1
- 1.0.0 release

* Mon Jan 07 2019 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.4.0-1
- 0.4.0 release

* Wed Sep 12 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-1
- 0.3.0 release

* Fri Sep 07 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.8.20180907git878fcd8
- update to upstream master

* Thu Sep 06 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.7.20180906gitff7ece8
- update to upstream master

* Wed Sep 05 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.6.20180905gitcb4951c
- update to upstream master

* Tue Sep 04 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.5.20180904git2b5f0d0
- update to upstream master

* Mon Aug 27 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.4.20180827git9d178b2
- Update to upstream master

* Thu Aug 23 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.3.20180823git0f40181
- Update to upstream master

* Tue Aug 21 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.2.20180821gitfff65a4
- Update to upstream master

* Wed Aug 08 2018 Gary Buhrmaster <gary.buhrmaster@gmail.com> 0.3.0-0.1.20180808git5be8903
- Update to new spec

