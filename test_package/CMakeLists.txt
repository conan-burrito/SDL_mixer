cmake_minimum_required(VERSION 3.6)
project(PackageTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example example.cpp)
target_link_libraries(example ${CONAN_LIBS})
target_include_directories(example  PRIVATE ${CONAN_INCLUDE_DIRS_SDL2}/SDL2)
set_target_properties(example
    PROPERTIES
    OUTPUT_NAME "test"
    CXX_STANDARD 11
)
