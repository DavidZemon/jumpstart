/**
 * @file {% if library %}{{ namespace }}/{% endif %}{{ name }}.h
 *{% if not cxx %}
 * TODO: Describe the module in detail here
 *{% endif %}
 * Copyright {% now "Y" %} {{ copyright }}
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
 * Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
 * WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
