# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

cmake_minimum_required(VERSION 3.3)

{% if cxx %}
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/CMakeModules"){% endif %}
file(STRINGS "version.txt" VERSION)
project({{ name }} VERSION ${VERSION})

option(CONAN "Enable Conan dependency manager" ON)
if (CONAN AND EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    conan_basic_setup(TARGETS)
    string(REPLACE ";" ":" LINK_FLAGS "${CONAN_LIB_DIRS}")
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath-link,${LINK_FLAGS}"){% if library %}
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--disable-new-dtags,-rpath-link,${LINK_FLAGS}"){% endif %}
endif ()

find_program(VALGRIND_EXE valgrind)

find_package(Doxygen QUIET)
find_package(WsbuDocGen QUIET)

enable_testing()

option(BUILD_SHARED_LIBS "Build dynamic libraries when on, else static" ON)
option(TEST_WITH_VALGRIND "Run unit tests with valgrind (if CMAKE_CROSSCOMPILING_EMULATOR is defined, it will override this setting)" OFF)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)
set(EXTRA_FLAGS "-Werror -Wall -Wpedantic -Wconversion")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${EXTRA_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${EXTRA_FLAGS}")

add_subdirectory(src)
add_subdirectory(tests){% if library %}

install(DIRECTORY "include/" DESTINATION include)
install(EXPORT ${PROJECT_NAME}Config DESTINATION lib/cmake/${PROJECT_NAME}){% endif %}

if (WSBUDOCGEN_FOUND)
    configure_wsbu_doxygen(
            MAINPAGE README.md{% if not cxx %}
            OPTIMIZE_C ON{% endif %}
            INPUT "src" "include"
            STRIP_INC_PATH "include")
endif ()

include({{ name }}CPack.cmake)
