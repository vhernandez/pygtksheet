BUILDDIR = $(top_builddir)/docs

REF_VERSION = $(PYTHON_GTKSHEET_MAJOR_VERSION).$(PYTHON_GTKSHEET_MINOR_VERSION)
FULL_VERSION = $(REF_VERSION).$(PYTHON_GTKSHEET_MICRO_VERSION)

HTML_STYLE = $(PYGOBJECT_DATADIR)/pygobject/xsl/ref-html-style.xsl
PDF_STYLE = $(PYGOBJECT_DATADIR)/pygobject/xsl/pdf-style.xsl

XMLFILES = \
	gtksheet-classes.xml \
	gtksheet-gtksheet.xml \
	gtksheet-gtksheetrange.xml

HTMLdir = $(datadir)/gtk-doc/html/pygtksheet
HTML_DATA =					\
	html/class-gtksheet.html		\
	html/class-gtksheetrange.html		\
	html/gtksheet-class-reference.html	\
	html/pygtksheet.devhelp		\
	html/index.html				\
	html/index.sgml

CSS_FILES = $(PYGOBJECT_PYGDOCS)/style.css
CSSdir = $(HTMLdir)
CSS_DATA = $(CSS_FILES)

BUILT_SOURCES = 	\
	build_stamp	\
	builddate.xml	\
	$(HTML_DATA)

CLEANFILES = 		\
	build_stamp	\
	builddate.xml	\
	$(HTML_DATA)

EXTRA_DIST = 		\
	$(XMLFILES) 	\
	$(XSLFILES)	\
	$(FIX_XREF)

REFERENCE_DEPS = 	\
	$(XMLFILES)	\
	$(XSLFILES)

$(HTML_DATA): build_stamp

if ENABLE_DOCS

builddate.xml: $(REFERENCE_DEPS)
	$(PYTHON) -c 'import datetime; print datetime.date.today()' > $@

build_stamp: $(REFERENCE_DEPS)builddate.xml
	xsltproc --nonet --xinclude -o $(BUILDDIR)/html/ \
		 --path $(BUILDDIR):$(srcdir) \
                 --stringparam gtkdoc.bookname "pygtksheet" \
                 --stringparam gtkdoc.version ${REF_VERSION} \
                 $(HTML_STYLE) $(srcdir)/gtksheet-classes.xml
	$(PYGOBJECT_FIXXREF) -i /usr/share/gtk-doc/html/pygtk/ $(BUILDDIR)/html/
	touch $@

endif

.PHONY : dist-hook-local
dist-hook: dist-hook-local build_stamp
	mkdir $(distdir)/html
	cp $(srcdir)/html/* $(distdir)/html
	cp $(srcdir)/build_stamp $(distdir)

