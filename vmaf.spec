# TODO:
# - python package
# - system libs if possible:
#   libvmaf/src/third_party/ptools
#   libvmaf/src/third_party/ptools/opencontainers_1_8_4
#   libvmaf/src/third_party/pugixml
#   third_party/libsvm
#
# Conditional build:
%bcond_with	sse2	# use SSE2 instructions

%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif
Summary:	Netflix's VMAF library
Summary(pl.UTF-8):	Biblioteka Netflix VMAF
Name:		vmaf
Version:	1.5.3
Release:	1
License:	BSD+patent
Group:		Libraries
#Source0Download: https://github.com/Netflix/vmaf/releases
Source0:	https://github.com/Netflix/vmaf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	73914f1bc2e15a82162549f1eba735fa
Patch0:		%{name}-x86-nosimd.patch
URL:		https://github.com/Netflix/vmaf
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	meson >= 0.47.0
BuildRequires:	ninja >= 1.5
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
%if %{with sse2}
Requires:	cpuinfo(sse2)
%endif

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

%if %{without sse2}
%{__sed} -i -e 's,#define ADM_OPT_RECIP_DIVISION,/* & */,' libvmaf/src/feature/adm_options.h
%endif

%build
%if %{with sse2}
CFLAGS="%{rpmcflags} -msse2"
CXXFLAGS="%{rpmcxxflags} -msse2"
%endif
%meson build-libvmaf libvmaf

%ninja_build -C build-libvmaf

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build-libvmaf

install build-libvmaf/tools/{vmaf_feature,vmaf_rc} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%triggerpostun libs -- vmaf-libs < 1.5.2
# replace library file with soname symlink
rm -f %{_libdir}/libvmaf.so.0
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md FAQ.md LICENSE NOTICE.md README.md VERSION
%attr(755,root,root) %{_bindir}/vmaf_feature
%attr(755,root,root) %{_bindir}/vmaf_rc
%attr(755,root,root) %{_bindir}/vmafossexec
%{_datadir}/model

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmaf.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libvmaf.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmaf.so
%{_includedir}/libvmaf
%{_pkgconfigdir}/libvmaf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvmaf.a
