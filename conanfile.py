import os

from conans import ConanFile, CMake, tools

class ShadercConan(ConanFile):
    name = "shaderc"
    description = "A collection of tools, libraries and tests for shader compilation."
    license = "Apache-2.0"
    topics = ("conan", "shaderc", "glsl", "hlsl", "msl", "spirv", "spir-v", "glslc", "spvc")
    homepage = "https://github.com/google/shaderc"
    url = "https://github.com/conan-io/conan-center-index"
    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 11)

    def requirements(self):
        self.requires.add("glslang/8.13.3559")
        self.requires.add("spirv-tools/2020.1")
        # if self.options.spvc:
        #    self.requires.add("spirv-cross/20200403")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["SHADERC_ENABLE_SPVC"] = False # spvc depends on private headers of SPIRV-Tools, making it hard to enable for conan
        self._cmake.definitions["SHADERC_SKIP_INSTALL"] = False
        self._cmake.definitions["SHADERC_SKIP_TESTS"] = True
        self._cmake.definitions["SHADERC_SPVC_ENABLE_DIRECT_LOGGING"] = False
        self._cmake.definitions["SHADERC_SPVC_DISABLE_CONTEXT_LOGGING"] = False
        self._cmake.definitions["SHADERC_ENABLE_WERROR_COMPILE"] = False
        if self.settings.compiler == "Visual Studio":
            self._cmake.definitions["SHADERC_ENABLE_SHARED_CRT"] = str(self.settings.compiler.runtime).startswith("MD")
        self._cmake.definitions["ENABLE_CODE_COVERAGE"] = False
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.append("pthread")
        if self.options.shared:
            self.cpp_info.defines.append("SHADERC_SHAREDLIB")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
