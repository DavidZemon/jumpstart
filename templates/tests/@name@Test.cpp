/**
 * @file {{ name }}Test.cpp
 *
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */

#include <gtest/gtest.h>
#include <{% if library %}wsbu/{% endif %}{{ name }}.h>

class {{ name }}Test : public ::testing::Test
{
    public:
        // TODO: Replace this constructor with any setup functionality you need
        {{ name }}Test() = default;

        // TODO: Replace this destructor with any teardown functionality you need
        ~{{ name }}Test() override = default;{% if cxx %}

    protected:
        {{ name }} testable;{% endif %}
};

// NOLINTNEXTLINE
TEST_F ({{ name }}Test, can_add) {{ '{' }} {%if cxx %}
    ASSERT_EQ(3, testable.add(1, 2));{% else %}
    ASSERT_EQ(3, add(1, 2));{% endif %}
}
