# TODO:
# - shared library
# - python package
# - optflags
# - system libs if possible:
#   libsvm
#   wrapper/src/pugixml
#   ptools ?
#   ptools/opencontainers_1_8_4 ?
Summary:	Netflix's VMAF library
Summary(pl.UTF-8):	Biblioteka Netflix VMAF
Name:		vmaf
Version:	1.3.1
Release:	0.1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/Netflix/vmaf/releases
Source0:	https://github.com/Netflix/vmaf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	864c2c74649fd8770fd6a566fdaf6f35
URL:		https://github.com/Netflix/vmaf
BuildRequires:	libstdc++-devel >= 6:4.8
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VMAF is a perceptual video quality assessment algorithm developed by
Netflix.

#%description -l pl.UTF-8

%package devel
Summary:	Netflix VMAF SDK
Summary(pl.UTF-8):	Pakiet programistyczny Netflix VMAF
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:4.8

%description devel
Netflix VMAF SDK.

%description devel -l pl.UTF-8
Pakiet programistyczny Netflix VMAF.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \

%{__sed} -i -e 's,^prefix=.*,prefix=%{_prefix},' \
	-e 's,^libdir=.*,libdir=%{_libdir},' \
	-e 's,^includedir=.*,includedir=%{_includedir},' wrapper/libvmaf.pc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md FAQ.md NOTICE.md README.md VERSION
%{_datadir}/model

%files devel
%defattr(644,root,root,755)
%{_libdir}/libvmaf.a
%{_includedir}/libvmaf.h
%{_pkgconfigdir}/libvmaf.pc
