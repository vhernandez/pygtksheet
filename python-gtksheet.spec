Summary: Python bindings for the GtkSheet widget set.
Name: python-gtksheet
Version: 0.1.0
Release: 1
Copyright: LGPL
Group: Development/Languages
Source: http://cloud.github.com/downloads/vhernandez/pygtksheet/python-gtksheet-%{version}.tar.gz
BuildRoot: /var/tmp/python-gtksheet-root
Requires: gtk2 >= 2.10.0
Requires: python >= 2.4
Requires: pygtk2 >= 2.8.0
Requires: gtksheet >= 0.1
Buildrequires: python-devel >= 2.4
Buildrequires: pygtk2-devel >= 2.8.0
Buildrequires: gtk+sheet-devel >= 0.1

%description
Python-gtksheet is an extension module for python that gives you access to
the GtkSheet widget.

%package devel
Summary: files needed to build wrappers for python-gtksheet addon libraries
Group: Development/Languages
Requires: python-gtksheet = %{version}

%description devel
This package containes files needed to build wrappers for python-gtksheet
addon libraries so that they interoperate with python-gtksheet.

%prep
%setup -q -n python-gtkshet-%{version}
./configure --prefix=%{_prefix}

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%files
%defattr(644, root, root, 755)
%dir %{_prefix}/lib/python?.?/site-packages/gtk-2.0/gtksheet
%{_prefix}/lib/python?.?/site-packages/gtk-2.0/gtksheet/*.py*

%defattr(755, root, root, 755)
%{_prefix}/lib/python?.?/site-packages/gtk-2.0/gtksheet/_gtksheetmodule.so

%doc AUTHORS NEWS README ChangeLog
%doc examples

%files devel
%defattr(755, root, root, 755)
%{_prefix}/lib/pkgconfig/python-gtksheet.pc
%{_prefix}/lib/python?.?/site-packages/gtk-2.0/gtksheet/_gtksheetmodule.la
%dir %{_prefix}/share/pygtk/2.0/defs
%{_prefix}/share/pygtk/2.0/defs/gtksheet.defs
%{_prefix}/share/pygtk/2.0/defs/gtksheet-types.defs
%{_prefix}/share/pygtk/2.0/defs/gtksheet-addons.defs



