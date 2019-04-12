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
    logworkaround = """
#!/bin/bash
# Abort on Error
set -e

export PING_SLEEP=30s
export WORKDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export BUILD_OUTPUT=$WORKDIR/build.out

touch $BUILD_OUTPUT

dump_output() {
   echo Tailing the last 500 lines of output:
   tail -500 $BUILD_OUTPUT  
}
error_handler() {
  echo ERROR: An error was encountered with the build.
  dump_output
  exit 1
}
# If an error occurs, run our error handler to output a tail of the build
trap error_handler ERR

# Set up a repeating loop to send some output to Travis.

bash -c "while true; do echo \$(date) - building ...; sleep $PING_SLEEP; done" &
PING_LOOP_PID=$!

# My build is using maven, but you could build anything with this, E.g.
# your_build_command_1 >> $BUILD_OUTPUT 2>&1
# your_build_command_2 >> $BUILD_OUTPUT 2>&1
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%s/seastar/build/_cooking/installed/lib
./seastar/cooking.sh -- -DSeastar_DPDK=ON -DCMAKE_BUILD_TYPE=Release >> $BUILD_OUTPUT 2>&1
cd build
ninja >> $BUILD_OUTPUT 2>&1

# The build finished without returning an error so dump a tail of the output
dump_output

# nicely terminate the ping output loop
kill $PING_LOOP_PID
"""

    def source(self):
        self.run("git clone --recursive https://github.com/scylladb/seastar.git")
        self.run("cd seastar && git checkout d863ed682c66d10a2b2f3afa8725fd91fa5bceb5")


    def build(self):
        #cmake = CMake(self)
        #cmake.configure(source_folder="hello")
        #cmake.build()

        # Explicit way:
        self.run("echo '" +  self.logworkaround % self.build_folder + "' > seastar/build.sh" )
        self.run("cat seastar/build.sh")
        self.run("chmod u+x seastar/build.sh")
        self.run(" bash seastar/build.sh")

    def package(self):
        self.copy("*.h", dst="include", src="seastar")
        self.copy("*seastar.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

