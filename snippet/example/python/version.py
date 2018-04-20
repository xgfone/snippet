import pbr.version


def get_version(program_name):
    return pbr.version.VersionInfo(program_name).version_string()
