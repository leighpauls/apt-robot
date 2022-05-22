
.PHONY: all


SRC_DIR = src
OUTPUT_DIR = out

CXX_FLAGS = -Irplidar_sdk/sdk/sdk/include -Irplidar_sdk/sdk/sdk/src -Isrc -std=c++17
LD_FLAGS += -lstdc++ -lpthread

all: $(OUTPUT_DIR)/lidar_reader


rplidar_sdk/sdk/output/Darwin/Release/librplidar_sdk.a: rplidar_sdk
	make -C rplidar_sdk/sdk

$(OUTPUT_DIR)/lidar_reader: $(SRC_DIR)/*.cpp rplidar_sdk/sdk/output/Darwin/Release/librplidar_sdk.a
	-mkdir `dirname $@`
	c++ $(CXX_FLAGS) -o $@ $^ $(LD_FLAGS)
