#
# Conditional build:
%bcond_with	gui		# GTK+ GUI components (non-existing as of 111)
%bcond_without	static_libs	# static library
#
Summary:	The eCryptfs mount helper and support libraries
Summary(pl.UTF-8):	Narzędzie pomocnicze i biblioteki do montowania eCryptfs
Name:		ecryptfs-utils
Version:	111
Release:	5
License:	GPL v2+
Group:		Base
#Source0Download: https://launchpad.net/ecryptfs/+download
Source0:	https://launchpad.net/ecryptfs/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
# Source0-md5:	83513228984f671930752c3518cac6fd
Patch0:		%{name}-sh.patch
Patch1:		%{name}-83-fixsalt.patch
Patch2:		%{name}-83-splitnss.patch
Patch3:		%{name}-84-fixsigness.patch
Patch4:		openssl.patch
Patch5:		%{name}-types.patch
URL:		http://ecryptfs.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gpgme-devel
%{?with_gui:BuildRequires:	gtk+2-devel >= 2.0}
BuildRequires:	intltool >= 0.41.0
BuildRequires:	keyutils-devel >= 1.0
BuildRequires:	libtool
BuildRequires:	nss-devel >= 3
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkcs11-helper-devel >= 1.04
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig >= 1.3.31
BuildRequires:	swig-python >= 1.3.31
BuildRequires:	trousers-devel
Requires:	uname(release) >= 2.6.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# python module
%define		skip_post_check_so	_libecryptfs.so.0.0.0

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
Requires:	keyutils-devel >= 1.0
Requires:	nss-devel >= 3

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
Summary:	eCryptfs PAM module
Summary(pl.UTF-8):	Moduł PAM eCryptfs
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_ecryptfs
eCryptfs PAM module.

%description -n pam-pam_ecryptfs -l pl.UTF-8
Moduł PAM eCryptfs.

%package -n python-ecryptfs
Summary:	Python bindings for the eCryptfs utils
Summary(pl.UTF-8):	Wiązania Pythona do narzędzi eCryptfs
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ecryptfs-utils-python < 85-2

%description -n python-ecryptfs
This package contains a module that permits applications written in
the Python programming language to use the interface supplied by the
ecryptfs-utils library.

%description -n python-ecryptfs -l pl.UTF-8
Ten pakiet zawiera moduł pozwalający aplikacjom napisanym w Pythonie
na korzystanie z interfejsu dostarczanego przez bibliotekę
ecryptfs-utils.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python} \
	--enable-gpg \
	%{?with_gui:--enable-gui} \
	--enable-nss \
	--enable-openssl \
	--enable-pam \
	--enable-pkcs11-helper \
	--enable-tspi \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libecryptfs.la

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/%{name}/_libecryptfs.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{py_sitedir}/%{name}/_libecryptfs.a}
%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 260 ecryptfs

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
        %groupremove ecryptfs
fi

%post	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS doc/{ecryptfs-faq.html,ecryptfs-pkcs11-helper-doc.txt}
%attr(755,root,root) /sbin/mount.ecryptfs
%attr(4754,root,ecryptfs) /sbin/mount.ecryptfs_private
%attr(755,root,root) /sbin/umount.ecryptfs_private
%attr(755,root,root) /sbin/umount.ecryptfs
%attr(755,root,root) %{_bindir}/ecryptfs-*
%attr(755,root,root) %{_bindir}/ecryptfsd
%attr(755,root,root) %{_libdir}/libecryptfs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libecryptfs.so.1
%dir %{_libdir}/ecryptfs
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_gpg.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_openssl.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_passphrase.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_pkcs11_helper.so
%attr(755,root,root) %{_libdir}/ecryptfs/libecryptfs_key_mod_tspi.so
%{_datadir}/%{name}
%{_mandir}/man1/ecryptfs-*.1*
%{_mandir}/man1/mount.ecryptfs_private.1*
%{_mandir}/man1/umount.ecryptfs_private.1*
%{_mandir}/man7/ecryptfs.7*
%{_mandir}/man8/ecryptfs-*.8*
%{_mandir}/man8/ecryptfsd.8*
%{_mandir}/man8/mount.ecryptfs.8*
%{_mandir}/man8/umount.ecryptfs.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libecryptfs.so
%{_includedir}/ecryptfs.h
%{_pkgconfigdir}/libecryptfs.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libecryptfs.a
%endif

%files -n pam-pam_ecryptfs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_ecryptfs.so
%{_mandir}/man8/pam_ecryptfs.8*

%files -n python-ecryptfs
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/_libecryptfs.so*
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
