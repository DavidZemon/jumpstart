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
endif ()

find_package(Doxygen QUIET)
find_package(WsbuDocGen QUIET)

enable_testing()

option(BUILD_SHARED_LIBS "Build dynamic libraries when on, else static" ON)

add_subdirectory(src)
add_subdirectory(tests)
{% if library %}
install(DIRECTORY "include/" DESTINATION include){% endif %}
install(EXPORT ${PROJECT_NAME}Config DESTINATION lib/cmake/${PROJECT_NAME})

if (WSBUDOCGEN_FOUND)
    configure_wsbu_doxygen(
            MAINPAGE README.md
            INPUT "src" "include"
            STRIP_INC_PATH "include")
endif ()

include({{ name }}CPack.cmake)
