import os
from pathlib import Path
import logging
from PySide2 import QtGui, QtCore, QtWidgets

from hyo2.abc.app.qt_progress import QtProgress
from hyo2.qax.app.gui_settings import GuiSettings
from hyo2.qax.app.widgets.qax.checks_tab import ChecksTab
from hyo2.qax.app.widgets.qax.main_tab import MainTab
from hyo2.qax.app.widgets.qax.plugin_tab import PluginTab
from hyo2.qax.app.widgets.qax.plugins_tab import PluginsTab
from hyo2.qax.app.widgets.qax.result_tab import ResultTab
from hyo2.qax.app.widgets.qax.run_tab import RunTab, QtCheckExecutor
from hyo2.qax.app.widgets.widget import AbstractWidget
from hyo2.qax.lib.config import QaxConfig, QaxConfigProfile
from hyo2.qax.lib.plugin import QaxPlugins
from hyo2.qax.lib.project import QAXProject
from ausseabed.qajson.model import QajsonRoot

logger = logging.getLogger(__name__)


class QAXWidget(QtWidgets.QTabWidget):
    # overloading
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    def __init__(self, main_win):
        QtWidgets.QTabWidget.__init__(self)
        self.prj = QAXProject()
        self.prj.params.progress = QtProgress(self)

        self.profile = None  # QaxConfigProfile

        # init default settings
        settings = QtCore.QSettings()
        # - output folder
        export_folder = settings.value("qax_export_folder")
        if (export_folder is None) or (not os.path.exists(export_folder)):
            settings.setValue("qax_export_folder", str(self.prj.output_folder))
        else:  # folder exists
            self.prj.output_folder = Path(export_folder)

        # - import
        import_folder = settings.value("ff_import_folder")
        if (import_folder is None) or (not os.path.exists(import_folder)):
            settings.setValue("ff_import_folder", str(self.prj.output_folder))
        import_folder = settings.value("dtm_import_folder")
        if (import_folder is None) or (not os.path.exists(import_folder)):
            settings.setValue("dtm_import_folder", str(self.prj.output_folder))
        # - project folder
        export_project_folder = settings.value("qax_export_project_folder")
        if export_project_folder is None:
            settings.setValue("qax_export_project_folder", str(self.prj.params.project_folder))
        else:  # exists
            self.prj.params.project_folder = (export_project_folder == "true")
        # - subfolders
        export_subfolders = settings.value("qax_export_subfolders")
        if export_subfolders is None:
            settings.setValue("qax_export_subfolders", self.prj.params.subfolders)
        else:  # exists
            self.prj.params.subfolders = (export_subfolders == "true")

        # make tabs
        self.tabs = self #QtWidgets.QTabWidget()

        # self.vbox = QtWidgets.QVBoxLayout()
        # self.setLayout(self.vbox)
        # self.vbox.addWidget(self.tabs)
        # self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setIconSize(QtCore.QSize(36, 36))
        # self.tabs.setTabPosition(QtWidgets.QTabWidget.South)
        # main tab
        self.tab_inputs = MainTab(parent_win=self, prj=self.prj)
        self.tab_inputs.profile_selected.connect(self._on_profile_selected)
        self.tab_inputs.generate_checks.connect(self._on_generate_checks)
        # noinspection PyArgumentList
        self.idx_inputs = self.tabs.insertTab(
            0, self.tab_inputs,
            QtGui.QIcon(GuiSettings.icon_path('qax.png')), "")

        self.tabs.setTabToolTip(self.idx_inputs, "QAX")

        self.tab_plugins = PluginsTab(parent_win=self, prj=self.prj)
        self.idx_plugins = self.tabs.insertTab(
            1, self.tab_plugins,
            QtGui.QIcon(GuiSettings.icon_path('plugins.png')), "")
        self.tabs.setTabToolTip(self.idx_plugins, "Plugins")

        self.tab_run = RunTab(self.prj)
        self.tab_run.objectName = "tab_run"
        self.tab_run.run_checks.connect(self._on_execute_checks)
        self.idx_run = self.tabs.insertTab(
            2, self.tab_run,
            QtGui.QIcon(GuiSettings.icon_path('play.png')), "")
        self.tabs.setTabToolTip(self.idx_run, "Run Checks")

        self.tab_result = ResultTab(self.prj)
        self.tab_result.objectName = "tab_result"
        self.idx_result = self.tabs.insertTab(
            3, self.tab_result,
            QtGui.QIcon(GuiSettings.icon_path('result.png')), "")
        self.tabs.setTabToolTip(self.idx_result, "View check results")

        self.tabs.currentChanged.connect(self.change_tabs)

    def initialize(self):
        self.tab_inputs.initialize()
        # todo: save last selected profile and set here as default.
        self.profile = QaxConfig.instance().profiles[0]
        self.tab_plugins.set_profile(self.profile)

    def _on_profile_selected(self, profile: QaxConfigProfile):
        self.profile = profile
        self.tab_plugins.set_profile(self.profile)

    def _on_generate_checks(self, path: Path):
        """ Read the feature files provided by the user"""
        logger.debug('generate checks ...')
        qa_json = self._build_qa_json()
        self.prj.qa_json = qa_json
        self.prj.save_qa_json()
        #
        # import json
        # print("----- QA JSON -----")
        # print(json.dumps(qajson.to_dict(), sort_keys=True, indent=4))
        # print("-----         -----")

    # QA JSON methods
    def _build_qa_json(self) -> QajsonRoot:
        """
        Builds a QA JSON root object based on the information currently
        entered into the user interface.
        """
        root = QajsonRoot(None)

        # update the qajson object with the check tool details
        for config_check_tool in self.tab_inputs.selected_check_tools:
            plugin_check_tool = QaxPlugins.instance().get_plugin(
                self.profile.name, config_check_tool.plugin_class)
            # update the `root` qa json object with the selected checks
            plugin_check_tool.update_qa_json(root)

            # get a list of user selected files from the relevant controls
            # for this plugin (based on the file groups)
            file_groups = plugin_check_tool.get_file_groups()
            all_files = self.tab_inputs.file_group_selection.get_files(
                file_groups)
            # update the `root` qa json object with files selected by the
            # user
            plugin_check_tool.update_qa_json_input_files(root, all_files)

            # get the plugin tab for the current check tool
            plugin_tab = next(
                (
                    ptab
                    for ptab in self.tab_plugins.plugin_tabs
                    if ptab.plugin == plugin_check_tool
                ),
                None
            )
            if plugin_tab is None:
                raise RuntimeError(
                    "No plugin tab found for {}".format(
                        config_check_tool.name))
            check_param_details = plugin_tab.get_check_ids_and_params()
            for (check_id, params) in check_param_details:
                for p in params:
                    print(p.to_dict())
                plugin_check_tool.update_qa_json_input_params(
                    root, check_id, params)

        return root

    def _on_execute_checks(self):
        """ the run checks """
        logger.debug('executing checks ...')
        qa_json = self._build_qa_json()

        # only the selected ones
        check_tool_plugins = [
            QaxPlugins.instance().get_plugin(
                self.profile.name, config_check_tool.plugin_class)
            for config_check_tool in self.tab_inputs.selected_check_tools
        ]

        executor = QtCheckExecutor(qa_json, check_tool_plugins)
        self.tab_run.run_executor(executor)

    def change_tabs(self, index):
        self.tabs.setCurrentIndex(index)
        self.tabs.currentWidget().setFocus()

    def change_info_url(self, url):
        self.main_win.change_info_url(url)
