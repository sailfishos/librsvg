Name:           librsvg
Summary:        An SVG library based on cairo
Version:        2.40.20
Release:        1
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/LibRsvg
Source:         http://download.gnome.org/sources/librsvg/2.40/librsvg-%{version}.tar.xz
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-png)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libcroco-0.6)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  vala-devel
BuildRequires:  vala
BuildRequires:  vala-tools

Patch1: 0001-Disable-gkt-doc.patch

%description
An SVG library based on cairo.

%package devel
Summary:        Libraries and include files for developing with librsvg
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with librsvg.

%package tools
Summary:        Extra tools for librsvg
Requires:       %{name} = %{version}-%{release}

%description tools
This package provides extra utilities based on the librsvg library.


%prep

%setup -q -n librsvg-%{version}/librsvg
%patch1 -p1


%build
# work around an ordering problem in configure
enable_pixbuf_loader=yes

export enable_pixbuf_loader

./autogen.sh --disable-static  \
        --disable-gtk-doc \
        --enable-introspection \
        --enable-vala \
        --prefix=%{_prefix} \
        --libdir=%{_libdir}

make %{?_smp_mflags}

%install

%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
rm -f $RPM_BUILD_ROOT%{_datadir}/pixmaps/svg-viewer.svg

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS NEWS README
%license COPYING COPYING.LIB
%{_libdir}/librsvg-2.so.*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-svg.so
%{_libdir}/girepository-1.0/*
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/librsvg.thumbnailer

%files devel
%{_libdir}/librsvg-2.so
%{_includedir}/librsvg-2.0
%{_libdir}/pkgconfig/librsvg-2.0.pc
%{_datadir}/gir-1.0/*
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/librsvg-2.0.vapi

%files tools
%{_bindir}/rsvg-convert
%{_mandir}/man1/rsvg-convert.1*
