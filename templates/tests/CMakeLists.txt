# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

find_package(GTest REQUIRED
    PATHS "${CONAN_GOOGLETEST_ROOT}")

add_custom_target(test-all
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    WORKING_DIRECTORY "${PROJECT_BINARY_DIR}")
{% if library and executable %}
function(create_test NAME LIB){% else %}
function(create_test NAME){% endif %}
    if (DEFINED ENV{TC_GTEST_OUTPUT_DIR})
        set(XML_OUTPUT_ARG "--gtest_output=xml:${CMAKE_BINARY_DIR}/$ENV{TC_GTEST_OUTPUT_DIR}/${NAME}.xml")
    endif ()

    add_executable(${NAME} ${ARGN}){% if library and executable %}
    target_link_libraries(${NAME} ${LIB} GTest::{{ test_package_name | lower }}_main){% elif executable %}
    target_link_libraries(${NAME} {{ name | lower }}-lib GTest::{{ test_package_name | lower }}_main){% else %}
    target_link_libraries(${NAME} {{ name | lower }} GTest::{{ test_package_name | lower }}_main){% endif %}
    if (DEFINED CMAKE_CROSSCOMPILING_EMULATOR)
        add_test(NAME ${NAME}
            COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
    elseif (VALGRIND_EXE AND TEST_WITH_VALGRIND)
        add_test(NAME ${NAME}
            COMMAND "${VALGRIND_EXE}" --leak-check=full --leak-resolution=med  --track-origins=yes --vgdb=no
                --error-exitcode=1 "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
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
