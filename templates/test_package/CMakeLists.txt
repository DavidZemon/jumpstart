{{ license_text_for_script }}

cmake_minimum_required(VERSION 3.9)

project({{ name }}TestConan)

find_package({{ name }} REQUIRED)

set(CMAKE_CXX_STANDARD 11)
add_executable(${PROJECT_NAME} ${PROJECT_NAME})
target_link_libraries(${PROJECT_NAME} PUBLIC {{ name }}::{{ lib_target_name }})

enable_testing()
add_test(NAME ${PROJECT_NAME}
        COMMAND ${CMAKE_CROSSCOMPILING_EMULATOR} "$<TARGET_FILE:${PROJECT_NAME}>")
