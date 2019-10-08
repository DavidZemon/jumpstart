# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

# This file is configured at cmake time, and loaded at cpack time. To pass variables to cpack from cmake, they must be
# configured in this file.

string(TOLOWER "${CPACK_PACKAGE_NAME}" PACKAGE_NAME_LOWER)
execute_process(COMMAND dpkg --print-architecture
    OUTPUT_VARIABLE ARCH
)
string(STRIP "${ARCH}" ARCH)
if (CPACK_GENERATOR STREQUAL DEB)
    set(CPACK_DEBIAN_PRODUCTION_PACKAGE_FILE_NAME "${PACKAGE_NAME_LOWER}_${CPACK_PACKAGE_VERSION}-${CPACK_DEBIAN_PACKAGE_RELEASE}_${ARCH}.deb")
elseif (CPACK_GENERATOR STREQUAL RPM)
else ()
    set(CPACK_ARCHIVE_PRODUCTION_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}${extension}")
    set(CPACK_COMPONENTS_ALL dev Unspecified)
endif()
