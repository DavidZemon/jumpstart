{% spaceless %}
{% if library %}
add_library({{ lib_target_name }} {{ name }}{{ extension }})
target_include_directories({{ lib_target_name }} PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
    $<INSTALL_INTERFACE:include>
)
{% spaceless %}
{% if executable %}
set_target_properties({{ lib_target_name }} PROPERTIES OUTPUT_NAME {{ name | lower }})
{% endif %}
{% endspaceless %}
install(TARGETS {{ lib_target_name }} EXPORT ${PROJECT_NAME}Config DESTINATION lib)
{% endif %}
{% spaceless %}
{% if executable %}
{% spaceless %}
{% if library %}
add_library({{ name | lower }}-cli-lib STATIC {{ name }}-cli{{ extension }})
target_link_libraries({{ name }} {{ lib_target_name }})

add_executable({{ name | lower }} main{{ extension }})
target_link_libraries({{ name }} {{ name | lower }}-cli-lib)
{% else %}
add_library({{ name | lower }}-lib STATIC {{ name }}{{ extension }})

add_executable({{ name | lower }} main{{ extension }})
target_link_libraries({{ name | lower }} {{ name | lower }}-lib)
{% endif %}
{% endspaceless %}
install(TARGETS {{ name | lower }} EXPORT ${PROJECT_NAME}Config DESTINATION bin)
{% endif %}
{% endspaceless %}
{% endspaceless %}
