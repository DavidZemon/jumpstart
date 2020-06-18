/**
 * @file {{ name }}-cliTest.cpp
 *
{{ license_text_for_cxx }}
 */

#include "{{ name }}-cli.h"

#include <gmock/gmock.h>

// NOLINTNEXTLINE
TEST ({{ name }}CliTest, does_not_fail) {
    ASSERT_EQ(0, run());
}
