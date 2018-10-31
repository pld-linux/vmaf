# TODO:
# - python package
# - system libs if possible:
#   libsvm
#   wrapper/src/pugixml
#   ptools ?
#   ptools/opencontainers_1_8_4 ?
#
# Conditional build:
%bcond_with	sse2	# use SSE2 instructions

%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif
Summary:	Netflix's VMAF library
Summary(pl.UTF-8):	Biblioteka Netflix VMAF
Name:		vmaf
Version:	1.3.9
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/Netflix/vmaf/releases
Source0:	https://github.com/Netflix/vmaf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b5f39df007a66e6b6e284a820066bb70
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-shared.patch
URL:		https://github.com/Netflix/vmaf
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VMAF is a perceptual video quality assessment algorithm developed by
Netflix.

%description -l pl.UTF-8
VMAF to percepcyjny algorytm oceny jakości obrazu tworzony przez
Netfliksa.

%package libs
Summary:	Netflix VMAF libary
Summary(pl.UTF-8):	Biblioteka Netflix VMAF
Group:		Libraries

%description libs
Netflix VMAF libary.

%description libs -l pl.UTF-8
Biblioteka Netflix VMAF.

%package devel
Summary:	Netflix VMAF SDK
Summary(pl.UTF-8):	Pakiet programistyczny Netflix VMAF
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel >= 6:4.8

%description devel
Netflix VMAF SDK.

%description devel -l pl.UTF-8
Pakiet programistyczny Netflix VMAF.

%package static
Summary:	Static Netflix VMAF library
Summary(pl.UTF-8):	Statyczna biblioteka Netflix VMAF
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Netflix VMAF library.

%description static -l pl.UTF-8
Statyczna biblioteka Netflix VMAF.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%if %{without sse2}
%{__sed} -i -e 's,#define ADM_OPT_RECIP_DIVISION,/* & */,' feature/src/adm_options.h
%endif

%build
CFLAGS="%{rpmcflags}%{?with_sse2: -msse2}" \
CXXFLAGS="%{rpmcxxflags}%{?with_sse2: -msse2}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \

%{__sed} -i -e 's,^prefix=.*,prefix=%{_prefix},' \
	-e 's,^libdir=.*,libdir=%{_libdir},' \
	-e 's,^includedir=.*,includedir=%{_includedir},' wrapper/libvmaf.pc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} -C wrapper install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

install feature/{psnr,vmaf} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md FAQ.md NOTICE.md README.md VERSION
%attr(755,root,root) %{_bindir}/psnr
%attr(755,root,root) %{_bindir}/vmaf
%{_datadir}/model

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmaf.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmaf.so
%{_includedir}/libvmaf.h
%{_pkgconfigdir}/libvmaf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvmaf.a
