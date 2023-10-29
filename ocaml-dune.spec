%global libname dune
%global _pkgdocdir %{_docdir}/%{name}-%{version}
# "fix" underlinking:
%define _disable_ld_no_undefined 1

# Since menhir now requires dune to build, but dune needs menhir only for the
# tests, build in bootstrap mode to skip the tests and the need for menhir.
%bcond_without menhir

Summary:	A composable build system for OCaml
Name:		ocaml-%{libname}
Version:	3.11.1
Release:	1
Group:		Development/OCaml
# Dune itself is MIT.  Some bundled libraries have a different license:
# ISC:
# - vendor/cmdliner
# LGPLv2:
# - vendor/incremental-cycles
# LGPLv2 with exceptions:
# - vendor/opam-file-format
# - vendor/re
License:	MIT and LGPLv2 and LGPLv2 with exceptions and ISC
URL:		https://dune.build
Source0:	https://github.com/ocaml/%{libname}/archive/%{version}/%{libname}-%{version}.tar.gz
BuildRequires:	emacs
BuildRequires:	ocaml >= 4.07
BuildRequires:	ocaml-findlib
BuildRequires:	ocaml-csexp
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)

%if %{without menhir}
# Required by tests.
BuildRequires:  ocaml-menhir
%endif

# Dune has vendored deps (ugh):
# I'm not clear on how to unbundle them.
# It seems to be unsupported upstream; the bootstrap process for dune
# doesn't seem to be able to detect libraries installed systemwide.
# https://github.com/ocaml/dune/issues/220
Provides:	bundled(ocaml-build-path-prefix-map) = 0.2
Provides:	bundled(ocaml-opam-file-format) = 2.0.0

Provides:	dune = %{version}-%{release}

Provides:	jbuilder = %{version}-%{release}
Obsoletes:	jbuilder < 1.0.1-3

%description
Dune is a build system designed for OCaml/Reason projects only. It focuses
on providing the user with a consistent experience and takes care of most of
the low-level details of OCaml compilation. All you have to do is provide a
description of your project and Dune will do the rest.

The scheme it implements is inspired from the one used inside Jane Street and
adapted to the open source world. It has matured over a long time and is used
daily by hundred of developers, which means that it is highly tested and
productive.

%files
%license LICENSE.md
%doc %{_pkgdocdir}/README.md
%doc %{_pkgdocdir}/CHANGES.md
%doc %{_pkgdocdir}/MIGRATION.md
%{_bindir}/dune
%{_mandir}/man*/dune*
%dir %{_pkgdocdir}/
%dir %{_libdir}/ocaml/dune/
%dir %{_libdir}/ocaml/dune-action-plugin/
%dir %{_libdir}/ocaml/dune-build-info/
%dir %{_libdir}/ocaml/dune-configurator/
%dir %{_libdir}/ocaml/dune-glob/
%dir %{_libdir}/ocaml/dune-private-libs/
%dir %{_libdir}/ocaml/dune-private-libs/dune-lang/
%dir %{_libdir}/ocaml/dune-private-libs/dune_re/
%dir %{_libdir}/ocaml/dune-private-libs/ocaml-config/
%dir %{_libdir}/ocaml/dune-private-libs/stdune/
%{_libdir}/ocaml/dune*/META
%{_libdir}/ocaml/dune*/*.cma
%{_libdir}/ocaml/dune*/*.cmi
%{_libdir}/ocaml/dune-configurator/.private/
%{_libdir}/ocaml/dune-private-libs/*/*.cma
%{_libdir}/ocaml/dune-private-libs/*/*.cmi
%{_libdir}/ocaml/dune*/*.cmxs
%{_libdir}/ocaml/dune-private-libs/*/*.cmxs
%{_libdir}/ocaml/stublibs/dllstdune_stubs.so
%{_libdir}/ocaml/stublibs/dlldune_filesystem_stubs_stubs.so

#---------------------------------------------------------------------
%package devel
Summary:	Development files for %{name}
Group:		Development/OCaml
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use %{name}.

%files devel
%{_libdir}/ocaml/dune*/dune-package
%{_libdir}/ocaml/dune*/opam
%{_libdir}/ocaml/dune*/*.cmt
%{_libdir}/ocaml/dune*/*.cmti
%{_libdir}/ocaml/dune*/*.ml
%{_libdir}/ocaml/dune*/*.mli
%{_libdir}/ocaml/dune-private-libs/*/*.cmt
%{_libdir}/ocaml/dune-private-libs/*/*.cmti
%{_libdir}/ocaml/dune-private-libs/*/*.ml
%{_libdir}/ocaml/dune-private-libs/*/*.mli
%{_libdir}/ocaml/dune*/*.a
%{_libdir}/ocaml/dune*/*.cmx
%{_libdir}/ocaml/dune*/*.cmxa
%{_libdir}/ocaml/dune-private-libs/*/*.a
%{_libdir}/ocaml/dune-private-libs/*/*.cmx
%{_libdir}/ocaml/dune-private-libs/*/*.cmxa
%{_libdir}/ocaml/dune-site/plugins

#---------------------------------------------------------------------

%package doc
Summary:	HTML documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description doc
HTML documentation for dune, a composable build system for OCaml.

%files doc
%exclude %{_pkgdocdir}/README.md
%exclude %{_pkgdocdir}/CHANGES.md
%doc %{_pkgdocdir}/*

#---------------------------------------------------------------------

%package emacs
Summary:	Emacs support for %{name}
Group:		Development/OCaml
License:	ISC
Requires:	%{name} = %{EVRD}
BuildArch:	noarch

%description emacs
The %{name}-devel package contains Emacs integration with the dune build
system, a mode to edit dune files, and flymake support for dune files.

%files emacs
%{_datadir}/emacs/site-lisp/dune*

#---------------------------------------------------------------------

%prep
%autosetup -n %{libname}-%{version} -p1

%build
./configure \
	--libdir %{_libdir}/ocaml \
	--mandir %{_mandir}

# This command fails, because ppx_bench, ppx_expect, and core_bench are missing.
# However, it is only tests that fail, not the actual build, so ignore the
# failures and continue.
%make_build release || :
./dune.exe build @install
%make_build doc

# Relink the stublib.  See https://github.com/ocaml/dune/issues/2977.
cd _build/default/src/stdune
ocamlmklib -g -ldopt "$RPM_LD_FLAGS" -o stdune_stubs fcntl_stubs.o
cd -

%install
# "make install" only installs the binary.  We want the libraries, too.
./dune.exe install --destdir %{buildroot}

# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod 0755 {} \+

# Install documentation by way of pkgdocdir.
rm -fr %{buildroot}%{_prefix}/doc
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -ar README.md CHANGES.md MIGRATION.md doc/_build/* %{buildroot}%{_pkgdocdir}/

%if %{without menhir}
%check
# These are the only tests we can run.  The others require components that
# either depend on dune themselves or are not available in Fedora at all.
%{buildroot}%{_bindir}/dune runtest test/unit-tests
%endif

