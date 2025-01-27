import info
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("withICU", self.options.isActive("libs/icu"))
        self.options.dynamic.registerOption("withHarfBuzz", self.options.isActive("libs/harfbuzz"))

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["6.4.0"] = 1
        self.patchToApply["6.5.3"] = [(".6.5.3", 1)]
        self.patchToApply["6.6.0"] = [(".6.5.3", 1)]

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/nodejs"] = None
        self.buildDependencies["python-modules/html5lib"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None
        self.runtimeDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["libs/qt6/qtwebchannel"] = None
        self.runtimeDependencies["libs/nss"] = None
        self.runtimeDependencies["libs/cups"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/lcms2"] = None

        if self.options.dynamic.withICU:
            self.runtimeDependencies["libs/icu"] = None
        if self.options.dynamic.withHarfBuzz:
            self.runtimeDependencies["libs/harfbuzz"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # together with the patch based on https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-qt/qtwebengine/qtwebengine-6.5.2-r1.ebuild
        self.subinfo.options.configure.args += [
            "-DQT_FEATURE_qtwebengine_build=ON",
            f"-DQT_FEATURE_webengine_system_icu={'ON' if self.subinfo.options.dynamic.withICU else 'OFF'}",
            # Package harfbuzz-subset was not found
            # f"-DQT_FEATURE_webengine_system_harfbuzz={'ON' if self.subinfo.options.dynamic.withHarfBuzz else 'OFF'}",
            f"-DQT_FEATURE_webengine_system_libwebp=ON",
            f"-DQT_FEATURE_webengine_system_libjpeg=ON",
            f"-DQT_FEATURE_webengine_system_libxml=ON",
            f"-DQT_FEATURE_webengine_system_freetype=ON",
            f"-DQT_FEATURE_webengine_system_glib=ON",
            f"-DQT_FEATURE_webengine_system_lcms2=ON",
            f"-DQT_FEATURE_webengine_system_pulseaudio=OFF",
        ]
        if not CraftCore.compiler.isLinux and CraftVersion(self.buildTarget) >= CraftVersion("6.5.2"):
            # See https://bugreports.qt.io/browse/QTBUG-115357
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_libpng=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_libpng=ON"]

        if CraftCore.compiler.isMSVC() and CraftVersion(self.buildTarget) >= CraftVersion("6.6.0"):
            self.subinfo.options.configure.args += [f"-DQT_FEATURE_webengine_system_zlib=OFF"]
        else:
            self.subinfo.options.configure.args += [f"-DQT_FEATURE_webengine_system_zlib=ON"]

    def _getEnv(self):
        # webengine requires enormous amounts of ram
        jobs = int(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))
        env = {"NINJAFLAGS": f"-j{int(jobs/2)}"}
        if CraftCore.compiler.isWindows:
            # shorten the path to python
            shortDevUtils = CraftShortPath(Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/").shortPath
            env["PATH"] = f"{shortDevUtils}/bin;{os.environ['PATH']}"
        elif CraftCore.compiler.isLinux:
            # this build system is broken and ignore ldflags
            env["LD_LIBRARY_PATH"] = CraftCore.standardDirs.craftRoot() / "lib"
        return env

    def configure(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().make()
