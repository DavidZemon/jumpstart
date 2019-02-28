# (C){% now "Y" %} Red Lion Controls, Inc. All rights reserved. Red Lion, the Red Lion logo and Sixnet are registered trademarks
# of Red Lion Controls, Inc. All other company and product names are trademarks of their respective owners.

from conans import ConanFile, CMake, tools


class {{ name }}(ConanFile):
    name = '{{ name }}'
    version = tools.load("version.txt").strip() + '-1'
    license = 'Proprietary'
    url = 'https://bitbucket.org/redlionstl/{{ name | lower }}'
    description = '{{ description }}'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        {% if library %}'shared': [True, False],
        {% endif %}'with_docs': [True, False],
        'public_docs': [True, False]
    }
    default_options = {% if library %}'shared=True', {% endif %}'with_docs=True', 'public_docs=False'
    generators = 'cmake'

    build_requires = (
        'googletest/1.8.1@wsbu/stable',
        'wsbu-docgen/[^0.1.3]@wsbu/stable'
    )

    exports = 'version.txt'
    scm = {
        'type': 'git',
        'url': 'auto',
        'revision': 'auto'
    }

    def configure(self):
        # Googletest should never be built as a shared library... it's just all kinds of broken
        self.options['googletest'].shared = False

    def build(self):
        cmake = self.cmake
        if self.options.with_docs:
            cmake_defs = {
                'WSBU_DOX_INSTALL': 'ON',
                'WSBU_DOX_PUBLIC': 'ON' if self.options.public_docs else 'OFF'
            }
        else:
            cmake_defs = {}
        cmake.configure(defs=cmake_defs)
        cmake.build()
        cmake.test()

    def package(self):
        self.cmake.install(){% if library %}

    def package_info(self):
        self.cpp_info.libs = ['{{ name | lower }}']{% endif %}

    @property
    def cmake(self):
        return CMake(self)
