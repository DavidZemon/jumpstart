/**
 * @file {{ name }}TestConan.cpp
 *
{{ license_text_for_cxx }}
 */

#include <{{ namespace }}/{{ name }}.h>

int main () {{ '{' }}{% if cxx %}
    const {{ name }} instance;
    return 3 != instance.add(1, 2);{% else %}
    return 3 != add(1, 2);{% endif %}
}
