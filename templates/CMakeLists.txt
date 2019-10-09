# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

cmake_minimum_required(VERSION 3.3)

file(STRINGS "version.txt" VERSION)
project({{ name }}{% if not cxx and not tests %} LANGUAGES C{% endif %} VERSION ${VERSION})

option(CONAN "Enable Conan dependency manager" ON)
if (CONAN AND EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    conan_basic_setup(TARGETS NO_OUTPUT_DIRS)
    string(REPLACE ";" ":" RPATHS "${CONAN_LIB_DIRS}"){% if library %}
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath-link,${RPATHS}"){% endif %}{% if executable or tests %}
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-rpath-link,${RPATHS}"){% endif %}
endif ()
{% if tests %}
find_program(VALGRIND_EXE valgrind){% endif %}
find_package(Doxygen QUIET)
find_package(WsbuDocGen QUIET){% if tests %}

enable_testing(){% endif %}{% if library or tests %}
{% endif %}{% if library %}
option(BUILD_SHARED_LIBS "Build dynamic libraries when on, else static" ON){% endif %}{% if tests %}
option(TEST_WITH_VALGRIND "Run unit tests with valgrind (if CMAKE_CROSSCOMPILING_EMULATOR is defined, it will override this setting)" OFF){% endif %}

add_compile_options(-Werror -Wall -Wpedantic -Wconversion)
set(CMAKE_C_STANDARD 99){% if cxx or tests %}
set(CMAKE_CXX_STANDARD 11){% endif %}{% if library %}
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--no-undefined"){% endif %}{% if executable or tests %}
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--disable-new-dtags"){% endif %}

add_subdirectory(src){% if tests %}
add_subdirectory(tests){% endif %}{% if service %}

install(PROGRAMS scripts/{{ name }}.init
        RENAME {{ name }}
        DESTINATION /etc/rc.d/init.d
        COMPONENT system
){% endif %}{% if library %}

install(DIRECTORY "include/"
    DESTINATION include
    COMPONENT dev
)
install(EXPORT ${PROJECT_NAME}Config
    DESTINATION lib/cmake/${PROJECT_NAME}
    NAMESPACE WSBU::
    COMPONENT dev
){% endif %}

if (WSBUDOCGEN_FOUND)
    configure_wsbu_doxygen(
            MAINPAGE README.md{% if not cxx %}
            OPTIMIZE_C ON{% endif %}
            INPUT "src" "include"
            STRIP_INC_PATH "include")
endif ()

include({{ name }}CPack.cmake)
