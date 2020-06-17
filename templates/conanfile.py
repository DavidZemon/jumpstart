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
        'googletest/[^1.8.1]@wsbu/stable',
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
        cmake.build(){% if tests %}
        cmake.test(){% endif %}

    def package(self):
        self.cmake.install(){% if library %}

    def package_info(self):
        self.cpp_info.libs = ['{{ name | lower }}']{% endif %}

    @property
    def cmake(self):
        return CMake(self)
