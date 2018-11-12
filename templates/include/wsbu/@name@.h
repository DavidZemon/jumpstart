/**
 * @file wsbu/{{ name }}.h
 *{% if not cxx %}
 * TODO: Describe the module in detail here
 *{% endif %}
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */

#ifndef WSBU_{{ name | upper }}_H
#define WSBU_{{ name | upper }}_H

{% spaceless %}
{% if not cxx %}
#ifdef __cplusplus
extern "C" {
#endif

void say_hi();

#ifdef __cplusplus
};
#endif
{% else %}

/**
 * This class isn't very useful.
 *
 * This is a longer description of a very useless class.
 */
class HelloPrinter {
    public:
        /**
         * Print a short message to stdout
         *
         * The C++ STL is used for printing "Hello" to stdout via the `cout` stream. Isn't that cool?
         */
        void say_hi ();
};

{% endif %}
{% endspaceless %}

#endif //WSBU_{{ name | upper }}_H
