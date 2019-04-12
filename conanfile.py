from conans import ConanFile, CMake, tools


class SeastarConan(ConanFile):
    name = "Seastar"
    version = "0.1"
    license = "Apache 2.0"
    author = "Najjar Chedy najjarchedy@gmail.com"
    url = "https://github.com/cppchedy/seastar_rec"
    description = "Seastar a high perfermance framework for server application"
    topics = ("server", "backend", "network")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/scylladb/seastar.git")
        self.run("cd seastar && git checkout d863ed682c66d10a2b2f3afa8725fd91fa5bceb5")


    def build(self):
        #cmake = CMake(self)
        #cmake.configure(source_folder="hello")
        #cmake.build()

        # Explicit way:
        print(self.source_folder)
        self.run('export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%s/build/_cooking/installed/lib' 
                    % self.source_folder)
        self.run('ls %s/seastar' % self.source_folder)
        self.run('ls %s/seastar' % self.build_folder)
        self.run('.%s/seastar/cooking.sh -- -DSeastar_DPDK=ON -DCMAKE_BUILD_TYPE=Release' % self.build_folder)

    def package(self):
        self.copy("*.h", dst="include", src="seastar")
        self.copy("*seastar.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

