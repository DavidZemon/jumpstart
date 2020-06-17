# Copyright {% now "Y" %} {{ copyright }}
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

find_package(GTest REQUIRED
    PATHS "${CONAN_GOOGLETEST_ROOT}")

add_custom_target(test-all
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    WORKING_DIRECTORY "${PROJECT_BINARY_DIR}")

find_program(GCOVR_EXE gcovr)
if (GCOVR_EXE)
    if (HTML_COVERAGE_REPORT)
        set(COVERAGE_TYPE html)
    else ()
        set(COVERAGE_TYPE xml)
    endif ()
    set(COVERAGE_COMMAND "${GCOVR_EXE}" --${COVERAGE_TYPE} --output "${PROJECT_BINARY_DIR}/coverage.${COVERAGE_TYPE}" --root "${PROJECT_SOURCE_DIR}")
    set(COVERAGE_COMMENT "Generating test coverage report.")

    # For use after testing was already done as a separate step, allowing you to
    # generate reports without re-running tests
    add_custom_target(report-coverage
        COMMAND ${COVERAGE_COMMAND}
        COMMENT "${COVERAGE_COMMENT}")
    # This target will execute tests and generate coverage reports as a single step
    add_custom_target(test-coverage
        COMMAND ${COVERAGE_COMMAND}
        COMMENT "${COVERAGE_COMMENT}"
        DEPENDS test-all)
endif ()
{% if library and executable %}
function(create_test NAME LIB){% else %}
function(create_test NAME){% endif %}
    set(XML_OUTPUT_ARG "--gtest_output=xml:${GTEST_OUTPUT_DIR}/${NAME}.xml")

    add_executable(${NAME} ${ARGN}){% if library and executable %}
    target_link_libraries(${NAME} ${LIB} GTest::{{ test_package_name | lower }}_main){% elif executable %}
    target_link_libraries(${NAME} {{ name | lower }}-lib GTest::{{ test_package_name | lower }}_main){% else %}
    target_link_libraries(${NAME} {{ name | lower }} GTest::{{ test_package_name | lower }}_main){% endif %}
    if (DEFINED CMAKE_CROSSCOMPILING_EMULATOR)
        add_test(NAME ${NAME}
            COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
    elseif (VALGRIND_EXE AND TEST_WITH_VALGRIND)
        # Valgrind isn't smart enough to create directories that don't exist
        file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/valgrind")
        add_test(NAME ${NAME}
            COMMAND "${VALGRIND_EXE}" --leak-check=full --leak-resolution=med  --track-origins=yes --vgdb=no
                --xml=yes "--xml-file=${CMAKE_BINARY_DIR}/valgrind/${NAME}-valgrind.xml" --error-exitcode=1
                "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
    else ()
        add_test(NAME ${NAME}
            COMMAND "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
    endif ()
    add_custom_target(test-${NAME}
        COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure -R "${NAME}"
        DEPENDS ${NAME}
    )
    add_dependencies(test-all ${NAME})
endfunction()
{% if library and executable %}
create_test({{ name }}Test {{ name | lower }}-lib {{ name }}Test.cpp)
create_test({{ name }}-cliTest {{ name | lower }}-cli-lib {{ name }}-cliTest.cpp){% elif library %}
create_test({{ name }}Test {{ name }}Test.cpp){% else %}
create_test({{ name }}Test {{ name }}Test.cpp)
create_test({{ name }}-cliTest {{ name }}-cliTest.cpp){% endif %}
