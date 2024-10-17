Name:           ocaml-augeas
Version:        0.4
Release:        %mkrel 1
Summary:        OCaml bindings for Augeas configuration API
License:        LGPLv2+ with exceptions
Group:          Development/Other
URL:            https://et.redhat.com/~rjones/augeas/files/
Source0:        http://et.redhat.com/~rjones/augeas/files/ocaml-augeas-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  augeas-devel >= 0.1.0
BuildRequires:  chrpath

%description
Augeas is a unified system for editing arbitrary configuration
files. This provides complete OCaml bindings for Augeas.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure
make
make doc

%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

# The upstream 'make install' rule is missing '*.so' and distributes
# '*.cmi' instead of just the augeas.cmi file.  Temporary fix:
#make install
ocamlfind install augeas META *.mli *.cmx *.cma *.cmxa *.a augeas.cmi *.so

strip $OCAMLFIND_DESTDIR/stublibs/dll*.so
chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING.LIB
%dir %{_libdir}/ocaml/augeas
%{_libdir}/ocaml/augeas/META
%{_libdir}/ocaml/augeas/*.cma
%{_libdir}/ocaml/augeas/*.cmi
%{_libdir}/ocaml/stublibs/*.so*

%files devel
%defattr(-,root,root)
%doc html
%{_libdir}/ocaml/augeas/*.a
%{_libdir}/ocaml/augeas/*.cmxa
%{_libdir}/ocaml/augeas/*.cmx
%{_libdir}/ocaml/augeas/*.mli

