from cpt.packager import ConanMultiPackager


if __name__ == "__main__":
    command = "sudo apt-get -qq update && sudo apt-get install -y stow"
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="Seastar:shared")
    builder.run()
