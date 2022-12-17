import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotWindows & CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.101.0"] = [("fix-if-vs-ifdef.diff", 1)]
        self.patchLevel["5.101.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtwayland"] = None
        self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None
        self.runtimeDependencies["libs/wayland-protocols"] = None
        self.runtimeDependencies["libs/wayland"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
