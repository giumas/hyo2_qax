import json
import logging
import os
from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QSizePolicy
from hyo2.abc.lib.helper import Helper

from hyo2.qax.app.gui_settings import GuiSettings
from hyo2.qax.app.widgets.qax.check_widget import CheckWidget
from hyo2.qax.lib.plugin import QaxCheckToolPlugin

logger = logging.getLogger(__name__)


class PluginTab(QtWidgets.QMainWindow):

    def __init__(self, parent_win, prj, plugin: QaxCheckToolPlugin):
        QtWidgets.QMainWindow.__init__(self)

        # store a project reference
        self.prj = prj
        self.parent_win = parent_win
        self.media = self.parent_win.media
        self.plugin = plugin

        self.panel = QtWidgets.QFrame()
        self.setCentralWidget(self.panel)
        self.vbox = QtWidgets.QVBoxLayout()
        self.panel.setLayout(self.vbox)

        # title
        label_name = QtWidgets.QLabel(plugin.name)
        label_name.setStyleSheet(GuiSettings.stylesheet_plugin_tab_titles())
        self.vbox.addWidget(label_name)

        self.groupbox_checks = QtWidgets.QGroupBox("Checks")
        self.groupbox_checks.setStyleSheet(
            "QGroupBox::title { color: rgb(155, 155, 155); }")
        self.groupbox_checks.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vbox.addWidget(self.groupbox_checks)

        layout_gb_checks = QtWidgets.QVBoxLayout()
        layout_gb_checks.setContentsMargins(0, 8, 0, 0)
        self.groupbox_checks.setLayout(layout_gb_checks)

        self.scrollarea_checks = QtWidgets.QScrollArea()
        self.scrollarea_checks.setWidgetResizable(True)
        self.scrollarea_checks.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollarea_checks.setStyleSheet("QScrollArea { border: none;}")
        layout_gb_checks.addWidget(self.scrollarea_checks)

        self.widget_checks = QtWidgets.QWidget()
        # self.widget_checks.setStyleSheet("QWidget { background-color: rgb(155, 0, 0); }")
        self.layout_checks = QtWidgets.QVBoxLayout(self.widget_checks)

        for check in self.plugin.checks():
            check_widget = CheckWidget(check)
            self.layout_checks.addWidget(check_widget)

        self.layout_checks.addStretch(1)
        self.scrollarea_checks.setWidget(self.widget_checks)


    def _add_checks(self):
        pass