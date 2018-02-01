#define Py_LIMITED_API
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <vector>
#include <iostream>
#include <algorithm>

static PyObject* quantize(PyObject *self, PyObject *args) ;

static PyMethodDef FooMethods[] = {
    {"quantize", quantize, METH_VARARGS, "Return the quantizes"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef foomodule = {
    PyModuleDef_HEAD_INIT,
    "quantize",
    "Simple module",
    -1,
    FooMethods
};

PyMODINIT_FUNC PyInit_quantize()
{
    return PyModule_Create(&foomodule);
}

static PyObject* quantize(PyObject *self, PyObject *args) {
    _import_array();
    PyObject *array;
    int n;
    if (!PyArg_ParseTuple(args, "Oi", &array, &n)) {
        return nullptr;
    }
    if (!PyArray_Check(array)) {
        PyErr_SetString(PyExc_TypeError, "Oh no!");
        return nullptr;
    }

    PyArrayObject *in_array = reinterpret_cast<PyArrayObject *>(array);
    if (PyArray_TYPE(in_array) != NPY_FLOAT64 && PyArray_TYPE(in_array) != NPY_FLOAT32) {
        PyErr_SetString(PyExc_TypeError, "Oh no!");
        return nullptr;
    }
    PyArrayObject * np_boundaries = nullptr, *np_quantized = nullptr;
    npy_intp sz = PyArray_Size(array);
    npy_intp dim = n;
    if (PyArray_TYPE(in_array) == NPY_DOUBLE) {
        double* data  = (double*)PyArray_DATA(in_array);

        np_boundaries = (PyArrayObject *) PyArray_SimpleNew(1, &dim, NPY_FLOAT64);
        double* boundaries  = (double*)PyArray_DATA(np_boundaries);
        np_quantized = (PyArrayObject *) PyArray_SimpleNew(1, &sz, NPY_FLOAT64);
        double* quantized  = (double*)PyArray_DATA(np_quantized);

        std::vector<double> values(sz);
        for (int i = 0; i < sz; ++i) {
            values[i] = data[i];
        }

        std::sort(values.begin(), values.end());
        for (int i = 0; i < n; ++i) {
            boundaries[i] = values[sz * i / n];
        }
        for (int i = 0; i < sz; ++i) {
            int place = 0;
            while (place < n && boundaries[place] < data[i]) {
                ++place;
            }
            quantized[i] = place;
        }

    }
    if (PyArray_TYPE(in_array) == NPY_FLOAT32) {
        float* data  = (float*)PyArray_DATA(in_array);
        np_boundaries = (PyArrayObject *) PyArray_SimpleNew(1, &dim, NPY_FLOAT32);
        float* boundaries  = (float*)PyArray_DATA(np_boundaries);
        np_quantized = (PyArrayObject *) PyArray_SimpleNew(1, &sz, NPY_FLOAT32);
        float* quantized  = (float*)PyArray_DATA(np_quantized);
        std::vector<double> values(sz);
        for (int i = 0; i < sz; ++i) {
            values[i] = data[i];
        }

        std::sort(values.begin(), values.end());
        for (int i = 0; i < n; ++i) {
            boundaries[i] = values[sz * i / n];
        }
        for (int i = 0; i < sz; ++i) {
            int place = 0;
            while (place < n && boundaries[place] < data[i]) {
                ++place;
            }
            quantized[i] = place;
        }

        
    }
    return PyTuple_Pack(2, np_boundaries, np_quantized);
}