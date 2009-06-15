-*- mode: m4 -*-
AC_PREREQ(2.63)

dnl the python-gtkextra version number
m4_define(python_gtksheet_major_version, 0)
m4_define(python_gtksheet_minor_version, 1)
m4_define(python_gtksheet_micro_version, 0)
m4_define(python_gtksheet_version, python_gtksheet_major_version.python_gtksheet_minor_version.python_gtksheet_micro_version)

dnl versions of packages we require ...
m4_define(gtk_required_version,      2.10.0)
m4_define(pygtk_required_version,    2.8.0)
m4_define(gtksheet_required_version,    0.1.0)

AC_INIT([python-gtksheet],[python_gtksheet_version],[http://sourceforge.net/tracker/?group_id=35371])
AC_SUBST(ACLOCAL_AMFLAGS, "-I m4 -I .")
AC_CONFIG_MACRO_DIR ("m4")
AC_DEFINE(PYTHON_GTKSHEET_MAJOR_VERSION, python_gtksheet_major_version, [Python GtkSheet major version])
AC_DEFINE(PYTHON_GTKSHEET_MINOR_VERSION, python_gtksheet_minor_version, [Python GtkSheet minor version])
AC_DEFINE(PYTHON_GTKSHEET_MICRO_VERSION, python_gtksheet_micro_version, [Python GtkSheet macro version])

AC_CONFIG_SRCDIR([gtksheet/gtksheetmodule.c])

AM_INIT_AUTOMAKE(AC_PACKAGE_NAME, AC_PACKAGE_VERSION)

dnl put the ACLOCAL flags in the makefile
ACLOCAL="$ACLOCAL $ACLOCAL_FLAGS"

AC_DISABLE_STATIC
LT_INIT

dnl AM_PATH_PYTHON(2.2)
AM_PATH_PYTHON
AC_MSG_CHECKING(for python >= 2.4)
prog="
import sys, string
minver = (2,4,0,'final',0)
if sys.version_info < minver:
  sys.exit(1)
sys.exit(0)"
if $PYTHON -c "$prog" 1>&AS_MESSAGE_LOG_FD 2>&AS_MESSAGE_LOG_FD
then
  AC_MSG_RESULT(okay)
else
  AC_MSG_ERROR(too old)
fi


AM_CHECK_PYTHON_HEADERS(, [AC_MSG_ERROR(could not find Python headers)])

#PKG_CHECK_MODULES(PANGO, pango >= pango_required_version,,[AC_MSG_ERROR(maybe you want the gtk-gnome-1-2 branch?)])
#AC_SUBST(PANGO_CFLAGS)
#AC_SUBST(PANGO_LIBS)

dnl gtk+
AM_PATH_GTK_2_0(gtk_required_version,,[AC_MSG_ERROR(maybe you want the gtk-gnome-1-2 branch?)],$extra_mods)

dnl gtk+extra
PKG_CHECK_MODULES(GTKSHEET, gtksheet-2.0 >= gtksheet_required_version)
AC_SUBST(GTKSHEET_CFLAGS)
AC_SUBST(GTKSHEET_LIBS)

dnl pygtk
PKG_CHECK_MODULES(PYGTK, pygtk-2.0 >= pygtk_required_version)
AC_SUBST(PYGTK_CFLAGS)

AC_MSG_CHECKING(PYGTK_DEFSDIR)
PYGTK_DEFSDIR=`$PKG_CONFIG --variable=defsdir "pygtk-2.0"`
AC_SUBST(PYGTK_DEFSDIR)
AC_MSG_RESULT($PYGTK_DEFSDIR)

AC_MSG_CHECKING(PYGTK_CODEGENDIR)
PYGTK_CODEGENDIR=`$PKG_CONFIG --variable=codegendir "pygtk-2.0"`
AC_SUBST(PYGTK_CODEGENDIR)
AC_MSG_RESULT($PYGTK_CODEGENDIR)

AC_ARG_ENABLE(numpy,
  AS_HELP_STRING([--disable-numpy],[Disable numeric python features]),,
  enable_numpy=yes)

dnl checks to see if Numeric Python is installed.
if test "x$enable_numpy" != xno; then
  save_CPPFLAGS="$CPPFLAGS"
  CPPFLAGS="$CPPFLAGS $PYTHON_INCLUDES"
  AC_CHECK_HEADER(arrayobject.h,
    [AC_DEFINE(HAVE_NUMPY)
     AC_DEFINE(HAVE_ARRAYOBJECT_H)],
    [AC_CHECK_HEADER(Extensions/arrayobject.h,
      [AC_DEFINE(HAVE_NUMPY)
       AC_DEFINE(HAVE_EXTENSIONS_ARRAYOBJECT_H)],
      [AC_CHECK_HEADER(Numeric/arrayobject.h,
        [AC_DEFINE(HAVE_NUMPY)
         AC_DEFINE(HAVE_NUMERIC_ARRAYOBJECT_H)])])])
  CPPFLAGS="$save_CPPFLAGS"
fi

dnl add debugging options ...
changequote(,)dnl
if test "x$GCC" = xyes; then
  case " $CFLAGS " in
  *[\	\ ]-Wall[\	\ ]*) ;;
  *) CFLAGS="$CFLAGS -Wall" ;;
  esac

  case " $CFLAGS " in
  *[\	\ ]-std=c9x[\	\ ]*) ;;
  *) CFLAGS="$CFLAGS -std=c9x" ;;
  esac
fi
changequote([,])dnl

AC_CONFIG_FILES(
  Makefile
  python-gtksheet.pc
  gtksheet/Makefile
  python-gtksheet.spec)
AC_OUTPUT


