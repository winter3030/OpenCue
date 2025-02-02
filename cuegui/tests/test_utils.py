#  Copyright Contributors to the OpenCue Project
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Common utility functions for CueGUI test code."""


import PySide2.QtGui

import cuegui.Main


__QAPPLICATION_SINGLETON = None


# pylint: disable=global-statement
def createApplication():
    global __QAPPLICATION_SINGLETON
    if __QAPPLICATION_SINGLETON is None:
        __QAPPLICATION_SINGLETON = cuegui.Main.CueGuiApplication()
        PySide2.QtGui.qApp = __QAPPLICATION_SINGLETON
