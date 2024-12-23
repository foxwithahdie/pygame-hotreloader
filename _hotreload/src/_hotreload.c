#include "_hotreload.h"

PyObject *method_structure(PyObject *self, PyObject *args) {
    int arg1;
    int arg2;
    PyArg_ParseTuple(args, "ii", &arg1, &arg2);
    //    arguments condensed into a tuple
    //     tuple destructured, then passed into your given objects based on your string
    // "ii" represents two integers, similar to printf
    //      then pass the memory addresses of each of the arguments you want to pass in

    return PyLong_FromLong((long) (arg1 + arg2)); // int does not exist, must convert to pyobject
    // lots of methods to take in raw data and convert it to python object
    // you can wrap your C functions in a python C function
}

static PyObject *version(PyObject *self) { // static if not meant to be used outside of the C source file - private
// wanna use static for inner C code
    // version recorder
    return Py_BuildValue("s", "pygame-hotreloader v0.0.2");
}

PyDoc_STRVAR(version_doc, "Returns the current version of the pygame-hotreloader project.");
PyDoc_STRVAR(add_doc, "adds TWO numbers together.");

static struct PyMethodDef methods[] = {
    {"add", method_structure, METH_VARARGS, add_doc},
    {"version", (PyCFunction) version, METH_NOARGS, version_doc},
    {NULL}  // null termination
}; // func_name, (PyCFunction) c_func_name, args, documentation - in PyDoc_STRVAR

PyDoc_STRVAR(hotreload_doc, "C implemented functions for interacting with the pygame instance.");

static struct PyModuleDef hotreload_module = {
    PyModuleDef_HEAD_INIT,
    "_hotreload", // c file name, __name__
    hotreload_doc, // __doc__
    -1, // notifies whether the module keeps any state in global variables -
        // return sizeof(struct), where the struct holds module-wide state things like counters
    methods, // functions
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit__hotreload(void) {
    // any code that would go in the global space when importing a module
    return PyModule_Create(&hotreload_module);
}
