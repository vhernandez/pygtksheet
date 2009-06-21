# require automake-1.5
AUTOMAKE_OPTIONS = 1.5

SUBDIRS = gtksheet docs

CLEANFILES =
EXTRA_DIST = 

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = python-gtksheet.pc

EXTRA_DIST += \
  autogen.sh \
  m4/python.m4 \
  python-gtksheet.spec \
  python-gtksheet.spec.in \
  python-gtksheet.pc.in \
  examples/bordercombo.py \
  examples/complex_test.py \
  examples/fontcombo.py \
  examples/move_range_test.py \
  examples/simple_test.py 

snap:
	$(MAKE) dist distdir=$(PACKAGE)-SNAP-`date +"%Y%m%d"`
