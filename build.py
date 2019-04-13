from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    command = "sudo apt-get -qq update && sudo apt-get install -y stow xfslibs-dev systemtap-sdt-dev"
    builder = ConanMultiPackager(docker_entry_script=command)
    builder.add_common_builds(shared_option_name="Seastar:shared")
    builder.run()
