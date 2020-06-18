{{ license_text_for_script }}

set(CPACK_GENERATOR
    TGZ
    ZIP
)

find_program(RPMBUILD rpmbuild)
if (RPMBUILD)
    list(APPEND CPACK_GENERATOR RPM)
endif ()

find_program(DEBUILD debuild)
if (DEBUILD)
    list(APPEND CPACK_GENERATOR DEB)
endif ()

set(CPACK_PROJECT_URL "{{ homepage }}")
set(CPACK_PACKAGE_VENDOR "{{ copyright }}")
set(CPACK_PACKAGE_CONTACT "{{ contact | safe }}")
set(CPACK_PACKAGE_VERSION_MAJOR ${PROJECT_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${PROJECT_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${PROJECT_VERSION_PATCH})
set(CPACK_PACKAGE_VERSION
    ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH})
if (PROJECT_VERSION_TWEAK)
    set(CPACK_PACKAGE_VERSION ${CPACK_PACKAGE_VERSION}.${PROJECT_VERSION_TWEAK})
endif ()
set(CPACK_PACKAGE_RELOCATABLE ON)

# Debian Specific
set(CPACK_DEBIAN_PACKAGE_HOMEPAGE                   "${CPACK_PROJECT_URL}")
set(CPACK_DEBIAN_PACKAGE_DEPENDS                    )
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS                  ON)
set(CPACK_DEBIAN_PACKAGE_RELEASE                    1)
set(CPACK_DEBIAN_FILE_NAME                          DEB-DEFAULT)
set(CPACK_DEBIAN_PACKAGE_CONTROL_STRICT_PERMISSION  ON)

# RPM Specific
set(CPACK_RPM_PACKAGE_URL                       "${CPACK_PROJECT_URL}")
set(CPACK_RPM_PACKAGE_REQUIRES                  )
set(CPACK_RPM_FILE_NAME                         RPM-DEFAULT)
set(CPACK_RPM_RELOCATION_PATHS                  /)
set(CPACK_RPM_MAIN_COMPONENT                    production_package)
set(CPACK_RPM_PACKAGE_RELEASE                   ${CPACK_DEBIAN_PACKAGE_RELEASE})

# Components
set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
set(CPACK_DEB_COMPONENT_INSTALL     ON)
set(CPACK_RPM_COMPONENT_INSTALL     ON)

set(CPACK_COMPONENT_dev_NAME        "Development headers/libraries")
set(CPACK_COMPONENT_dev_DESCRIPTION "Headers, static libraries, build system files for {{ name }}")

set(CPACK_PROJECT_CONFIG_FILE "${PROJECT_SOURCE_DIR}/{{ name }}CPackOptions.cmake")
include(CPack)

# Bundle the system and "Unspecified" components together for the sake fo the DEB and RPM packages
cpack_add_component_group(production_package)
cpack_add_component(Unspecified GROUP production_package){% if service %}
cpack_add_component(system      GROUP production_package){% endif %}
