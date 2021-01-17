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
Version:	2.1.0
Release:	1
License:	BSD+patent
Group:		Libraries
#Source0Download: https://github.com/Netflix/vmaf/releases
Source0:	https://github.com/Netflix/vmaf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a65e105a67008796d566e9cc38e8e0fe
Patch0:		%{name}-x32.patch
URL:		https://github.com/Netflix/vmaf
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	meson >= 0.47.0
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm >= 2.14
%endif
BuildRequires:	ninja >= 1.7.1
BuildRequires:	python3 >= 1:3.6
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

%{__mv} libvmaf/README.md libvmaf/README.libvmaf.md

%if %{without sse2}
%{__sed} -i -e 's,#define ADM_OPT_RECIP_DIVISION,/* & */,' libvmaf/src/feature/adm_options.h
%endif

%build
%if %{with sse2}
# SSE2 requires global support
CFLAGS="%{rpmcflags} -msse2"
CXXFLAGS="%{rpmcxxflags} -msse2"
%endif

# AVX512 is (properly) runtime detected (but SSE2 is probably prerequisite)
%meson build-libvmaf libvmaf \
%if %{with sse2}
	-Denable_avx512=true
%endif

%ninja_build -C build-libvmaf

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build-libvmaf

install build-libvmaf/tools/vmafossexec $RPM_BUILD_ROOT%{_bindir}

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
%doc libvmaf/tools/README.md
%attr(755,root,root) %{_bindir}/vmaf
%attr(755,root,root) %{_bindir}/vmafossexec

%files libs
%defattr(644,root,root,755)
%doc CHANGELOG.md FAQ.md LICENSE README.md libvmaf/README.libvmaf.md
%attr(755,root,root) %{_libdir}/libvmaf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvmaf.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvmaf.so
%{_includedir}/libvmaf
%{_pkgconfigdir}/libvmaf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvmaf.a
