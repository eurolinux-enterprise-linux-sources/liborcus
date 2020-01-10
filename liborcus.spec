%global apiversion 0.6

Name: liborcus
Version: 0.5.1
Release: 7%{?dist}
Summary: Standalone file import filter library for spreadsheet documents

Group: System Environment/Libraries
License: MIT
URL: http://gitorious.org/orcus
Source: http://kohei.us/files/orcus/src/%{name}-%{version}.tar.bz2

BuildRequires: boost-devel
BuildRequires: zlib-devel

Patch0: add-aarch64.patch

%description
%{name} is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary: Tools for working with %{name}
Group: Applications/Publishing
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools for working with %{name}.

%prep
%setup -q
%patch0 -p1
# fix build of orcus-zip-dump
sed -i -e 's/orcus_zip_dump_LDADD = /& $(BOOST_SYSTEM_LIB) /' \
    src/Makefile.in
# TODO: upstream the changes
sed -i \
    -e 's/[a-z_]*_test_LDADD = /& $(BOOST_SYSTEM_LIB) /' \
    -e 's/parser_test_[a-z_]*_LDADD = /& $(BOOST_SYSTEM_LIB) /' \
    -e 's/liborcus_test_xml_structure_tree_LDADD = /& $(BOOST_SYSTEM_LIB) /' \
    src/liborcus/Makefile.in src/parser/Makefile.in

%build
# TODO spreadsheet-model requires ixion
%configure --disable-debug --disable-silent-rules --disable-static \
    --disable-werror --with-pic \
    --disable-spreadsheet-model
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la

%check
export LD_LIBRARY_PATH=`pwd`/src/liborcus/.libs:`pwd`/src/parser/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-mso-%{apiversion}.so.*
%{_libdir}/%{name}-parser-%{apiversion}.so.*

%files devel
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/%{name}-mso-%{apiversion}.so
%{_libdir}/%{name}-parser-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc

%files tools
%{_bindir}/orcus-mso-encryption
%{_bindir}/orcus-xml-dump
%{_bindir}/orcus-zip-dump

%changelog
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
