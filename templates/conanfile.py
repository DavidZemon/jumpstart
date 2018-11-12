from conans import ConanFile, CMake, tools


class {{ name }}Conan(ConanFile):
    name = '{{ name }}'
    version = tools.load("version.txt").strip() + '-1'
    license = 'Proprietary'
    url = 'https://bitbucket.org/redlionstl/{{ name | lower }}'
    description = '{{ description }}'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'

    build_requires = (
        'googletest/1.8.0@wsbu/stable',
        'wsbu-docgen/[^0.1.0]@wsbu/stable'
    )

    exports = 'version.txt'
    exports_sources = '*', '!bin/*', '!build/*', '!cmake-build-*', '!.idea/*'

    def configure(self):
        # Googletest should never be built as a shared library... it's just all kinds of broken
        self.options['googletest'].shared = False

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '/'
        cmake.configure()
        cmake.build()

    def package(self):
        self.run('cmake --build {0} --target install -- DESTDIR={1}'.format(self.build_folder, self.package_folder)){% if library %}

    def package_info(self):
        self.cpp_info.libs = ['{{ name | lower }}']{% endif %}
