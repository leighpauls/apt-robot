#!/bin/bash

PYTHON_CONFIG=/Users/leighpauls/.pyenv/versions/3.10.4/bin/python-config


FLAGS="$(${PYTHON_CONFIG} --includes) $(${PYTHON_CONFIG} --libs) $(${PYTHON_CONFIG} --cflags) $(${PYTHON_CONFIG} --ldflags)"


c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) $FLAGS -undefined dynamic_lookup src/python_binding.cpp -o out/python_binding$($PYTHON_CONFIG --extension-suffix)
