from ausseabed.qajson.model import QajsonParam
from PySide2 import QtCore, QtGui, QtWidgets
from typing import Optional, NoReturn, List

from hyo2.qax.app.gui_settings import GuiSettings
from hyo2.qax.lib.plugin import QaxCheckReference


def get_param_widget(param: QajsonParam, parent=None) -> 'CheckParamWidget':
    """ Returns a `CheckParamWidget` of the correct type for the given
    param. Factory method.
    """
    # todo: implementation here will need to change to support more advanced
    # parameter types
    if isinstance(param.value, str):
        return CheckParamStringWidget(param, parent)
    elif isinstance(param.value, bool):
        return CheckParamBoolWidget(param, parent)
    elif isinstance(param.value, int):
        return CheckParamIntWidget(param, parent)
    elif isinstance(param.value, float):
        return CheckParamFloatWidget(param, parent)
    else:
        # special case. Return a widget that doesn't allow modification.
        # it simply shows that this is an unsupported type.
        return CheckParamUnknownWidget(param, parent)


class CheckParamWidget(QtWidgets.QWidget):
    """ base class for all CheckParamWidgets. These show the parameter details
    to the user, allow modification, and perform validation of user entered
    data.
    """

    # emitted when a new file is selected
    value_changed = QtCore.Signal(QajsonParam)

    def __init__(self, param: QajsonParam, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self._param = param
        self.label_min_width = 200

    def param(self) -> QajsonParam:
        raise NotImplementedError(
            "Must implement in param function of child class to return "
            "correct value type within an QajsonParam")

    def _on_edited(self) -> NoReturn:
        self._raise_value_changed(self.param())

    def _raise_value_changed(self, param: QajsonParam) -> NoReturn:
        self.value_changed.emit(param)

    @property
    def value(self):
        return self.param().value

    @value.setter
    def value(self, value):
        raise NotImplementedError("Must implement in child class")


class CheckParamStringWidget(CheckParamWidget):
    """ Supports parameters with string value types
    """

    def __init__(self, param: QajsonParam, parent=None):
        super().__init__(param, parent=parent)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        label_name = QtWidgets.QLabel("{}".format(self._param.name))
        label_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_name.setMinimumWidth(self.label_min_width)
        label_name.setStyleSheet(GuiSettings.stylesheet_check_param_name())
        hbox.addWidget(label_name)

        self.lineedit_value = QtWidgets.QLineEdit()
        self.lineedit_value.setText(self._param.value)
        self.lineedit_value.textEdited.connect(self._on_edited)
        hbox.addWidget(self.lineedit_value)

    def param(self) -> QajsonParam:
        return QajsonParam(
            name=self._param.name,
            value=self.lineedit_value.text()
        )

    @CheckParamWidget.value.setter
    def value(self, value):
        self.lineedit_value.setText(str(value))


class CheckParamIntWidget(CheckParamWidget):
    """ Supports parameters with int value types
    """

    def __init__(self, param: QajsonParam, parent=None):
        super().__init__(param, parent=parent)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        label_name = QtWidgets.QLabel("{}".format(self._param.name))
        label_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_name.setMinimumWidth(self.label_min_width)
        label_name.setStyleSheet(GuiSettings.stylesheet_check_param_name())
        hbox.addWidget(label_name)

        self.lineedit_value = QtWidgets.QLineEdit()
        self.lineedit_value.setText(str(self._param.value))
        self.lineedit_value.textEdited.connect(self._on_edited)
        hbox.addWidget(self.lineedit_value)

    def param(self) -> QajsonParam:
        return QajsonParam(
            name=self._param.name,
            value=int(self.lineedit_value.text())
        )

    @CheckParamWidget.value.setter
    def value(self, value):
        self.lineedit_value.setText(str(value))


class CheckParamBoolWidget(CheckParamWidget):
    """ Supports parameters with bool value types
    """

    def __init__(self, param: QajsonParam, parent=None):
        super().__init__(param, parent=parent)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(hbox)

        label_name = QtWidgets.QLabel(f"{self._param.name}")
        label_name.setMinimumWidth(self.label_min_width)
        label_name.setStyleSheet(GuiSettings.stylesheet_check_param_name())
        hbox.addWidget(label_name)

        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(self._param.value)
        self.checkbox.stateChanged.connect(self._on_edited)
        hbox.addWidget(self.checkbox)

    def param(self) -> QajsonParam:
        return QajsonParam(
            name=self._param.name,
            value=self.checkbox.isChecked()
        )

    @CheckParamWidget.value.setter
    def value(self, value):
        self.checkbox.setChecked(value)


class CheckParamFloatWidget(CheckParamWidget):
    """ Supports parameters with int value types
    """

    def __init__(self, param: QajsonParam, parent=None):
        super().__init__(param, parent=parent)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        label_name = QtWidgets.QLabel("{}".format(self._param.name))
        label_name.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_name.setMinimumWidth(self.label_min_width)
        label_name.setStyleSheet(GuiSettings.stylesheet_check_param_name())
        hbox.addWidget(label_name)

        self.lineedit_value = QtWidgets.QLineEdit()
        self.lineedit_value.setText(str(self._param.value))
        self.lineedit_value.textEdited.connect(self._on_edited)
        hbox.addWidget(self.lineedit_value)

    def param(self) -> QajsonParam:
        return QajsonParam(
            name=self._param.name,
            value=float(self.lineedit_value.text())
        )

    @CheckParamWidget.value.setter
    def value(self, value):
        self.lineedit_value.setText(str(value))


class CheckParamUnknownWidget(CheckParamWidget):
    """ Supports parameters with string value types
    """

    def __init__(self, param: QajsonParam, parent=None):
        super().__init__(param, parent=parent)

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        label_name = QtWidgets.QLabel(
            "Unknown param type: {}".format(self._param.name))
        label_name.setMinimumWidth(self.label_min_width)
        label_name.setStyleSheet(GuiSettings.stylesheet_check_param_name())
        hbox.addWidget(label_name)

    def param(self) -> QajsonParam:
        return QajsonParam(
            name=self._param.name,
            value=None
        )

    @CheckParamWidget.value.setter
    def value(self, value):
        pass
