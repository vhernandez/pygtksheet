pygtksheetdir = $(pythondir)/gtk-2.0/gtksheet
pygtksheetexecdir = $(pyexecdir)/gtk-2.0/gtksheet

pygtksheet_PYTHON = \
  __init__.py 


# FIXME: Do we want to drop files in the pygtk directory or in our own pkg directory
defsdir = $(PYGTK_DEFSDIR)
defs_DATA = \
 gtksheet.defs \
 gtksheet-types.defs \
 gtksheet-addons.defs 

EXTRA_DIST = $(defs_DATA)
CLEANFILES =

pkgincludedir = $(includedir)/pygtksheet-2.0/pygtksheet
pkginclude_HEADERS = 

INCLUDES = -I$(top_srcdir) $(PYTHON_INCLUDES)
#COMMONDEFS = $(srcdir)/gtksheet-types.defs 
COMMONDEFS = 

# gtksheet module
pygtksheetexec_LTLIBRARIES = _gtksheetmodule.la
_gtksheetmodule_la_CFLAGS = $(PYGTK_CFLAGS) $(GTK_CFLAGS) $(GTKSHEET_CFLAGS)
_gtksheetmodule_la_LDFLAGS = -module -avoid-version -export-symbols-regex init_gtksheet
_gtksheetmodule_la_LIBADD =  $(GTKSHEET_LIBS) $(PYGTK_LIBS) $(GTK_LIBS)
_gtksheetmodule_la_SOURCES = gtksheetmodule.c
gtksheet.c: $(COMMONDEFS) gtksheet-addons.defs gtksheet-types.defs gtksheet.override
nodist__gtksheetmodule_la_SOURCES = gtksheet.c

CLEANFILES += gtksheet.c
EXTRA_DIST += gtksheet.override \
	gtksheetrange.override

CODEGEN=pygobject-codegen-2.0

.defs.c:
	(cd $(srcdir) \
	 && $(CODEGEN) \
	    --register $(PYGTK_DEFSDIR)/pango-types.defs \
	    --register $(PYGTK_DEFSDIR)/gdk-types.defs \
	    --register $(PYGTK_DEFSDIR)/gtk-types.defs \
	    --override $*.override \
	    --prefix py$* $*.defs) > gen-$*.c \
	&& cp gen-$*.c $*.c \
	&& rm -f gen-$*.c


