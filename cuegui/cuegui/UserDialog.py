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
from opencue.compiled_proto import opencueUser_pb2

class UserDialog(QtWidgets.QDialog):
    def __init__(self, rpcObject=None, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.rpcObject = rpcObject

        self.title = "Create New User" if self.rpcObject is None else "Edit User"
        self.setWindowTitle(self.title)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setSizeGripEnabled(True)

        if self.rpcObject is None:
            self.__action_btn = QtWidgets.QPushButton("Create", self)
        else:
            self.__action_btn = QtWidgets.QPushButton("Update", self)
        self.__cancel_btn = QtWidgets.QPushButton("Close", self)

        self.__name_label = QtWidgets.QLabel("User name")
        self.__name_field = QtWidgets.QLineEdit()
        self.__name_field.setPlaceholderText("Enter User name here")

        self.__parameters_widget = self.__createUserWidget()

        QtWidgets.QGridLayout(self)
        self.layout().addWidget(self.__name_label, 0, 0, 1, 1)
        self.layout().addWidget(self.__name_field, 0, 1, 1, 2)
        self.layout().addWidget(self.__parameters_widget, 1, 0, 4, 3)
        self.layout().addWidget(self.__action_btn, 8, 1)
        self.layout().addWidget(self.__cancel_btn, 8, 2)

        if self.rpcObject is None:
            self.__action_btn.clicked.connect(self.__createUser)
        else:
            pass
            self.__action_btn.clicked.connect(self.__updateUser)
        self.__cancel_btn.clicked.connect(self.__cancelDialog)
        self.adjustSize()

    def __createUserWidget(self):
        widget = QtWidgets.QGroupBox("Parameters")
        layout = QtWidgets.QGridLayout()

        # checkbox
        self.admin_checkbox = QtWidgets.QCheckBox("Admin")
        layout.addWidget(self.admin_checkbox, 0, 0, 1, 1)
        if self.rpcObject is not None:
            self.activate_checkbox = QtWidgets.QCheckBox("Activate")
            layout.addWidget(self.activate_checkbox, 0, 1, 1, 1)

        # spinbox
        layout.addWidget(QtWidgets.QLabel("Priority"), 1, 0, 1, 1)
        self.priority_spinbox = QtWidgets.QSpinBox(self)
        self.priority_spinbox.setMaximum(100)
        self.priority_spinbox.setMinimum(1)
        self.priority_spinbox.setValue(1)
        self.priority_spinbox.setFixedWidth(200)
        layout.addWidget(self.priority_spinbox, 1, 1, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Max cores"), 1, 2, 1, 1)
        self.max_cores_spinbox = QtWidgets.QSpinBox(self)
        self.max_cores_spinbox.setMaximum(2000)
        self.max_cores_spinbox.setMinimum(1)
        self.max_cores_spinbox.setValue(2)
        self.max_cores_spinbox.setFixedWidth(200)
        layout.addWidget(self.max_cores_spinbox, 1, 3, 1, 1)
        # selector
        layout.addWidget(QtWidgets.QLabel("Show"), 2, 0, 1, 1)
        self.show_selector = QtWidgets.QComboBox(self)
        for show in opencue.api.getShows():
            self.show_selector.addItem(show.name())
        self.show_selector.addItem("showname")
        self.show_selector.addItem("showaaname")
        layout.addWidget(self.show_selector, 2, 1, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Show min cores"), 2, 2, 1, 1)
        self.show_min_cores_spinbox = QtWidgets.QSpinBox(self)
        self.show_min_cores_spinbox.setMaximum(2000)
        self.show_min_cores_spinbox.setMinimum(1)
        self.show_min_cores_spinbox.setValue(2)
        layout.addWidget(self.show_min_cores_spinbox, 2, 3, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Show max cores"), 3, 0, 1, 1)
        self.show_max_cores_spinbox = QtWidgets.QSpinBox(self)
        self.show_max_cores_spinbox.setMaximum(2000)
        self.show_max_cores_spinbox.setMinimum(1)
        self.show_max_cores_spinbox.setValue(2)
        layout.addWidget(self.show_max_cores_spinbox, 3, 1, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Priority weight"), 3, 2, 1, 1)
        self.priority_weight_spinbox = QtWidgets.QSpinBox(self)
        self.priority_weight_spinbox.setMaximum(100)
        self.priority_weight_spinbox.setMinimum(0)
        self.priority_weight_spinbox.setValue(10)
        layout.addWidget(self.priority_weight_spinbox, 3, 3, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Error weight"), 4, 0, 1, 1)
        self.error_weight_spinbox = QtWidgets.QSpinBox(self)
        self.error_weight_spinbox.setMaximum(0)
        self.error_weight_spinbox.setMinimum(-100)
        self.error_weight_spinbox.setValue(-10)
        layout.addWidget(self.error_weight_spinbox, 4, 1, 1, 1)
        # spinbox
        layout.addWidget(QtWidgets.QLabel("Submit time weight"), 4, 2, 1, 1)
        self.submit_time_weight_spinbox = QtWidgets.QSpinBox(self)
        self.submit_time_weight_spinbox.setMaximum(100)
        self.submit_time_weight_spinbox.setMinimum(0)
        self.submit_time_weight_spinbox.setValue(10)
        layout.addWidget(self.submit_time_weight_spinbox, 4, 3, 1, 1)

        if self.rpcObject is not None:
            self.__setupWidgetData()

        widget.setLayout(layout)
        return widget

    def __setupWidgetData(self):
        self.rpcObject = self.rpcObject[0]
        self.__name_field.setText(self.rpcObject.data.name)
        self.__name_field.setEnabled(False)
        if self.rpcObject.data.admin:
            self.admin_checkbox.setChecked(True)
        if self.rpcObject.data.activate:
            self.activate_checkbox.setChecked(True)
        self.priority_spinbox.setValue(self.rpcObject.data.job_priority)
        self.max_cores_spinbox.setValue(self.rpcObject.data.job_max_cores / 100)
        item_index = self.show_selector.findText(self.rpcObject.data.show)
        self.show_selector.setCurrentIndex(item_index)
        self.show_min_cores_spinbox.setValue(self.rpcObject.data.show_min_cores / 100)
        self.show_max_cores_spinbox.setValue(self.rpcObject.data.show_max_cores / 100)
        self.priority_weight_spinbox.setValue(self.rpcObject.data.priority_weight)
        self.error_weight_spinbox.setValue(self.rpcObject.data.error_weight)
        self.submit_time_weight_spinbox.setValue(self.rpcObject.data.submit_time_weight)

    def __createUser(self):
        user_name = self.__name_field.text()
        if not user_name:
            QtWidgets.QMessageBox.critical(
                self,
                "Invalid User Name",
                "Please enter a valid user name.",
                QtWidgets.QMessageBox.Ok
            )
            return

        if self.show_min_cores_spinbox.value() >= self.show_max_cores_spinbox.value():
            QtWidgets.QMessageBox.critical(
                self,
                "Invalid Cores",
                "Show Maximum smaller than show minimum. Please enter valid Cores.",
                QtWidgets.QMessageBox.Ok
            )
            return

        for user in opencue.api.getUserInfos():
            if str(user.name()) == user_name:
                QtWidgets.QMessageBox.critical(
                    self,
                    "User Already Exists",
                    "User with that name already exists, please enter a unique user name.",
                    QtWidgets.QMessageBox.Ok
                )
                return
        '''try:
            opencue.api.getUserInfo(user_name)
            QtWidgets.QMessageBox.critical(
                self,
                "User Already Exists",
                "User with that name already exists, please enter a unique user name.",
                QtWidgets.QMessageBox.Ok
            )
            return
        except opencue.exception.CueInternalErrorException:
            pass'''

        try:
            job_priority = self.priority_spinbox.value()
            job_max_cores = self.max_cores_spinbox.value() * 100
            show = self.show_selector.currentText()
            show_min_cores = self.show_min_cores_spinbox.value() * 100
            show_max_cores = self.show_max_cores_spinbox.value() * 100
            priority_weight = self.priority_weight_spinbox.value()
            error_weight = self.error_weight_spinbox.value()
            submit_time_weight = self.submit_time_weight_spinbox.value()
            admin = True if self.admin_checkbox.isChecked() else False
            new_user = opencueUser_pb2.User(
                name=user_name, admin=admin, job_priority=job_priority, job_max_cores=job_max_cores, show=show,
                show_min_cores=show_min_cores, show_max_cores=show_max_cores, activate=True,
                priority_weight=priority_weight, error_weight=error_weight, submit_time_weight=submit_time_weight)
            opencue.api.createUser(new_user)
        except opencue.exception.CueException as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Failed To Create User",
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.accept()

    def __updateUser(self):
        if self.show_min_cores_spinbox.value() >= self.show_max_cores_spinbox.value():
            QtWidgets.QMessageBox.critical(
                self,
                "Invalid Cores",
                "Show Maximum smaller than show minimum. Please enter valid Cores.",
                QtWidgets.QMessageBox.Ok
            )
            return

        try:
            user_name = self.__name_field.text()
            job_priority = self.priority_spinbox.value()
            job_max_cores = self.max_cores_spinbox.value() * 100
            show = self.show_selector.currentText()
            show_min_cores = self.show_min_cores_spinbox.value() * 100
            show_max_cores = self.show_max_cores_spinbox.value() * 100
            priority_weight = self.priority_weight_spinbox.value()
            error_weight = self.error_weight_spinbox.value()
            submit_time_weight = self.submit_time_weight_spinbox.value()
            admin = True if self.admin_checkbox.isChecked() else False
            activate = True if self.activate_checkbox.isChecked() else False
            update_user = opencueUser_pb2.User(
                name=user_name, admin=admin, job_priority=job_priority, job_max_cores=job_max_cores, show=show,
                show_min_cores=show_min_cores, show_max_cores=show_max_cores, activate=activate,
                priority_weight=priority_weight, error_weight=error_weight, submit_time_weight=submit_time_weight)
            opencue.api.updateUserInfo(update_user)
        except opencue.exception.CueException as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Failed To Update User",
                str(e),
                QtWidgets.QMessageBox.Ok
            )
            return

        self.accept()

    def __cancelDialog(self):
        """Abort creating a new show"""
        self.reject()
