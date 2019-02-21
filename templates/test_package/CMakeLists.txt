# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

cmake_minimum_required(VERSION 3.3)

project({{ name }}TestConan)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)
string(REPLACE ";" ":" LINK_FLAGS "${CONAN_LIB_DIRS}")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath-link,${LINK_FLAGS} -Wl,--no-undefined")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath-link,${LINK_FLAGS} -Wl,--disable-new-dtags")

find_package({{ name }} REQUIRED)

set(CMAKE_CXX_STANDARD 11)
add_executable(${PROJECT_NAME} ${PROJECT_NAME})
target_link_libraries(${PROJECT_NAME} PUBLIC WSBU::{{ lib_target_name }})

enable_testing()
add_test(NAME ${PROJECT_NAME}
        COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
