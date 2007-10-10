Summary:	The eCryptfs mount helper and support libraries
Summary(pl.UTF-8):	Narzędzie pomocnicze i biblioteki do montowania eCryptfs
Name:		ecryptfs-utils
Version:	26
Release:	1
License:	GPL v2+
Group:		Base
Source0:	http://dl.sourceforge.net/ecryptfs/%{name}-%{version}.tar.bz2
# Source0-md5:	9d756cebe6301c560a98ac46f79734fa
URL:		http://ecryptfs.sourceforge.net/
BuildRequires:	gpgme-devel
BuildRequires:	keyutils-devel >= 1.0
BuildRequires:	libgcrypt-devel
# missing plugin source
#BuildRequires:        opencryptoki-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-tools-pod
BuildRequires:	trousers-devel
Requires:	uname(release) >= 2.6.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eCryptfs is a stacked cryptographic filesystem that ships in Linux
kernel versions 2.6.19 and above. This package provides the mount
helper and supporting libraries to perform key management and mount
functions.

Install ecryptfs-utils if you would like to mount eCryptfs.

%description -l pl.UTF-8
eCryptfs to stakowalny kryptograficzny system plików dostępny w jądrze
Linuksa od wersji 2.6.19. Ten pakiet udostępnia narzędzie pomocnicze
dla programu mount oraz wspierające je biblioteki wykonujące
zarządzanie kluczami i funkcje związane z montowaniem.

Pakiet ecryptfs-utils należy zainstalować, aby montować eCryptfs.

%package devel
Summary:	The eCryptfs userspace development package
Summary(pl.UTF-8):	Pakiet programistyczny przestrzeni użytkownika dla eCryptfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	keyutils-devel
Requires:	libgcrypt-devel

%description devel
Userspace development files for eCryptfs.

%description devel -l pl.UTF-8
Pliki programistyczne przestrzeni użytkownika dla eCryptfs.

%package static
Summary:	Static eCryptfs library
Summary(pl.UTF-8):	Statyczna biblioteka eCryptfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static eCryptfs library.

%description static -l pl.UTF-8
Statyczna biblioteka eCryptfs.

%package -n pam-pam_ecryptfs
Summary:	A PAM module - ecryptfs
Summary(pl.UTF-8):	Moduł PAM ecryptfs
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_ecryptfs
A PAM module - ecryptfs.

%description -n pam-pam_ecryptfs -l pl.UTF-8
Moduł PAM ecryptfs.

%prep
%setup -q

%build
%configure \
	--disable-opencryptoki \
	--enable-openssl \
	--enable-tspi \
	--enable-gpg \
	--enable-pam \
	--disable-rpath

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -D doc/manpage/ecryptfs-manager.8 $RPM_BUILD_ROOT%{_mandir}/man8/ecryptfs-manager.8
install -D doc/manpage/ecryptfsd.8 $RPM_BUILD_ROOT%{_mandir}/man8/ecryptfsd.8
install -D doc/manpage/mount.ecryptfs.8 $RPM_BUILD_ROOT%{_mandir}/man8/mount.ecryptfs.8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS doc/ecryptfs-faq.html
%attr(755,root,root) /sbin/mount.ecryptfs
%attr(755,root,root) %{_bindir}/ecryptfs-*
%attr(755,root,root) %{_bindir}/ecryptfsd
%attr(755,root,root) %{_libdir}/libecryptfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecryptfs.so.0
%dir %{_libdir}/ecryptfs
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_gpg.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_openssl.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_passphrase.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_tspi.so
%{_mandir}/man7/ecryptfs.7*
%{_mandir}/man8/ecryptfs-*.8*
%{_mandir}/man8/ecryptfsd.8*
%{_mandir}/man8/mount.ecryptfs.8*

%files devel
%defattr(644,root,root,755)
%doc doc/design_doc/ecryptfs_design_doc_v0_2.tex doc/design_doc/*.eps
%attr(755,root,root) %{_libdir}/libecryptfs.so
%{_libdir}/libecryptfs.la
%{_includedir}/ecryptfs.h
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libecryptfs.a

%files -n pam-pam_ecryptfs
%defattr(644,root,root,755)
%doc doc/ecryptfs-pam-doc.txt
%attr(755,root,root) /%{_lib}/security/pam_ecryptfs.so
