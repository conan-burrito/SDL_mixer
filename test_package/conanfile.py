from conans import tools, ConanFile, CMake
import os


class Test(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'

    generators = 'cmake', 'cmake_find_package_multi'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            self.run(os.path.join('bin', 'test'), run_environment=True)

        if self.settings.os == 'Emscripten':
            self.run("node %s" % os.path.join("bin", "test"), run_environment=True)
