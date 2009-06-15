#include <pygobject.h>
void pygtksheet_add_constants(PyObject *module, const gchar *strip_prefix);
void pygtksheet_register_classes (PyObject *d); 
extern PyMethodDef pygtksheet_functions[];
 
DL_EXPORT(void)
init_gtksheet(void)
{
    PyObject *m, *d;
 
    init_pygobject ();
 
    m = Py_InitModule ("gtksheet._gtksheet", pygtksheet_functions);
    d = PyModule_GetDict (m);
 
    pygtksheet_register_classes (d);
    pygtksheet_add_constants(m, "GTK_");
 
    if (PyErr_Occurred ()) {
        Py_FatalError ("can't initialise module gtksheet");
    }
}

