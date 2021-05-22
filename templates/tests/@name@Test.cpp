/**
 * @file {{ name }}Test.cpp
 *
{{ license_text_for_cxx }}
 */

#include <{% if library %}{{ namespace }}/{% endif %}{{ name }}.h>

#include <gmock/gmock.h>

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
