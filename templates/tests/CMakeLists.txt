find_package({{ test_package_name }} REQUIRED)

add_custom_target(test-all
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    WORKING_DIRECTORY "${PROJECT_BINARY_DIR}")

function(create_test NAME)
    if (DEFINED ENV{TC_GTEST_OUTPUT_DIR})
        set(XML_OUTPUT_ARG "--gtest_output=xml:${CMAKE_BINARY_DIR}/$ENV{TC_GTEST_OUTPUT_DIR}/${NAME}.xml")
    endif ()

    add_executable(${NAME} ${ARGN})
    target_include_directories(${NAME} PRIVATE ${{ '{' }}{{ test_package_name | upper }}_INCLUDE_DIRS}){% if executable %}
    target_link_libraries(${NAME} {{ name | lower }}-lib ${{ '{' }}{{ test_package_name | upper }}_BOTH_LIBRARIES} pthread){% else %}
    target_link_libraries(${NAME} {{ name | lower }} ${{ '{' }}{{ test_package_name | upper }}_BOTH_LIBRARIES} pthread){% endif %}
    add_test(NAME ${NAME}
        COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${NAME}>" ${XML_OUTPUT_ARG})
    add_custom_target(test-${NAME}
        COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure -R "${NAME}"
        DEPENDS ${NAME}
    )
    add_dependencies(test-all ${NAME})
endfunction()

create_test({{ name }}Test {{ name }}Test{{ extension }})
