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
