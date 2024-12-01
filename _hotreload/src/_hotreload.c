#include "_hotreload.h"

PyObject *method_structure(PyObject *self, PyObject *args);

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

static PyObject *version(PyObject *self) {
    // version recorder
    return Py_BuildValue("s", "pygame-hotreloader v0.0.1");
}

static struct PyMethodDef methods[] = {
    {"version", (PyCFunction) version, METH_NOARGS, "Returns the current version of the pygame-hotreloader project."},
    {NULL, NULL, 0, NULL} 
}; // func_name, (PyCFunction) c_func_name, args, documentation

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "_hotreload", // c file name, __name__
    NULL, // __doc__
    -1, // notifies whether the module keeps any state in global variables -
        // return sizeof(struct), where the struct holds module-wide state things like counters
    methods // functions
};

PyMODINIT_FUNC PyInit__hotreload(void) {
    // any code that would go in the global space when importing a module
    return PyModule_Create(&module);
}
