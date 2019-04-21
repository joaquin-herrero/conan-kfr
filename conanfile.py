from conans import ConanFile, CMake, tools


class KfrConan(ConanFile):
    name = "kfr"
    version = "3.0.9"
    license = "GPL-2.0"
    author = "Joaquin Herrero <replicante87@gmail.com>"
    url = "https://github.com/joaquin-herrero/conan-kfr"
    description = "KFR is an open source C++ DSP framework that focuses on high performance"
    topics = ("dsp", "audio")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "tests": [True, False], "dft": [True, False]}
    default_options = "shared=True", "tests=False", "dft=True"
    generators = "cmake"

    def source(self):
        zip_file = "%s.zip" % self.version
        url = "https://github.com/kfrlib/kfr/archive/%s" % zip_file
        
        tools.download(url, zip_file, verify=False)
        tools.unzip(zip_file)

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        source_path = "%s-%s" % (self.name, self.version)
        cmakelists_path = "%s/CMakeLists.txt" % source_path
        tools.replace_in_file(cmakelists_path, "project(kfr CXX)",
                              '''project(kfr CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        source_path = "%s-%s" % (self.name, self.version)

        cmake = CMake(self)
        cmake.definitions["ENABLE_TESTS"] = self.options.tests
        if self.settings.compiler == "apple-clang":
            cmake.definitions["ENABLE_DFT"] = self.options.dft
        cmake.configure(source_folder=source_path)
        cmake.build()

    def package(self):
        source_path = "%s-%s" % (self.name, self.version)
        include_dir = "%s/include" % source_path

        self.copy("*.h", dst="include", src=include_dir)
        self.copy("*.hpp", dst="include", src=include_dir)
        self.copy("*.i", dst="include", src=include_dir)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

