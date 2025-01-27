import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KRuler app"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.buildDependencies["kde/frameworks/tier1/ki18n"] = None
        self.buildDependencies["kde/frameworks/tier3/knotifications"] = None
        self.buildDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.buildDependencies["kde/frameworks/tier3/kxmlgui"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
