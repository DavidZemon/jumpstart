# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

# This file is configured at cmake time, and loaded at cpack time. To pass variables to cpack from cmake, they must be
# configured in this file.

string(TOLOWER "${CPACK_PACKAGE_NAME}" PACKAGE_NAME_LOWER)

# Special DEB settings
execute_process(COMMAND dpkg --print-architecture OUTPUT_VARIABLE DEB_ARCH)
string(STRIP "${DEB_ARCH}" DEB_ARCH)
set(CPACK_DEBIAN_PRODUCTION_PACKAGE_FILE_NAME "${PACKAGE_NAME_LOWER}_${CPACK_PACKAGE_VERSION}-${CPACK_DEBIAN_PACKAGE_RELEASE}_${DEB_ARCH}.deb")
set(CPACK_DEBIAN_DEV_PACKAGE_DEPENDS "${PACKAGE_NAME_LOWER}=${CPACK_PACKAGE_VERSION}-${CPACK_DEBIAN_PACKAGE_RELEASE}")

# Special RPM settings
execute_process(COMMAND uname -m OUTPUT_VARIABLE RPM_ARCH)
string(STRIP "${RPM_ARCH}" RPM_ARCH)
set(CPACK_RPM_DEV_FILE_NAME "${PACKAGE_NAME_LOWER}-devel-${CPACK_PACKAGE_VERSION}-${CPACK_RPM_PACKAGE_RELEASE}.${RPM_ARCH}.rpm")
set(CPACK_RPM_DEV_PACKAGE_REQUIRES "${PACKAGE_NAME_LOWER}=${CPACK_PACKAGE_VERSION}-${CPACK_RPM_PACKAGE_RELEASE}")

# Special archive settings
set(CPACK_ARCHIVE_PRODUCTION_PACKAGE_FILE_NAME "${CPACK_PACKAGE_FILE_NAME}${extension}")

if (NOT CPACK_GENERATOR MATCHES "(DEB|RPM)")
    set(CPACK_COMPONENTS_ALL dev Unspecified)
endif()
