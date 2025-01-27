# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libsecret"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5" and CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/frankosterfeld/qtkeychain.git"
        for ver in ["v0.13.1", "0.14.1"]:
            self.targets[ver] = f"https://github.com/frankosterfeld/qtkeychain/archive/{ver}.tar.gz"
            self.archiveNames[ver] = "qtkeychain-{ver}.tar.gz"
            self.targetInstSrc[ver] = "qtkeychain-%s" % ver
        self.targetDigests["v0.13.1"] = (["dc84aea039b81f2613c7845d2ac88bad1cf3a06646ec8af0f7276372bb010c11"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.14.1"] = (["afb2d120722141aca85f8144c4ef017bd74977ed45b80e5d9e9614015dadd60c"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.14.1"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args = ["-DBUILD_WITH_QT6=ON"]
