
.PHONY: all


SRC_DIR=src
OUTPUT_DIR=out

COMMON_CXX_FLAGS = -Irplidar_sdk/sdk/sdk/include -Irplidar_sdk/sdk/sdk/src -Isrc -std=c++17 -lstdc++ -lpthread

PYTHON_CONFIG=/Users/leighpauls/.pyenv/versions/3.10.4/bin/python-config

LIDARPY_FLAGS=$($(PYTHON_CONFIG) --includes) $(shell .venv/bin/python -m pybind11 --includes) $($(PYTHON_CONFIG) --libs) $($(PYTHON_CONFIG) --cflags) $($(PYTHON_CONFIG) --ldflags) -O3 -Wall -shared -fPIC -undefined dynamic_lookup

LIDARPY_OUTPUT=$(OUTPUT_DIR)/lidarpy$(shell $(PYTHON_CONFIG) --extension-suffix)


all: $(OUTPUT_DIR)/lidar_reader $(LIDARPY_OUTPUT)

rplidar_sdk/sdk/output/Darwin/Release/librplidar_sdk.a: rplidar_sdk
	make -C rplidar_sdk/sdk

$(OUTPUT_DIR)/lidar_reader: $(SRC_DIR)/lidar.cpp $(SRC_DIR)/lidar_reader.cpp rplidar_sdk/sdk/output/Darwin/Release/librplidar_sdk.a
	-mkdir `dirname $@`
	c++ $(COMMON_CXX_FLAGS) -o $@ $^

$(LIDARPY_OUTPUT): $(SRC_DIR)/lidar.cpp $(SRC_DIR)/lidarpy.cpp rplidar_sdk/sdk/output/Darwin/Release/librplidar_sdk.a
	-mkdir `dirname $@`
	c++ $(COMMON_CXX_FLAGS) $(LIDARPY_FLAGS) -o $@ $^
