{{ license_text_for_script }}

import os
import shutil

from conans import ConanFile, CMake, tools


class {{ name }}(ConanFile):
    name = '{{ name | lower }}'
    version = tools.load("version.txt").strip() + '-1'
    license = 'Proprietary'
    description = '{{ description }}'
    homepage = '{{ homepage }}'
    url = '{{ homepage }}'
    topics = 'tag1', 'tag2'
    settings = 'os', 'compiler', 'build_type', 'arch'{% if library %}
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}{% endif %}
    generators = 'cmake_find_package'

    build_requires = (
        'gtest/cci.20210126',
        'doxygen/[^1.8.8]'
    )

    exports = 'version.txt'
    scm = {
        'type': 'git',
        'url': 'auto',
        'revision': 'auto'
    }

    def build(self):
        cmake = self.cmake
        cmake.configure()
        cmake.build(){% if tests %}
        cmake.test(){% endif %}

    def package(self):
        self.cmake.install()
        cmake_config_dir = os.path.join(self.package_folder, 'lib', 'cmake')
        if os.path.exists(cmake_config_dir):
            shutil.rmtree(cmake_config_dir)

        os.makedirs(os.path.join(f'{self.package_folder}', 'licenses'), True)
        shutil.copy2(os.path.join(self.source_folder, 'LICENSE'), os.path.join(f'{self.package_folder}', 'licenses', self.name)){% if library %}

    def package_info(self):
        self.cpp_info.set_property('cmake_file_name', '{{ name }}')
        self.cpp_info.set_property('cmake_target_name', '{{ name }}')
        self.cpp_info.components['{{ lib_target_name }}'].libs = ['{{ name | lower }}']{% endif %}

    @property
    def cmake(self):
        return CMake(self)
