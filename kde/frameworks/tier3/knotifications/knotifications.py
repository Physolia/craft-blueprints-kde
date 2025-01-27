import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in ["master", "5.245.0"]:
            # Fix macOS build, see https://invent.kde.org/frameworks/knotifications/-/merge_requests/118
            self.patchToApply[ver] = [("fix-macos-build.patch", 1)]
            self.patchToApply[ver] += [("knotifications-5.245.0-20231111.diff", 1)]

        self.patchLevel["master"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            if CraftCore.compiler.isAndroid:
                self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
            else:
                self.runtimeDependencies["qt-libs/phonon"] = None
            if OsUtils.isMac():
                self.runtimeDependencies["libs/qt5/qtmacextras"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["libs/libcanberra"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt/qtspeech"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None

        if OsUtils.isWin():
            self.runtimeDependencies["dev-utils/snoretoast"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
