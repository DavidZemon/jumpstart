{{ license_text_for_script }}

from conans import ConanFile, CMake, tools, RunEnvironment


class {{ name }}Test(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            self.run('ctest --output-on-failure')
