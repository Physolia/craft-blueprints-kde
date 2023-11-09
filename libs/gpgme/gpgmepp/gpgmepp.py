import info


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftCore.compiler.isMSVC():
            # Theoretically gpgmepp supports other platforms than Windows with MSVC
            # however not with the patch for MSVC applied below and no one put effort in
            # making it work on other platforms. So if you are interested in it do it :-)
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

        self.patchToApply["1.21.0"] = ("cmake.patch", 1)

        self.patchLevel["1.21.0"] = 6


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DWITH_QT=ON"]

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DQGPGME_BUILD_QT5=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DQGPGME_BUILD_QT6=OFF"]
