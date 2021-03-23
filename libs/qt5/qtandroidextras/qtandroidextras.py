# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Android

    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)