# Copyright {% now "Y" %} {{ copyright }}
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
