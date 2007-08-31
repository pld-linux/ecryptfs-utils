Summary:	The eCryptfs mount helper and support libraries
Name:		ecryptfs-utils
Version:	23
Release:	1
License:	GPL
Group:		Base
URL:		http://ecryptfs.sourceforge.net
Source0:	http://dl.sourceforge.net/ecryptfs/%{name}-%{version}.tar.bz2
# Source0-md5:	63ed7aa33edf074bb3abdba6271b4370
BuildRequires:	gpgme-devel
BuildRequires:	keyutils-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
Requires:	uname(version) >= 2.6.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
eCryptfs is a stacked cryptographic filesystem that ships in Linux
kernel versions 2.6.19 and above. This package provides the mount
helper and supporting libraries to perform key management and mount
functions.

Install ecryptfs-utils if you would like to mount eCryptfs.

%package devel
Summary:	The eCryptfs userspace development package
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	keyutils-devel
Requires:	openssl-devel
Requires:	pam-devel

%description devel
Userspace development files for eCryptfs.

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
	--disable-rpath

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING AUTHORS NEWS THANKS
%attr(755,root,root) /sbin/mount.ecryptfs
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libecryptfs.so.*
%{_libdir}/ecryptfs
%{_mandir}/man7/ecryptfs.7*

%files devel
%defattr(644,root,root,755)
%doc doc/design_doc/ecryptfs_design_doc_v0_2.tex doc/design_doc/*.eps
%attr(755,root,root) %{_libdir}/libecryptfs.so
%{_includedir}/ecryptfs.h

%files -n pam-pam_ecryptfs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_ecryptfs.so
