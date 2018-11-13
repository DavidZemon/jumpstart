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

int add (const int lhs, const int rhs);

#ifdef __cplusplus
};
#endif
{% else %}

/**
 * This class isn't very useful.
 *
 * This is a longer description of a very useless class.
 */
class {{ name }} {
    public:
        /**
         * Add two numbers.
         *
         * This is, by far, the fanciest addition you have ever seen.
         *
         * @param[in]   lhs     The left-hand side argument for addition
         * @param[in]   rhs     The right-hand side argument for addition
         *
         * @return      Sum of lhs and rhs
         */
        int add (const int lhs, const int rhs) const;
};

{% endif %}
{% endspaceless %}

#endif //WSBU_{{ name | upper }}_H
