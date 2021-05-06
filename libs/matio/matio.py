import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/tbeu/matio.git"
        for ver in ["1.5.21"]:
            self.targets[ver] = f"https://github.com/tbeu/matio/releases/download/v{ver}/matio-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"matio-{ver}"
        self.targetDigests['1.5.21'] = (
            ['21809177e55839e7c94dada744ee55c1dea7d757ddaab89605776d50122fb065'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'A library for reading and writing binary MATLAB MAT files'
        self.defaultTarget = '1.5.21'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/hdf5"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        hdf5dir = os.path.join(CraftStandardDirs.craftRoot(), "cmake", "hdf5")
        self.subinfo.options.configure.args = f"-DHDF5_DIR={hdf5dir} -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF"

    def createPackage(self):
        return TypePackager.createPackage(self)