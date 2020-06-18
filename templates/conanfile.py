{{ license_text_for_script }}

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
    default_options = {% if library %}'shared=True', {% endif %}'with_docs=True', 'public_docs=True'
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
