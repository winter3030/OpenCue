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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from PySide2 import QtCore
from PySide2 import QtWidgets

import opencue

import cuegui.AbstractTreeWidget
import cuegui.AbstractWidgetItem
import cuegui.Constants
import cuegui.Logger
import cuegui.MenuActions
import cuegui.UserDialog


logger = cuegui.Logger.getLogger(__file__)

class UsersWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)

        self.__btnRefresh = QtWidgets.QPushButton("Refresh", self)
        self.__btnRefresh.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__btnRefresh.setFixedWidth(150)
        self.__btnRefresh.clicked.connect(self.updateSoon)

        self.__btnAddUser = QtWidgets.QPushButton("Add User", self)
        self.__btnAddUser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.__btnAddUser.setFixedWidth(150)
        self.__btnAddUser.clicked.connect(self.__addUser)

        self.__monitorUsers = UsersTreeWidget(self)

        self.__menuActions = cuegui.MenuActions.MenuActions(self, self.updateSoon, list)

        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__btnAddUser, 0, 3)
        layout.addWidget(self.__btnRefresh, 0, 2)
        core_tip = QtWidgets.QLabel("(In OpenCue 1 core=100)")
        core_tip.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(core_tip, 0, 1)
        layout.addWidget(self.__monitorUsers, 3, 0, 3, 4)

    def updateSoon(self):
        self.__monitorUsers._update()

    def __addUser(self):
        user_dialog = cuegui.UserDialog.UserDialog(rpcObject=None)
        user_dialog.exec_()
        self.updateSoon()

    def getColumnVisibility(self):
        return self.__monitorUsers.getColumnVisibility()

    def setColumnVisibility(self, settings):
        self.__monitorUsers.setColumnVisibility(settings)

class UsersTreeWidget(cuegui.AbstractTreeWidget.AbstractTreeWidget):
    def __init__(self, parent):
        self.startColumnsForType(cuegui.Constants.TYPE_USER)
        self.addColumn("Name", 90, id=1,
                       data=lambda user: user.name())
        self.addColumn("Priority", 80, id=2,
                       data=lambda user: ("%d" % user.job_priority()),
                       sort=lambda user: user.job_priority())
        self.addColumn("Job Max cores", 90, id=3,
                       data=lambda user: ("%d" % user.job_max_cores()),
                       sort=lambda user: user.job_max_cores())
        self.addColumn("Show", 80, id=4,
                       data=lambda user: user.show())
        self.addColumn("Show min cores", 100, id=5,
                       data=lambda user: ("%d" % user.show_min_cores()),
                       sort=lambda user: user.show_min_cores())
        self.addColumn("Show max cores", 100, id=6,
                       data=lambda user: ("%d" % user.show_max_cores()),
                       sort=lambda user: user.show_max_cores())
        self.addColumn("Priority weight", 100, id=7,
                       data=lambda user: ("%d" % user.priority_weight()),
                       sort=lambda user: user.priority_weight())
        self.addColumn("Error weight", 90, id=8,
                       data=lambda user: ("%d" % user.error_weight()),
                       sort=lambda user: user.error_weight())
        self.addColumn("Submit time weight", 100, id=9,
                       data=lambda user: ("%d" % user.submit_time_weight()),
                       sort=lambda user: user.submit_time_weight())
        self.addColumn("Admin", 80, id=10,
                       data=lambda user: ("%s" % user.admin()))
        self.addColumn("Activate", 80, id=11,
                       data=lambda user: ("%s" % user.activate()))

        cuegui.AbstractTreeWidget.AbstractTreeWidget.__init__(self, parent)

        # Used to build right click context menus
        self.__menuActions = cuegui.MenuActions.MenuActions(
            self, self.updateSoon, self.selectedObjects)

        self.itemClicked.connect(self.__itemSingleClickedToDouble)

        self.setUpdateInterval(180)

    def __itemSingleClickedToDouble(self, item, col):
        """Called when an item is clicked on. Causes single clicks to be treated
        as double clicks.
        @type  item: QTreeWidgetItem
        @param item: The item single clicked on
        @type  col: int
        @param col: Column number single clicked on"""
        self.itemDoubleClicked.emit(item, col)

    def _createItem(self, object):
        """Creates and returns the proper item"""
        item = UserWidgetItem(object, self)
        return item

    def _getUpdate(self):
        """Returns the proper data from the cuebot"""
        try:
            return opencue.api.getUserInfos()
        except Exception as e:
            logger.critical(e)
            return []

    def contextMenuEvent(self, e):
        """When right clicking on an item, this raises a context menu"""
        menu = QtWidgets.QMenu()
        self.__menuActions.users().addAction(menu, "editUser")
        menu.addSeparator()
        self.__menuActions.users().addAction(menu, "delete")
        menu.exec_(QtCore.QPoint(e.globalX(), e.globalY()))

    def _processUpdate(self, work, rpcObjects):
        del work
        self._itemsLock.lockForWrite()
        try:
            updated = []
            for rpcObject in rpcObjects:
                objectId = "{}.{}".format(rpcObject.__class__.__name__, rpcObject.name())
                updated.append(objectId)

                # If id already exists, update it
                if objectId in self._items:
                    self._items[objectId].update(rpcObject)
                # If id does not exist, create it
                else:
                    self._items[objectId] = self._createItem(rpcObject)

            # Remove any items that were not updated
            for proxy in list(set(self._items.keys()) - set(updated)):
                self._removeItem(proxy)
            self.redraw()
        finally:
            self._itemsLock.unlock()

class UserWidgetItem(cuegui.AbstractWidgetItem.AbstractWidgetItem):
  def __init__(self, object, parent):
    cuegui.AbstractWidgetItem.AbstractWidgetItem.__init__(
      self, cuegui.Constants.TYPE_USER, object, parent)
