%global apiversion 0.12

# build conversion tools
%bcond_with convtools
# build python3 bindings
%bcond_with python

Name: liborcus
Version: 0.12.1
Release: 2%{?dist}
Summary: Standalone file import filter library for spreadsheet documents

License: MPLv2.0
URL: https://gitlab.com/orcus/orcus
Source0: http://kohei.us/files/orcus/src/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
%if %{with convtools}
BuildRequires: help2man
BuildRequires: pkgconfig(libixion-0.12)
%endif
BuildRequires: pkgconfig(mdds-1.2)
%if %{with python}
BuildRequires: pkgconfig(python3)
%endif
BuildRequires: pkgconfig(zlib)

Patch0: 0001-Wtautological-compare-compare-against-the-other-para.patch

%description
%{name} is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%if %{with convtools}
%package model
Summary: Spreadsheet model for %{name} conversion tools
Requires: %{name}%{?_isa} = %{version}-%{release}

%description model
The %{name}-model package contains a spreadsheet model used by the
conversion tools.
%endif

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary: Tools for working with %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Helper tools for %{name} and converters of various file formats to HTML
and text.

%if %{with python}
%package python3
Summary: Python 3 bindings for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description python3
Python 3 bindings for %{name}.
%endif

%package doc
Summary: API documentation for %{name}
BuildArch: noarch

%description doc
API documentation for %{name}.

%prep
%autosetup -p1

%if %{without convtools}
%global condopts %{?condopts} --disable-spreadsheet-model
%endif
%if %{without python}
%global condopts %{?condopts} --disable-python
%endif

%build
%configure --disable-debug --disable-silent-rules --disable-static \
    --disable-werror --with-pic %{?condopts}
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{python3_sitearch}/*.la

%if %{with convtools}
# create and install man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -S '%{name} %{version}' -n 'convert a CSV file' -o orcus-csv.1 %{buildroot}/usr/bin/orcus-csv
help2man -N -S '%{name} %{version}' -n 'convert a Gnumeric file' -o orcus-gnumeric.1 %{buildroot}/usr/bin/orcus-gnumeric
help2man -N -S '%{name} %{version}' -n 'convert an ODF spreadsheet' -o orcus-ods.1 %{buildroot}/usr/bin/orcus-ods
help2man -N -S '%{name} %{version}' -n 'transform an XML file' -o orcus-xls-xml.1 %{buildroot}/usr/bin/orcus-xls-xml
help2man -N -S '%{name} %{version}' -n 'convert a OpenXML spreadsheet' -o orcus-xlsx.1 %{buildroot}/usr/bin/orcus-xlsx
help2man -N -S '%{name} %{version}' -n 'convert an XML file' -o orcus-xml.1 %{buildroot}/usr/bin/orcus-xml
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -p -m 0644 orcus-*.1 %{buildroot}/%{_mandir}/man1
%endif

# build documentation
make doc-doxygen

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if %{with convtools}
%post model -p /sbin/ldconfig
%postun model -p /sbin/ldconfig
%endif

%files
%doc AUTHORS CHANGELOG
%license LICENSE
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-mso-%{apiversion}.so.*
%{_libdir}/%{name}-parser-%{apiversion}.so.*

%if %{with convtools}
%files model
%{_libdir}/%{name}-spreadsheet-model-%{apiversion}.so.*
%endif

%files devel
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/%{name}-mso-%{apiversion}.so
%{_libdir}/%{name}-parser-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%if %{with convtools}
%{_libdir}/%{name}-spreadsheet-model-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-spreadsheet-model-%{apiversion}.pc
%endif

%files tools
%{_bindir}/orcus-css-dump
%{_bindir}/orcus-detect
%{_bindir}/orcus-json
%{_bindir}/orcus-mso-encryption
%{_bindir}/orcus-xml-dump
%{_bindir}/orcus-zip-dump
%{_bindir}/orcus-yaml
%if %{with convtools}
%{_bindir}/orcus-csv
%{_bindir}/orcus-gnumeric
%{_bindir}/orcus-ods
%{_bindir}/orcus-xls-xml
%{_bindir}/orcus-xlsx
%{_bindir}/orcus-xml
%{_mandir}/man1/orcus-csv.1*
%{_mandir}/man1/orcus-gnumeric.1*
%{_mandir}/man1/orcus-ods.1*
%{_mandir}/man1/orcus-xls-xml.1*
%{_mandir}/man1/orcus-xlsx.1*
%{_mandir}/man1/orcus-xml.1*
%endif

%if %{with python}
%files python3
%{python3_sitearch}/_orcus.so
%{python3_sitearch}/_orcus_json.so
%{python3_sitelib}/orcus
%endif

%files doc
%license LICENSE
%doc doc/_doxygen/html

%changelog
* Fri Oct 20 2017 David Tardon <dtardon@redhat.com> - 0.12.1-2
- Related: rhbz#1477101 fix problem found by coverity

* Mon Sep 18 2017 David Tardon <dtardon@redhat.com> - 0.12.1-1
- Resolves: rhbz#1477101 rebase to 0.12.1

* Mon May 04 2015 David Tardon <dtardon@redhat.com> - 0.7.0-6
- Related: rhbz#1207772 add some upstream fixes

* Fri Apr 17 2015 David Tardon <dtardon@redhat.com> - 0.7.0-5
- Resolves: rhbz#1207772 rebase to 0.7.0

* Tue Aug 19 2014 David Tardon <dtardon@redhat.com> - 0.5.1-8
- Resolves: rhbz#1125584 fix build on ppc64le

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.5.1-7
- Mass rebuild 2014-01-24

* Tue Jan 21 2014 David Tardon <dtardon@redhat.com> - 0.5.1-6
- Resolves: rhbz#1041331 liborcus fails to build for ARM (Aarch64)
  (really this time)

* Tue Jan 21 2014 David Tardon <dtardon@redhat.com> - 0.5.1-5
- Resolves: rhbz#1041331 liborcus fails to build for ARM (Aarch64)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.5.1-4
- Mass rebuild 2013-12-27

* Mon Jun 10 2013 David Tardon <dtardon@redhat.com> - 0.5.1-3
- trivial changes

* Tue May 28 2013 David Tardon <dtardon@redhat.com> - 0.5.1-2
- build orcus-zip-dump too

* Mon May 06 2013 David Tardon <dtardon@redhat.com> - 0.5.1-1
- new release

* Fri Feb 15 2013 Stephan Bergmannn <sbergman@redhat.com> - 0.3.0-5
- missing boost include

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.3.0-4
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.3.0-3
- Rebuild for Boost-1.53.0

* Sat Dec 08 2012 David Tardon <dtardon@redhat.com> - 0.3.0-2
- a pointless release bump

* Fri Dec 07 2012 David Tardon <dtardon@redhat.com> - 0.3.0-1
- new release

* Sun Sep 09 2012 David Tardon <dtardon@redhat.com> - 0.1.0-1
- initial import
