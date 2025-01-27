import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1-alpha-20230712-1"]:
            self.targets[
                ver
            ] = f"https://github.com/linuxdeploy/linuxdeploy-plugin-appimage/releases/download/{ver}/linuxdeploy-plugin-appimage-x86_64.AppImage"
            # add version to file name to allow downloading multiple versions
            self.archiveNames[ver] = f"linuxdeploy-plugin-appimage-{ver}-x86_64.AppImage"
            self.targetInstallPath[ver] = "dev-utils/bin"
        self.targetDigests["1-alpha-20230712-1"] = (["87959cd3daa288d1b76ceb3858934b4db8e5a157397e663b8cf65969134ae1af"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1-alpha-20230712-1"
        self.description = "Plugin for linuxdeploy. Creates AppImages from AppDirs."
        self.webpage = "https://github.com/linuxdeploy/linuxdeploy-plugin-appimage"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        # remove version from file name
        return utils.moveFile(
            self.installDir() / self.subinfo.archiveNames[self.buildTarget], self.installDir() / "linuxdeploy-plugin-appimage-x86_64.AppImage"
        )
