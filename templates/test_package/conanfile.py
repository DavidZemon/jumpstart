{{ license_text_for_script }}

from conans import ConanFile, CMake


class {{ name }}Test(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake_find_package'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run('ctest --output-on-failure', run_environment=True)
