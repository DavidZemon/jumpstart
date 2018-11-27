/**
 * @file {{ name }}TestConan.cpp
 *
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */

#include <wsbu/{{ name }}.h>

int main () {{ '{' }}{% if cxx %}
    const {{ name }} instance;
    return 3 != instance.add(1, 2);{% else %}
    return 3 != add(1, 2);{% endif %}
}
