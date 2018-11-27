/**
 * @file {{ name }}-cliTest.cpp
 *
 * @copyright (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered
 * trademarks of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.
 */

#include <gtest/gtest.h>
#include "{{ name }}-cli.h"

TEST ({{ name }}CliTest, does_not_fail) {
    ASSERT_EQ(0, run());
}
