import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "kronometer"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["productname"] = "Kronometer"
        self.defines["executable"] = "bin\\kronometer.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kronometer.ico")
        self.defines["icon_png"] = os.path.join(self.packageDir(), "150-apps-kronometer.png")
        self.defines["icon_png_44"] = os.path.join(self.packageDir(), "44-apps-kronometer.png")
        self.defines["shortcuts"] = [{"name": "Kronometer", "target": "bin\kronometer.exe"}]
        self.defines["website"] = "https://apps.kde.org/en/kronometer"

        self.addExecutableFilter(r"bin/(?!(kronometer)).*")
        return TypePackager.createPackage(self)
