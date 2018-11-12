/*!
 * @file {{ name }}Test.cpp
 *
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */

#include <gtest/gtest.h>
#include <wsbu/{{ name }}.h>

class {{ name }}Test : public ::testing::Test
{
    public:
        {{ name }}Test() {
            // TODO: Test setup goes here
        }

        virtual ~{{ name }}Test() {
            // TODO: Test teardown goes here
        }{% if cxx %}

    protected:
        {{ name }} testable;{% endif %}
};

TEST_F ({{ name }}Test, say_hi) {{ '{' }}{%if cxx %}
    ASSERT_EQ(3, testable.add(1, 2));{% else %}
    ASSERT_EQ(3, add(1, 2));{% endif %}
}
