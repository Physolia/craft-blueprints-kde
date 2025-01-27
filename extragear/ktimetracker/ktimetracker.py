import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/ktimetracker|master"
        self.defaultTarget = "5.0.1"

        for ver in ["5.0.0", "5.0.1"]:
            self.targets[ver] = "https://download.kde.org/stable/ktimetracker/%s/src/ktimetracker-%s.tar.xz" % (ver, ver)
            self.targetInstSrc[ver] = "ktimetracker-%s" % ver

        self.displayName = "KTimeTracker"
        self.description = "Personal Time Tracker"
        self.webpage = "https://userbase.kde.org/KTimeTracker"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        # KTimeTracker forces Breeze style on Windows
        self.runtimeDependencies["kde/plasma/breeze"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["productname"] = "KTimeTracker"
        self.defines["website"] = "https://userbase.kde.org/KTimeTracker"
        self.defines["executable"] = "bin\\ktimetracker.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "ktimetracker.ico")

        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))

        return TypePackager.createPackage(self)
