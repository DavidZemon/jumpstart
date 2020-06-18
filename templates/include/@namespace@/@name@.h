/**
 * @file {% if library %}{{ namespace }}/{% endif %}{{ name }}.h
 *{% if not cxx %}
 * TODO: Describe the module in detail here
 *{% endif %}
{{ license_text_for_cxx }}
 */

#pragma once

{% spaceless %}
{% if not cxx %}
#ifdef __cplusplus
extern "C" {
#endif

int add (int lhs, int rhs);

#ifdef __cplusplus
}
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
        [[nodiscard]] int add (int lhs, int rhs) const;
};

{% endif %}
{% endspaceless %}
