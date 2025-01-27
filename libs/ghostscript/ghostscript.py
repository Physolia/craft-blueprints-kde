import info
from CraftCompiler import CraftCompiler


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        if not CraftCore.compiler.isMSVC():
            self.buildDependencies["dev-utils/msys"] = None
            self.runtimeDependencies["libs/lcms2"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/openjpeg"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/tiff"] = None
            self.runtimeDependencies["libs/fontconfig"] = None

    def setTargets(self):
        self.svnTargets["master"] = "git://git.ghostscript.com/ghostpdl.git"
        for ver in ["10.01.2"]:
            ver2 = ver.replace(".", "")
            self.targets[ver] = f"https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{ver2}/ghostscript-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"ghostscript-{ver}"
            self.targetDigestUrls[ver] = (
                [f"https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{ver2}/SHA512SUMS"],
                CraftHash.HashAlgorithm.SHA512,
            )

        self.defaultTarget = "10.01.2"


from Package.CMakePackageBase import *


class PackageMSVC(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def configure(self):
        return True

    def make(self):
        self.enterSourceDir()

        extraArgs = []
        if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64:
            extraArgs.append("WIN64=")
        # because ghostscript doesn't know about msvc2015, it guesses wrong on this. But,
        # because of where we are, rc /should/ be in the path, so we'll just use that.
        if CraftCore.compiler.isMSVC():
            extraArgs.append("RCOMP=rc.exe")
        if CraftCore.compiler.isMSVC2017():
            # work-around: https://bugs.ghostscript.com/show_bug.cgi?id=698426
            vcInstallDir = os.environ["VCINSTALLDIR"].rstrip("\\")
            extraArgs += ["MSVC_VERSION=15", f'DEVSTUDIO="{vcInstallDir}"']
        utils.system(["nmake", "-f", "psi\\msvc.mak"] + extraArgs)
        return True

    def install(self):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir(dst):
            os.mkdir(dst)
        if not os.path.isdir(os.path.join(dst, "bin")):
            os.mkdir(os.path.join(dst, "bin"))
        if not os.path.isdir(os.path.join(dst, "lib")):
            os.mkdir(os.path.join(dst, "lib"))
        if not os.path.isdir(os.path.join(dst, "include")):
            os.mkdir(os.path.join(dst, "include"))
        if not os.path.isdir(os.path.join(dst, "include", "ghostscript")):
            os.mkdir(os.path.join(dst, "include", "ghostscript"))

        _bit = CraftCore.compiler.bits
        utils.copyFile(os.path.join(src, "bin", "gsdll%s.dll" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(src, "bin", "gsdll%s.lib" % _bit), os.path.join(dst, "lib"), False)
        utils.copyFile(os.path.join(src, "bin", "gswin%s.exe" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(src, "bin", "gswin%sc.exe" % _bit), os.path.join(dst, "bin"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "iapi.h"), os.path.join(self.imageDir(), "include", "ghostscript", "iapi.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "psi", "ierrors.h"), os.path.join(self.imageDir(), "include", "ghostscript", "ierrors.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "devices", "gdevdsp.h"), os.path.join(self.imageDir(), "include", "ghostscript", "gdevdsp.h"), False)
        utils.copyFile(os.path.join(self.sourceDir(), "base", "gserrors.h"), os.path.join(self.imageDir(), "include", "ghostscript", "gserrors.h"), False)
        utils.copyDir(os.path.join(self.sourceDir(), "lib"), os.path.join(self.imageDir(), "lib"), False)

        return True


from Package.AutoToolsPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        # self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.args += [
            "--with-drivers=ALL",
            "--disable-cups",
            "--without-x",
            "--disable-contrib",
            "--enable-freetype",
            "--with-jbig2dec",
            "--enable-openjpeg",
            "--disable-gtk",
            "--enable-fontconfig",
        ]
        if not CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["--with-system-libtiff"]
        else:
            self.subinfo.options.configure.args += ["--with-libtiff"]
        self.subinfo.options.make.args += ["so", "all"]
        self.subinfo.options.install.args += ["install-so", "install"]
        self.subinfo.options.useShadowBuild = False

    def unpack(self):
        if not AutoToolsPackageBase.unpack(self):
            return False
        forceSystemLibs = ["freetype", "jpeg", "libpng", "lcms", "lcms2", "zlib"]
        if not CraftCore.compiler.isMacOS:
            forceSystemLibs += ["tiff", "openjpeg"]
        for d in forceSystemLibs:
            utils.rmtree(os.path.join(self.sourceDir(), d))
        return True

    def make(self):
        env = {}
        if CraftCore.compiler.isLinux:
            env["LD_LIBRARY_PATH"] = CraftCore.standardDirs.craftRoot() / "lib"
        with utils.ScopedEnv(env):
            return super().make()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isLinux:
            # only the sym links get installed...
            return utils.copyFile(f"{self.buildDir()}/sobin/libgs.so.10", f"{self.installDir()}/lib/libgs.so.10")

        return True


if CraftCore.compiler.isGCCLike():

    class Package(PackageMSys):
        pass

else:

    class Package(PackageMSVC):
        pass
