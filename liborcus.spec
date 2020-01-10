%global apiversion 0.8

# build conversion tools
%bcond_with convtools

Name: liborcus
Version: 0.7.0
Release: 6%{?dist}
Summary: Standalone file import filter library for spreadsheet documents

License: MPLv2.0
URL: https://gitlab.com/orcus/orcus
Source: http://kohei.us/files/orcus/src/%{name}-%{version}.tar.bz2

BuildRequires: boost-devel
BuildRequires: chrpath
%if %{with convtools}
BuildRequires: help2man
BuildRequires: pkgconfig(libixion-0.8)
%endif
BuildRequires: pkgconfig(mdds)
BuildRequires: pkgconfig(zlib)

Patch0: 0001-fix-invalid-memory-access-in-base64-functions.patch
Patch1: 0001-coverity-54426-missing-break-in-switch-statement.patch
Patch2: 0001-coverity-54448-Uninitialized-scalar-field.patch
Patch3: 0001-do-not-let-main-throw.patch

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

%prep
%autosetup -p1

%if %{without convtools}
%global condopts --disable-spreadsheet-model
%endif

%build
%configure --disable-debug --disable-silent-rules --disable-static \
    --disable-werror --with-pic %{?condopts}
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%if %{with convtools}
export LD_LIBRARY_PATH=`pwd`/src/liborcus/.libs:`pwd`/src/parser/.libs:`pwd`/src/spreadsheet/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
help2man -N -n 'convert a CSV file' -o orcus-csv.1 ./src/.libs/orcus-csv
help2man -N -n 'convert a Gnumeric file' -o orcus-gnumeric.1 ./src/.libs/orcus-gnumeric
help2man -N -n 'convert an ODF spreadsheet' -o orcus-ods.1 ./src/.libs/orcus-ods
help2man -N -n 'transform an XML file' -o orcus-xls-xml.1 ./src/.libs/orcus-xls-xml
help2man -N -n 'convert a OpenXML spreadsheet' -o orcus-xlsx.1 ./src/.libs/orcus-xlsx
help2man -N -n 'convert an XML file' -o orcus-xml.1 ./src/.libs/orcus-xml
%endif

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# because boost.m4 is total crap and adds RPATH unconditionally
chrpath -d %{buildroot}/%{_libdir}/*.so

%if %{with convtools}
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -p -m 0644 orcus-*.1 %{buildroot}/%{_mandir}/man1
%endif

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
%doc AUTHORS COPYING README
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
%{_bindir}/orcus-detect
%{_bindir}/orcus-mso-encryption
%{_bindir}/orcus-xml-dump
%{_bindir}/orcus-zip-dump
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

%changelog
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
