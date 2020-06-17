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
    url = '{{ homepage }}'
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
        'gtest/[^1.10.0]@davidzemon/stable',
        'docgen/[^0.1.4]@davidzemon/stable'
    )

    exports = 'version.txt'
    scm = {
        'type': 'git',
        'url': 'auto',
        'revision': 'auto'
    }

    def build(self):
        cmake = self.cmake
        if self.options.with_docs:
            cmake_defs = {
                'DOX_INSTALL': 'ON',
                'DOX_PUBLIC': 'ON' if self.options.public_docs else 'OFF'
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
