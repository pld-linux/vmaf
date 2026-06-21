# TODO:
# - enable_cuda, enable_nvtx on bcond
# - python package
#
# Conditional build:
%bcond_with	sse2	# use SSE2 instructions

%ifarch pentium4 %{x8664} x32
%define	with_sse2	1
%endif
Summary:	Netflix's VMAF library
Summary(pl.UTF-8):	Biblioteka Netflix VMAF
Name:		vmaf
Version:	3.2.0
Release:	1
License:	BSD+patent
Group:		Libraries
#Source0Download: https://github.com/Netflix/vmaf/releases
Source0:	https://github.com/Netflix/vmaf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ed5fdf1fe4acf1edfab46f14affb58e2
Patch0:		%{name}-x32.patch
URL:		https://github.com/Netflix/vmaf
BuildRequires:	gcc >= 6:4.8
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	meson >= 0.56.1
%ifarch %{ix86} %{x8664} x32
BuildRequires:	nasm >= 2.14
%endif
BuildRequires:	ninja >= 1.7.1
BuildRequires:	python3 >= 1:3.6
BuildRequires:	rpmbuild(macros) >= 2.042
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
%patch -P0 -p1

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

%define _vpath_srcdir	libvmaf
# AVX512 is (properly) runtime detected (but SSE2 is probably prerequisite)
%meson \
%if %{with sse2}
	-Denable_avx512=true
%endif

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

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

%files libs
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md libvmaf/README.libvmaf.md
%{_libdir}/libvmaf.so.*.*.*
%ghost %{_libdir}/libvmaf.so.3

%files devel
%defattr(644,root,root,755)
%{_libdir}/libvmaf.so
%{_includedir}/libvmaf
%{_pkgconfigdir}/libvmaf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvmaf.a
