from conans import tools, ConanFile, CMake

import os


class SDLMixerConan(ConanFile):
    name = 'SDL_mixer'
    version = '2.0.4'
    description = 'SDL_mixer is a sample multi-channel audio mixer library'
    homepage = 'http://www.libsdl.org/projects/SDL_mixer/'
    license = 'zlib'
    url = 'https://github.com/conan-burrito/SDL_mixer'

    generators = 'cmake', 'cmake_find_package_multi'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
        'ogg': [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'ogg': True
    }

    build_policy = 'missing'

    exports_sources = ['CMakeLists.txt', 'patches/*']

    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    @property
    def source_subfolder(self):
        return 'src'

    @property
    def build_subfolder(self):
        return "_build"

    def requirements(self):
        self.requires("SDL2/2.0.12@conan-burrito/stable")

        if self.options.ogg:
            self.requires("ogg/1.3.4@conan-burrito/stable")
            self.requires("vorbis/1.3.7@conan-burrito/stable")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("SDL2_mixer-{}".format(self.version), self.source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.definitions["SDM_VERSION_STRING"] = self.version
        self._cmake.definitions["SDM_VERSION_MAJOR"] = self.version.split(".")[0]

        self._cmake.definitions['WITH_FLAC'] = 'OFF'
        self._cmake.definitions['WITH_MICMOD'] = 'OFF'
        self._cmake.definitions['WITH_MODPLUG'] = 'OFF'
        self._cmake.definitions['WITH_OGG'] = 'ON' if self.options.ogg else 'OFF'
        self._cmake.definitions['WITH_MPEG'] = 'OFF'
        self._cmake.definitions['WITH_OPUS'] = 'OFF'
        self._cmake.definitions['WITH_MAD'] = 'OFF'
        self._cmake.definitions['WITH_CMD'] = 'OFF'

        self._cmake.configure(build_folder=self.build_subfolder)
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("COPYING", src=self.source_subfolder, dst="licenses", keep_path=False)
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        # SDL_mixer
        self.cpp_info.libs.append('SDL2_mixer')

        self.cpp_info.names["cmake_find_package"] = "SDL_mixer"
        self.cpp_info.names["cmake_find_package_multi"] = "SDL_mixer"

