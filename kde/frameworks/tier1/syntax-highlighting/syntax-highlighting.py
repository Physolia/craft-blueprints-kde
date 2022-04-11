import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Syntax highlighting engine for Kate syntax definitions."
        self.displayName = "KSyntaxHighlighting"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
