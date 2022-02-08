{{ license_text_for_script }}

cmake_minimum_required(VERSION 3.9)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_BINARY_DIR}")
file(STRINGS "version.txt" VERSION)
project({{ name }}{% if not cxx and not tests %} LANGUAGES C{% endif %} VERSION ${VERSION})

# Configure SonarQube properties file
if (DEFINED ENV{CI_GTEST_OUTPUT_DIR})
    set(GTEST_OUTPUT_DIR "${CMAKE_BINARY_DIR}/$ENV{CI_GTEST_OUTPUT_DIR}")
else ()
    set(GTEST_OUTPUT_DIR "${CMAKE_BINARY_DIR}/gtest_output")
endif ()
# Don't use PROJECT_SOURCE_DIR in the properties file because paths get changed up when in Docker
file(RELATIVE_PATH RELATIVE_SOURCE_ROOT "${CMAKE_CURRENT_BINARY_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}")
configure_file(sonar-project.properties.in sonar-project.properties @ONLY)

find_package(Doxygen QUIET){% if tests %}

enable_testing(){% endif %}{% if library or tests %}
{% endif %}{% if library %}
option(BUILD_SHARED_LIBS "Build dynamic libraries when on, else static" ON){% endif %}{% if tests %}
option(TEST_WITH_VALGRIND "Run unit tests with valgrind (if CMAKE_CROSSCOMPILING_EMULATOR is defined, it will override this setting)" OFF)
option(HTML_COVERAGE_REPORT "When enabled, test coverage will be reported in HTML format for human consumption. When disable, coverage will be reported in XML for use with SonarQube." ON){% endif %}

add_compile_options(-Werror -Wall -Wpedantic -Wconversion){% if tests %}
set(CMAKE_C_FLAGS_DEBUG   "${CMAKE_C_FLAGS_DEBUG} --coverage")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} --coverage"){% endif %}
set(CMAKE_C_STANDARD 99){% if cxx or tests %}
set(CMAKE_CXX_STANDARD 17){% endif %}{% if library %}
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--no-undefined"){% endif %}

find_program(CPPCHECK_EXE cppcheck)
if (CPPCHECK_EXE)
    message("-- Program cppcheck found: ${CPPCHECK_EXE}")
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    add_custom_target(cppcheck
        COMMAND "${CPPCHECK_EXE}" --std=c{% if cxx or tests %}++{% endif %}${CMAKE_CXX_STANDARD} --enable=all --quiet "--project=${PROJECT_BINARY_DIR}/compile_commands.json")
endif ()

find_program(CLANG_TIDY_EXE clang-tidy)
if (CLANG_TIDY_EXE)
    message("-- Program clang-tidy found: ${CLANG_TIDY_EXE}")
    set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
    set(CMAKE_C_CLANG_TIDY "${CLANG_TIDY_EXE}" --quiet "-header-filter=${PROJECT_SOURCE_DIR}/(include/{{ namespace }}|src|tests)/.*" -p "${PROJECT_BINARY_DIR}/compile_commands.json"){% if cxx or tests %}
    set(CMAKE_CXX_CLANG_TIDY "${CMAKE_C_CLANG_TIDY}"){% endif %}
endif ()

add_subdirectory(src){% if tests %}
add_subdirectory(tests){% endif %}{% if service %}

install(PROGRAMS scripts/{{ name }}.init
        RENAME {{ name }}
        DESTINATION /etc/rc.d/init.d
        COMPONENT system){% endif %}{% if library %}

install(DIRECTORY "include/"
    DESTINATION include
    COMPONENT dev)
install(EXPORT ${PROJECT_NAME}Config
    DESTINATION lib/cmake/${PROJECT_NAME}
    NAMESPACE {{ name }}::
    COMPONENT dev){% endif %}

if (TARGET Doxygen::doxygen)
    set(DOXYGEN_USE_MDFILE_AS_MAINPAGE "README.md")
    set(DOXYGEN_STRIP_INC_PATH "include"){% if not cxx %}
    set(DOXYGEN_OPTIMIZE_C ON){% endif %}
    doxygen_add_docs(docs "README.md" "src" "include")
endif ()

include({{ name }}CPack.cmake)
