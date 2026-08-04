# TESTING NOTE: The testsuite requires numerous packages, many of which are
# built with dune.  Furthermore, the testsuite assumes it is running in a git
# checkout, and has access to the Internet.  We cannot satisfy any of these
# conditions on an abf builder, so we do not run the test suite.

# One of the dune libraries now depends on lwt.  We do not currently need that
# library in OpenMandriva, so don't build it.
%bcond lwt 0

%bcond_with docs

# Libraries currently required in the distro (aligned with Fedora bootstrap set).
# dune-glob/action-plugin need a public "re" findlib package and are omitted.
# dune-rpc/chrome-trace/ocamlc-loc are not needed by reverse deps yet.
%global pkgbuild dune-build-info,dune-configurator,dune-private-libs,dune-site,dyn,fs-io,ordering,stdune,top-closure,xdg

%global giturl  https://github.com/ocaml/dune

Name:           ocaml-dune
Version:        3.24.1
Release:	12
Summary:        Composable build system for OCaml and Reason

# Dune itself is MIT.  Some bundled libraries have a different license:
# ISC:
# - vendor/cmdliner
# - vendor/fmt
# - vendor/notty
# - vendor/opam-0install
# - vendor/sha
# - vendor/uutf
# LGPL-2.0-only:
# - vendor/incremental-cycles
# LGPL-2.0-only WITH OCaml-LGPL-linking-exception
# - vendor/ocaml-inotify
# - vendor/opam
# - vendor/opam-file-format
# - vendor/re
# LGPL-2.1-or-later:
# - vendor/0install-solver
# MIT:
# - vendor/build_path_prefix_map
# - vendor/fiber
# - vendor/lwd
# - vendor/spawn
License:        MIT AND ISC AND LGPL-2.0-only AND LGPL-2.0-only WITH OCaml-LGPL-linking-exception AND LGPL-2.1-or-later
URL:            https://dune.build
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}/dune-%{version}.tar.gz
Source1:	macros.buildsys.dune
# When building without lwt, remove libraries that need it
Patch:          https://src.fedoraproject.org/rpms/ocaml-dune/raw/rawhide/f/%{name}-no-lwt.patch
# Temporary workaround for broken debuginfo (rhbz#2168932)
# See https://github.com/ocaml/dune/issues/6929
Patch:          https://src.fedoraproject.org/rpms/ocaml-dune/raw/rawhide/f/%{name}-debuginfo.patch

# Change to the furo theme for the docs
# https://github.com/ocaml/dune/commit/9f3da04c1c27ff80e8d1ab71de15c53a0ca953da
Patch:          https://src.fedoraproject.org/rpms/ocaml-dune/raw/rawhide/f/use-furo-theme.patch

BuildRequires:  make
BuildRequires:  ocaml >= 4.08
BuildRequires:  ocaml-compiler-libs
%if !0%{?rhel}
BuildRequires:  ocaml-csexp-devel >= 1.5.0
BuildRequires:  ocaml-pp-devel >= 1.2.0
%endif
BuildRequires:  ocaml-compiler

%if %{with docs}
BuildRequires:  python%{pyver}dist(furo)
BuildRequires:  python%{pyver}dist(sphinx)
BuildRequires:  python%{pyver}dist(sphinx-copybutton)
BuildRequires:  python%{pyver}dist(sphinx-design)
%endif

%if %{with lwt}
BuildRequires:  ocaml-lwt-devel >= 5.6.0
%endif

# Dune has vendored deps to avoid dependency cycles.  Upstream deliberately
# does not support unbundling these dependencies.
# See https://github.com/ocaml/dune/issues/220
Provides:       bundled(ocaml-0install-solver) = 2.18
Provides:       bundled(ocaml-build-path-prefix-map) = 0.3
Provides:       bundled(ocaml-cmdliner) = 1.2.0
Provides:       bundled(ocaml-fiber) = 3.7.0
Provides:       bundled(ocaml-fmt) = 0.8.10
Provides:       bundled(ocaml-incremental-cycles) = 1e2030a5d5183d84561cde142eecca40e03db2a3
Provides:       bundled(ocaml-inotify) = 2.3
Provides:       bundled(ocaml-lwd) = 0.3
Provides:       bundled(ocaml-notty) = 0.2.3
Provides:       bundled(ocaml-opam) = 2.2.0~alpha2
Provides:       bundled(ocaml-opam-0install) = 0.4.3
Provides:       bundled(ocaml-opam-file-format) = 2.1.6
Provides:       bundled(ocaml-re) = 1.11.0
Provides:       bundled(ocaml-sha) = 1.15.4
Provides:       bundled(ocaml-spawn) = 0.15.1
Provides:       bundled(ocaml-uutf) = 1.0.3

Provides:       dune = %{version}-%{release}

# Subpackages dropped from the 3.24 bootstrap set (need public re or unused)
Obsoletes:      %{name}-action-plugin < %{version}-%{release}
Obsoletes:      %{name}-action-plugin-devel < %{version}-%{release}
Obsoletes:      %{name}-glob < %{version}-%{release}
Obsoletes:      %{name}-glob-devel < %{version}-%{release}
Obsoletes:      %{name}-rpc < %{version}-%{release}
Obsoletes:      %{name}-rpc-devel < %{version}-%{release}
Obsoletes:      ocaml-chrome-trace < %{version}-%{release}
Obsoletes:      ocaml-chrome-trace-devel < %{version}-%{release}
Obsoletes:      ocaml-ocamlc-loc < %{version}-%{release}
Obsoletes:      ocaml-ocamlc-loc-devel < %{version}-%{release}

# The dune rules module requires Toploop
Requires:       ocaml-compiler-libs%{?_isa}

# Install documentation in the main package doc directory
%global _docdir_fmt %{name}

%description
Dune is a build system designed for OCaml/Reason projects only. It focuses
on providing the user with a consistent experience and takes care of most of
the low-level details of OCaml compilation. All you have to do is provide a
description of your project and Dune will do the rest.

The scheme it implements is inspired from the one used inside Jane Street and
adapted to the open source world. It has matured over a long time and is used
daily by hundred of developers, which means that it is highly tested and
productive.

%if %{with docs}
%package        doc
# The content is MIT.  Other licenses are due to files added by sphinx.
# BSD-2-Clause:
# - _static/basic.css
# - _static/doctools.js
# - _static/documentation_options.js
# - _static/file.png
# - _static/language_data.js
# - _static/minus.png
# - _static/plus.png
# - _static/searchtools.js
# - _static/sphinx_highlight.js
# MIT:
# - _static/check-solid.svg
# - _static/clipboard.min.js
# - _static/copy-button.svg
# - _static/copybutton.css
# - _static/copybutton.js
# - _static/copybutton_funcs.js
# - _static/design-style.*.min.css
# - _static/design-tabs.js
# - _static/css
# - _static/js
License:        MIT AND BSD-2-Clause
Summary:        HTML documentation for %{name}
BuildArch:      noarch

%description    doc
HTML documentation for dune, a composable build system for OCaml.
%endif

## Dune libraries

%package        build-info
Summary:        Embed build information in an executable
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    build-info
The build-info library allows access to information about how an
executable was built, such as the version of the project at which it was
built or the list of statically linked libraries with their versions.
It supports reporting the version from a version control system during
development to get a precise reference of when the executable was built.

%package        build-info-devel
Summary:        Development files for %{name}-build-info
License:        MIT
Requires:       %{name}-build-info%{?_isa} = %{version}-%{release}

%description    build-info-devel
The ocaml-dune-build-info-devel package contains libraries and signature
files for developing applications that use ocaml-dune-build-info.

%package        configurator
Summary:        Helper library for gathering system configuration
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}

%description    configurator
Dune-configurator is a small library that helps write OCaml scripts that
test features available on the system, in order to generate config.h
files for instance.  Among other things, dune-configurator allows one
to:

- test if a C program compiles
- query pkg-config
- import a #define from OCaml header files
- generate a config.h file

%package        configurator-devel
Summary:        Development files for %{name}-configurator
License:        MIT
Requires:       %{name}-configurator%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune-devel%{?_isa} = %{version}-%{release}

# This can be removed when F40 reaches EOL
Obsoletes:      %{name}-devel < 2.9.1-4
Provides:       %{name}-devel = %{version}-%{release}

%description    configurator-devel
The ocaml-dune-configurator-devel package contains libraries and
signature files for developing applications that use
ocaml-dune-configurator.

%package        private-libs
Summary:        Private dune libraries
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}

%description    private-libs
This package contains code that is shared between various dune-xxx
packages.  However, it is not meant for public consumption and provides
no stability guarantee.

%package        private-libs-devel
Summary:        Development files for %{name}-private-libs
License:        MIT
Requires:       %{name}-private-libs%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}

%description    private-libs-devel
The ocaml-dune-private-libs-devel package contains libraries and
signature files for other dune packages.  Do not use.

%if %{with lwt}
%package        rpc-lwt
Summary:        Communicate with dune using rpc and Lwt
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-rpc%{?_isa} = %{version}-%{release}

%description    rpc-lwt
This package contains a library used to communicate with dune over rpc
using Lwt.

%package        rpc-lwt-devel
Summary:        Development files for %{name}-rpc-lwt
License:        MIT
Requires:       %{name}-rpc-lwt%{?_isa} = %{version}-%{release}
Requires:       %{name}-rpc-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
%endif
Requires:       ocaml-lwt-devel%{?_isa}

%description    rpc-lwt-devel
The ocaml-dune-rpc-lwt-devel package contains libraries and signature
files for developing applications that use ocaml-rpc-lwt.
%endif

%package        site
Summary:        Embed location information inside executables and libraries
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-private-libs%{?_isa} = %{version}-%{release}

%description    site
This library enables embedding location information inside executables
and libraries.

%package        site-devel
Summary:        Development files for %{name}-site
License:        MIT
Requires:       %{name}-site%{?_isa} = %{version}-%{release}
Requires:       %{name}-private-libs-devel%{?_isa} = %{version}-%{release}

%description    site-devel
The ocaml-dune-site-devel package contains libraries and signature files
for developing applications that use ocaml-dune-site.

%package     -n ocaml-dyn
Summary:        Dynamic types
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}

%description -n ocaml-dyn
This library supports dynamic types in OCaml.

%package     -n ocaml-dyn-devel
Summary:        Development files for ocaml-dyn
License:        MIT
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-pp-devel%{?_isa}
%endif

%description -n ocaml-dyn-devel
The ocaml-dyn-devel package contains libraries and signature files for
developing applications that use ocaml-dyn.

%package     -n ocaml-ordering
Summary:        Element ordering
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-ordering
Element ordering in OCaml.

%package     -n ocaml-ordering-devel
Summary:        Development files for ocaml-ordering
License:        MIT
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}

%description -n ocaml-ordering-devel
The ocaml-ordering-devel package contains libraries and signature files
for developing applications that use ocaml-ordering.

%package     -n ocaml-fs-io
Summary:        File-system IO helpers used by dune
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-fs-io
Miscellaneous filesystem operations used by dune libraries.

%package     -n ocaml-fs-io-devel
Summary:        Development files for ocaml-fs-io
License:        MIT
Requires:       ocaml-fs-io%{?_isa} = %{version}-%{release}

%description -n ocaml-fs-io-devel
The ocaml-fs-io-devel package contains libraries and signature files
for developing applications that use ocaml-fs-io.

%package     -n ocaml-stdune
Summary:        Dune's unstable standard library
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-fs-io%{?_isa} = %{version}-%{release}
Requires:       ocaml-top-closure%{?_isa} = %{version}-%{release}

%description -n ocaml-stdune
This package contains Dune's unstable standard library.

%package     -n ocaml-stdune-devel
Summary:        Development files for ocaml-stdune
License:        MIT
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-fs-io-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-top-closure-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
%endif

%description -n ocaml-stdune-devel
The ocaml-stdune-devel package contains libraries and signature files
for developing applications that use ocaml-stdune.

%package     -n ocaml-top-closure
Summary:        Topological closure over a graph
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-top-closure
Topological closure used by dune's standard library.

%package     -n ocaml-top-closure-devel
Summary:        Development files for ocaml-top-closure
License:        MIT
Requires:       ocaml-top-closure%{?_isa} = %{version}-%{release}

%description -n ocaml-top-closure-devel
The ocaml-top-closure-devel package contains libraries and signature
files for developing applications that use ocaml-top-closure.

%package     -n ocaml-xdg
Summary:        XDG Base Directory Specification
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ocaml-xdg
This package contains the XDG Base Directory Specification.

%package     -n ocaml-xdg-devel
Summary:        Development files for ocaml-xdg
License:        MIT
Requires:       ocaml-xdg%{?_isa} = %{version}-%{release}

%description -n ocaml-xdg-devel
The ocaml-xdg-devel package contains libraries and signature files for
developing applications that use ocaml-xdg.

%package emacs
Summary:	Dune file editing support for the emacs editor
Requires:	emacs
License:	MIT
Requires:	%{name}%{?_isa} = %{EVRD}

%description emacs
Dune file editing support for the emacs editor

%prep
%autosetup -N -n dune-%{version}
%if %{without lwt}
%autopatch 0 -p1
rm -fr otherlibs/dune-rpc-lwt opam/dune-rpc-lwt.opam dune-rpc-lwt.opam
%endif
%autopatch -m1 -p1

%build
./configure \
	--prefix %{_prefix} \
	--bindir %{_bindir} \
	--datadir %{_datadir} \
	--docdir %{_prefix}/doc \
	--etcdir %{_sysconfdir} \
	--libdir %{ocamldir} \
	--libexecdir %{ocamldir} \
	--mandir %{_mandir} \
	--sbindir %{_sbindir}

# Bootstrap then build dune binary + required libraries in one pass.
# A second selective -p build without "dune" drops dune.install artifacts
# and breaks make install.
ocaml boot/bootstrap.ml
_boot/dune.exe build -p dune,%{pkgbuild} %{?_smp_mflags} --verbose \
	--profile dune-bootstrap
%if %{with docs}
%make_build doc
%endif

%install
%make_install

# Libraries (dune package itself already installed by make install)
_boot/dune.exe install --destdir=%{buildroot} -p %{pkgbuild}

# We use %%doc below
rm -fr %{buildroot}%{_prefix}/doc

# Generate %%files lists
%ocaml_files -s

mkdir -p %{buildroot}%{_prefix}/lib/rpm/macros.d
install -c -m 644 %{S:1} %{buildroot}%{_prefix}/lib/rpm/macros.d/

%files
%license LICENSE.md
%doc CHANGES.md README.md
%{_bindir}/dune
%{_mandir}/man*/dune*
%{_prefix}/lib/rpm/macros.d/macros.buildsys.dune

%if %{with docs}
%files doc
%doc doc/_build/*
%endif

%files build-info -f .ofiles-dune-build-info

%files build-info-devel -f .ofiles-dune-build-info-devel

%files configurator -f .ofiles-dune-configurator
%dir %{ocamldir}/dune/
%{ocamldir}/dune/META

%files configurator-devel -f .ofiles-dune-configurator-devel
%{ocamldir}/dune/dune-package
%{ocamldir}/dune/opam

%files private-libs -f .ofiles-dune-private-libs

%files private-libs-devel -f .ofiles-dune-private-libs-devel

%if %{with lwt}
%files rpc-lwt -f .ofiles-dune-rpc-lwt

%files rpc-lwt-devel -f .ofiles-dune-rpc-lwt-devel
%endif

%files site -f .ofiles-dune-site

%files site-devel -f .ofiles-dune-site-devel

%files -n ocaml-dyn -f .ofiles-dyn

%files -n ocaml-dyn-devel -f .ofiles-dyn-devel

%files -n ocaml-fs-io -f .ofiles-fs-io

%files -n ocaml-fs-io-devel -f .ofiles-fs-io-devel

%files -n ocaml-ordering -f .ofiles-ordering

%files -n ocaml-ordering-devel -f .ofiles-ordering-devel

%files -n ocaml-stdune -f .ofiles-stdune

%files -n ocaml-stdune-devel -f .ofiles-stdune-devel

%files -n ocaml-top-closure -f .ofiles-top-closure

%files -n ocaml-top-closure-devel -f .ofiles-top-closure-devel

%files -n ocaml-xdg -f .ofiles-xdg

%files -n ocaml-xdg-devel -f .ofiles-xdg-devel

%files emacs
%{_datadir}/emacs/site-lisp/*.el
