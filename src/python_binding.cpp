#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

int add(int i, int j) { return i + j; }

std::vector<double> get_some_list() {
  return std::vector<double>({1.0, 2.0, 3.0});
}

PYBIND11_MODULE(python_binding, m) {
  m.doc() = "pybind11 example plugin"; // optional module docstring

  m.def("add", &add, "A function that adds two numbers");

  m.def("get_some_list", &get_some_list, "returns a list");
}
