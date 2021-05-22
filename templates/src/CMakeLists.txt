{{ license_text_for_script }}

cmake_minimum_required(VERSION 3.9)

{% if library %}
add_library({{ lib_target_name }} {{ name }}{{ extension }})
target_include_directories({{ lib_target_name }} PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
    $<INSTALL_INTERFACE:include>
)
{% if executable %}
set_target_properties({{ lib_target_name }} PROPERTIES OUTPUT_NAME {{ name | lower }}){% endif %}
install(TARGETS {{ lib_target_name }} EXPORT ${PROJECT_NAME}Config DESTINATION lib)
{% endif %}{% if executable %}{% if library %}
add_library({{ name | lower }}-cli-lib STATIC {{ name }}-cli{{ extension }})
target_include_directories({{ name | lower }}-cli-lib INTERFACE "${CMAKE_CURRENT_LIST_DIR}")
target_link_libraries({{ name | lower }}-cli-lib {{ lib_target_name }})

add_executable({{ name | lower }} main{{ extension }})
target_link_libraries({{ name | lower }} {{ name | lower }}-cli-lib){% else %}
{% if tests %}
add_library({{ name | lower }}-lib STATIC
    {{ name }}-cli{{ extension }}
    {{ name }}{{ extension }}
)
target_include_directories({{ name | lower }}-lib INTERFACE "${CMAKE_CURRENT_LIST_DIR}")

{% endif %}add_executable({{ name | lower }} main{{ extension }}){% if tests %}
target_link_libraries({{ name | lower }} {{ name | lower }}-lib){% endif %}{% endif %}
install(TARGETS {{ name | lower }} DESTINATION bin){% endif %}
