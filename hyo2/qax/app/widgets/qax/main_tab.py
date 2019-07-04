import os
import logging
from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets
from hyo2.abc.lib.helper import Helper
from hyo2.qax.app.gui_settings import GuiSettings
# Use NSURL as a workaround to pyside/Qt4 behaviour for dragging and dropping on OSx
if Helper.is_darwin():
    # noinspection PyUnresolvedReferences
    from Foundation import NSURL

logger = logging.getLogger(__name__)


class MainTab(QtWidgets.QMainWindow):

    here = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, parent_win, prj):
        QtWidgets.QMainWindow.__init__(self)

        # store a project reference
        self.prj = prj
        self.parent_win = parent_win
        self.media = self.parent_win.media

        # ui
        self.panel = QtWidgets.QFrame()
        self.setCentralWidget(self.panel)
        self.vbox = QtWidgets.QVBoxLayout()
        self.panel.setLayout(self.vbox)

        left_space = 100
        vertical_space = 1
        label_size = 160

        self.settings = QtWidgets.QGroupBox("Profile Settings")
        self.settings.setStyleSheet("QGroupBox::title { color: rgb(155, 155, 155); }")
        self.vbox.addWidget(self.settings)

        vbox = QtWidgets.QVBoxLayout()
        self.settings.setLayout(vbox)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        self.text_profiles = QtWidgets.QLabel("Profile:")
        hbox.addWidget(self.text_profiles)
        profiles_list = ["NOAA", "AusSeabed", "Custom"]
        self.set_profiles = QtWidgets.QComboBox()
        self.set_profiles.addItems(profiles_list)
        self.set_profiles.setCurrentText(profiles_list[0])
        # noinspection PyUnresolvedReferences
        self.set_profiles.currentTextChanged.connect(self.on_set_profiles)
        hbox.addWidget(self.set_profiles)
        hbox.addStretch()

        vbox.addSpacing(vertical_space)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        self.set_flier_finder = QtWidgets.QCheckBox("Flier Finder")
        self.set_flier_finder.setFixedWidth(label_size)
        hbox.addWidget(self.set_flier_finder)
        hbox.addSpacing(left_space)
        self.set_holiday_finder = QtWidgets.QCheckBox("Holiday Finder")
        self.set_holiday_finder.setFixedWidth(label_size)
        hbox.addWidget(self.set_holiday_finder)
        hbox.addSpacing(left_space)
        self.set_grid_qa = QtWidgets.QCheckBox("Grid QA")
        self.set_grid_qa.setFixedWidth(label_size)
        hbox.addWidget(self.set_grid_qa)
        hbox.addStretch()

        vbox.addSpacing(vertical_space)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        self.set_designated_scan = QtWidgets.QCheckBox("Designated Scan")
        self.set_designated_scan.setFixedWidth(label_size)
        hbox.addWidget(self.set_designated_scan)
        hbox.addSpacing(left_space)
        self.set_feature_scan = QtWidgets.QCheckBox("Feature Scan")
        self.set_feature_scan.setFixedWidth(label_size)
        hbox.addWidget(self.set_feature_scan)
        hbox.addSpacing(left_space)
        self.set_valsou_check = QtWidgets.QCheckBox("VALSOU Check")
        self.set_valsou_check.setFixedWidth(label_size)
        hbox.addWidget(self.set_valsou_check)
        hbox.addStretch()

        vbox.addSpacing(vertical_space)

        self.survey = QtWidgets.QGroupBox("Survey Products")
        self.survey.setStyleSheet("QGroupBox::title { color: rgb(155, 155, 155); }")
        self.vbox.addWidget(self.survey)

        vbox = QtWidgets.QVBoxLayout()
        self.survey.setLayout(vbox)

        # add dtm
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        text_add_dtm = QtWidgets.QLabel("Survey DTMs:")
        hbox.addWidget(text_add_dtm)
        text_add_dtm.setMinimumWidth(90)
        self.input_dtm = QtWidgets.QListWidget()
        hbox.addWidget(self.input_dtm)
        self.input_dtm.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.input_dtm.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.input_dtm.customContextMenuRequested.connect(self.make_dtm_context_menu)
        self.input_dtm.setAlternatingRowColors(True)
        self.input_dtm.setMaximumHeight(100)
        # Enable dropping onto the input ss list
        self.input_dtm.setAcceptDrops(True)
        self.input_dtm.installEventFilter(self)
        button_add_dtm = QtWidgets.QPushButton()
        hbox.addWidget(button_add_dtm)
        button_add_dtm.setFixedHeight(GuiSettings.single_line_height())
        button_add_dtm.setFixedWidth(GuiSettings.single_line_height())
        button_add_dtm.setText(" + ")
        button_add_dtm.setToolTip('Add (or drag-and-drop) the survey DTMs as CSAR or BAG files')
        # noinspection PyUnresolvedReferences
        button_add_dtm.clicked.connect(self.click_add_dtm)

        vbox.addSpacing(10)

        # add ENC
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        text_add_ff = QtWidgets.QLabel("Feature Files:")
        hbox.addWidget(text_add_ff)
        text_add_ff.setFixedHeight(GuiSettings.single_line_height())
        text_add_ff.setMinimumWidth(90)
        self.input_ff = QtWidgets.QListWidget()
        hbox.addWidget(self.input_ff)
        self.input_ff.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.input_ff.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.input_ff.customContextMenuRequested.connect(self.make_ff_context_menu)
        self.input_ff.setAlternatingRowColors(True)
        self.input_ff.setMaximumHeight(100)
        # Enable dropping onto the input s57 list
        self.input_ff.setAcceptDrops(True)
        self.input_ff.installEventFilter(self)
        button_add_ff = QtWidgets.QPushButton()
        hbox.addWidget(button_add_ff)
        button_add_ff.setFixedHeight(GuiSettings.single_line_height())
        button_add_ff.setFixedWidth(GuiSettings.single_line_height())
        button_add_ff.setText(" + ")
        button_add_ff.setToolTip('Add (or drag-and-drop) the feature files as S57 file (.000)')
        # noinspection PyUnresolvedReferences
        button_add_ff.clicked.connect(self.click_add_ff)

        vbox.addStretch()

        # clear data
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        button_clear_data = QtWidgets.QPushButton()
        hbox.addWidget(button_clear_data)
        button_clear_data.setFixedHeight(GuiSettings.single_line_height())
        # button_clear_data.setFixedWidth(GuiSettings.single_line_height())
        button_clear_data.setText("Clear data")
        button_clear_data.setToolTip('Clear all data loaded')
        # noinspection PyUnresolvedReferences
        button_clear_data.clicked.connect(self.click_clear_data)
        # info
        button = QtWidgets.QPushButton()
        hbox.addWidget(button)
        button.setFixedHeight(GuiSettings.single_line_height())
        button.setFixedWidth(GuiSettings.single_line_height())
        icon_info = QtCore.QFileInfo(os.path.join(self.media, 'small_info.png'))
        button.setIcon(QtGui.QIcon(icon_info.absoluteFilePath()))
        button.setToolTip('Open the manual page')
        button.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0); }\n"
                             "QPushButton:hover { background-color: rgba(230, 230, 230, 100); }\n")
        # noinspection PyUnresolvedReferences
        button.clicked.connect(self.click_open_manual)
        hbox.addStretch()

        # data outputs
        self.savedData = QtWidgets.QGroupBox("Data outputs [drap-and-drop the desired output folder]")
        self.savedData.setStyleSheet("QGroupBox::title { color: rgb(155, 155, 155); }")
        self.savedData.setMaximumHeight(GuiSettings.single_line_height() * 8)
        self.vbox.addWidget(self.savedData)

        vbox = QtWidgets.QVBoxLayout()
        self.savedData.setLayout(vbox)

        # set optional formats
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        text_set_formats = QtWidgets.QLabel("Formats:")
        hbox.addWidget(text_set_formats)
        text_set_formats.setFixedHeight(GuiSettings.single_line_height())
        text_set_formats.setMinimumWidth(64)
        self.output_pdf = QtWidgets.QCheckBox("PDF")
        self.output_pdf.setChecked(True)
        self.output_pdf.setDisabled(True)
        hbox.addWidget(self.output_pdf)
        self.output_s57 = QtWidgets.QCheckBox("S57")
        self.output_s57.setChecked(True)
        self.output_s57.setDisabled(True)
        hbox.addWidget(self.output_s57)
        self.output_shp = QtWidgets.QCheckBox("Shapefile")
        self.output_shp.setToolTip('Activate/deactivate the creation of Shapefiles in output')
        self.output_shp.setChecked(self.prj.params.write_shp)
        # noinspection PyUnresolvedReferences
        self.output_shp.clicked.connect(self.click_output_shp)
        hbox.addWidget(self.output_shp)
        self.output_kml = QtWidgets.QCheckBox("KML")
        self.output_kml.setToolTip('Activate/deactivate the creation of KML files in output')
        self.output_kml.setChecked(self.prj.params.write_kml)
        # noinspection PyUnresolvedReferences
        self.output_kml.clicked.connect(self.click_output_kml)
        hbox.addWidget(self.output_kml)

        hbox.addSpacing(36)

        text_set_prj_folder = QtWidgets.QLabel("Create project folder: ")
        hbox.addWidget(text_set_prj_folder)
        text_set_prj_folder.setFixedHeight(GuiSettings.single_line_height())
        self.output_prj_folder = QtWidgets.QCheckBox("")
        self.output_prj_folder.setToolTip('Create a sub-folder with project name')
        self.output_prj_folder.setChecked(self.prj.params.project_folder)
        # noinspection PyUnresolvedReferences
        self.output_prj_folder.clicked.connect(self.click_output_project_folder)
        hbox.addWidget(self.output_prj_folder)

        text_set_subfolders = QtWidgets.QLabel("Per-tool sub-folders: ")
        hbox.addWidget(text_set_subfolders)
        text_set_subfolders.setFixedHeight(GuiSettings.single_line_height())
        self.output_subfolders = QtWidgets.QCheckBox("")
        self.output_subfolders.setToolTip('Create a sub-folder for each tool')
        self.output_subfolders.setChecked(self.prj.params.subfolders)
        # noinspection PyUnresolvedReferences
        self.output_subfolders.clicked.connect(self.click_output_subfolders)
        hbox.addWidget(self.output_subfolders)

        hbox.addStretch()

        # add folder
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        text_add_folder = QtWidgets.QLabel("Folder:")
        hbox.addWidget(text_add_folder)
        text_add_folder.setMinimumWidth(64)
        self.output_folder = QtWidgets.QListWidget()
        hbox.addWidget(self.output_folder)
        self.output_folder.setMinimumHeight(GuiSettings.single_line_height())
        self.output_folder.setMaximumHeight(GuiSettings.single_line_height() * 2)
        self.output_folder.clear()
        new_item = QtWidgets.QListWidgetItem()
        new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 'folder.png')))
        new_item.setText("%s" % self.prj.outputs.output_folder)
        new_item.setFont(GuiSettings.console_font())
        new_item.setForeground(GuiSettings.console_fg_color())
        self.output_folder.addItem(new_item)
        # Enable dropping onto the input ss list
        self.output_folder.setAcceptDrops(True)
        self.output_folder.installEventFilter(self)
        button_add_folder = QtWidgets.QPushButton()
        hbox.addWidget(button_add_folder)
        button_add_folder.setFixedHeight(GuiSettings.single_line_height())
        button_add_folder.setFixedWidth(GuiSettings.single_line_height())
        button_add_folder.setText(" .. ")
        button_add_folder.setToolTip('Add (or drag-and-drop) output folder')
        # noinspection PyUnresolvedReferences
        button_add_folder.clicked.connect(self.click_add_folder)

        # open folder
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()

        button_default_output = QtWidgets.QPushButton()
        hbox.addWidget(button_default_output)
        button_default_output.setFixedHeight(GuiSettings.single_line_height())
        # button_open_output.setFixedWidth(GuiSettings.single_line_height())
        button_default_output.setText("Use default")
        button_default_output.setToolTip('Use the default output folder')
        # noinspection PyUnresolvedReferences
        button_default_output.clicked.connect(self.click_default_output)

        button_open_output = QtWidgets.QPushButton()
        hbox.addWidget(button_open_output)
        button_open_output.setFixedHeight(GuiSettings.single_line_height())
        # button_open_output.setFixedWidth(GuiSettings.single_line_height())
        button_open_output.setText("Open folder")
        button_open_output.setToolTip('Open the output folder')
        # noinspection PyUnresolvedReferences
        button_open_output.clicked.connect(self.click_open_output)

        hbox.addStretch()

        self.vbox.addStretch()

        # data outputs
        self.checksSuite = QtWidgets.QGroupBox("Checks suite")
        self.checksSuite.setStyleSheet("QGroupBox::title { color: rgb(155, 155, 155); }")
        self.checksSuite.setMaximumHeight(GuiSettings.single_line_height() * 8)
        self.vbox.addWidget(self.checksSuite)

        vbox = QtWidgets.QVBoxLayout()
        self.checksSuite.setLayout(vbox)

        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        button_generate_checks = QtWidgets.QPushButton()
        hbox.addWidget(button_generate_checks)
        button_generate_checks.setFixedHeight(GuiSettings.single_line_height())
        # button_generate_checks.setFixedWidth(GuiSettings.single_line_height())
        button_generate_checks.setText("Generate")
        button_generate_checks.setToolTip('Generate the QA JSON checks based on the selected profile')
        # noinspection PyUnresolvedReferences
        button_generate_checks.clicked.connect(self.click_generate_checks)
        hbox.addStretch()

        # add folder
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)
        text_add_folder = QtWidgets.QLabel("QA JSON:")
        hbox.addWidget(text_add_folder)
        text_add_folder.setMinimumWidth(64)
        self.qa_json = QtWidgets.QListWidget()
        hbox.addWidget(self.qa_json)
        self.qa_json.setMinimumHeight(GuiSettings.single_line_height())
        self.qa_json.setMaximumHeight(GuiSettings.single_line_height() * 2)
        self.qa_json.clear()
        # Enable dropping onto the input ss list
        self.qa_json.setAcceptDrops(True)
        self.qa_json.installEventFilter(self)
        button_add_json = QtWidgets.QPushButton()
        hbox.addWidget(button_add_json)
        button_add_json.setFixedHeight(GuiSettings.single_line_height())
        button_add_json.setFixedWidth(GuiSettings.single_line_height())
        button_add_json.setText(" .. ")
        button_add_json.setToolTip('Add (or drag-and-drop) QA JSON')
        # noinspection PyUnresolvedReferences
        button_add_json.clicked.connect(self.click_add_json)

        self.installEventFilter(self)

        self.on_set_profiles()

    def eventFilter(self, obj, e):

        # drag events
        if (e.type() == QtCore.QEvent.DragEnter) or (e.type() == QtCore.QEvent.DragMove):

            if obj in (self.input_dtm, ):

                if e.mimeData().hasUrls:

                    for url in e.mimeData().urls():

                        if Helper.is_darwin():
                            dropping_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())

                        else:
                            dropping_file = str(url.toLocalFile())

                        if os.path.splitext(dropping_file)[-1].lower() in (".bag", ".csar"):
                            e.accept()
                            return True

            elif obj in (self.input_ff,):

                if e.mimeData().hasUrls:

                    for url in e.mimeData().urls():

                        if Helper.is_darwin():
                            dropping_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())

                        else:
                            dropping_file = str(url.toLocalFile())

                        if os.path.splitext(dropping_file)[-1].lower() in (".000", ):
                            e.accept()
                            return True

            elif obj in (self.output_folder,):

                if e.mimeData().hasUrls:

                    for url in e.mimeData().urls():

                        if Helper.is_darwin():
                            dropped_path = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())

                        else:
                            dropped_path = str(url.toLocalFile())

                        dropped_path = os.path.abspath(dropped_path)

                        if os.path.isdir(dropped_path):
                            e.accept()
                            return True

            elif obj in (self.qa_json,):

                if e.mimeData().hasUrls:

                    for url in e.mimeData().urls():

                        if Helper.is_darwin():
                            dropping_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())

                        else:
                            dropping_file = str(url.toLocalFile())

                        if os.path.splitext(dropping_file)[-1].lower() in (".json", ):
                            e.accept()
                            return True

            e.ignore()
            return True

        # drop events
        if e.type() == QtCore.QEvent.Drop:

            # print('drop', obj)
            if obj is self.input_dtm:

                if e.mimeData().hasUrls():

                    e.setDropAction(QtCore.Qt.CopyAction)
                    e.accept()
                    # Workaround for OSx dragging and dropping
                    for url in e.mimeData().urls():
                        if Helper.is_darwin():
                            dropped_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                        else:
                            dropped_file = str(url.toLocalFile())

                        logger.debug("dropped file: %s" % dropped_file)
                        if os.path.splitext(dropped_file)[-1] in (".bag", ".csar"):

                            self._add_dtm(selection=dropped_file)

                        else:
                            msg = 'Drag-and-drop is only possible with the following file extensions:\n' \
                                  '- BAG files: .bag\n\n' \
                                  '- CSAR files: .csar\n\n' \
                                  'Dropped file:\n' \
                                  '%s' % dropped_file
                            # noinspection PyCallByClass,PyArgumentList
                            QtWidgets.QMessageBox.critical(self, "Drag-and-drop Error", msg, QtWidgets.QMessageBox.Ok)
                    return True

            elif obj is self.input_ff:

                if e.mimeData().hasUrls():

                    e.setDropAction(QtCore.Qt.CopyAction)
                    e.accept()
                    # Workaround for OSx dragging and dropping
                    for url in e.mimeData().urls():
                        if Helper.is_darwin():
                            dropped_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                        else:
                            dropped_file = str(url.toLocalFile())

                        logger.debug("dropped file: %s" % dropped_file)
                        if os.path.splitext(dropped_file)[-1] in (".000",):
                            self._add_ff(selection=dropped_file)
                        else:
                            msg = 'Drag-and-drop is only possible with the following file extensions:\n' \
                                  '- S57 Feature Files: .000\n\n' \
                                  'Dropped file:\n' \
                                  '%s' % dropped_file
                            # noinspection PyCallByClass,PyArgumentList
                            QtWidgets.QMessageBox.critical(self, "Drag-and-drop Error", msg, QtWidgets.QMessageBox.Ok)
                    return True

            elif obj is self.output_folder:

                if e.mimeData().hasUrls():

                    e.setDropAction(QtCore.Qt.CopyAction)
                    e.accept()
                    # Workaround for OSx dragging and dropping
                    for url in e.mimeData().urls():

                        if Helper.is_darwin():
                            dropped_path = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())

                        else:
                            dropped_path = str(url.toLocalFile())

                        dropped_path = os.path.abspath(dropped_path)

                        logger.debug("dropped file: %s" % dropped_path)
                        if os.path.isdir(dropped_path):
                            self._add_folder(selection=dropped_path)

                        else:
                            msg = 'Drag-and-drop is only possible with a single folder\n'
                            # noinspection PyCallByClass,PyArgumentList
                            QtWidgets.QMessageBox.critical(self, "Drag-and-drop Error", msg, QtWidgets.QMessageBox.Ok)

                    return True

            elif obj is self.qa_json:

                if e.mimeData().hasUrls():

                    e.setDropAction(QtCore.Qt.CopyAction)
                    e.accept()
                    # Workaround for OSx dragging and dropping
                    for url in e.mimeData().urls():
                        if Helper.is_darwin():
                            dropped_file = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                        else:
                            dropped_file = str(url.toLocalFile())

                        logger.debug("dropped file: %s" % dropped_file)
                        if os.path.splitext(dropped_file)[-1] in (".json",):
                            self._add_json(selection=dropped_file)
                        else:
                            msg = 'Drag-and-drop is only possible with the following file extensions:\n' \
                                  '- QA JSON Files: .json\n\n' \
                                  'Dropped file:\n' \
                                  '%s' % dropped_file
                            # noinspection PyCallByClass,PyArgumentList
                            QtWidgets.QMessageBox.critical(self, "Drag-and-drop Error", msg, QtWidgets.QMessageBox.Ok)
                    return True

            e.ignore()
            return True

        return QtWidgets.QMainWindow.eventFilter(self, obj, e)

    def on_set_profiles(self):
        profile_text = self.set_profiles.currentText()
        logger.debug("current profile: %s" % profile_text)

        if profile_text == "NOAA":
            self.set_flier_finder.setChecked(True)
            self.set_flier_finder.setEnabled(False)

            self.set_holiday_finder.setChecked(True)
            self.set_holiday_finder.setEnabled(False)

            self.set_grid_qa.setChecked(True)
            self.set_grid_qa.setEnabled(False)

            self.set_designated_scan.setChecked(True)
            self.set_designated_scan.setEnabled(False)

            self.set_feature_scan.setChecked(True)
            self.set_feature_scan.setEnabled(False)

            self.set_valsou_check.setChecked(True)
            self.set_valsou_check.setEnabled(False)

        elif profile_text == "AusSeabed":
            self.set_flier_finder.setChecked(True)
            self.set_flier_finder.setEnabled(False)

            self.set_holiday_finder.setChecked(True)
            self.set_holiday_finder.setEnabled(False)

            self.set_grid_qa.setChecked(True)
            self.set_grid_qa.setEnabled(False)

            self.set_designated_scan.setChecked(False)
            self.set_designated_scan.setEnabled(False)

            self.set_feature_scan.setChecked(False)
            self.set_feature_scan.setEnabled(False)

            self.set_valsou_check.setChecked(False)
            self.set_valsou_check.setEnabled(False)

        else:
            self.set_flier_finder.setChecked(False)
            self.set_flier_finder.setEnabled(True)

            self.set_holiday_finder.setChecked(False)
            self.set_holiday_finder.setEnabled(True)

            self.set_grid_qa.setChecked(False)
            self.set_grid_qa.setEnabled(True)

            self.set_designated_scan.setChecked(False)
            self.set_designated_scan.setEnabled(True)

            self.set_feature_scan.setChecked(False)
            self.set_feature_scan.setEnabled(True)

            self.set_valsou_check.setChecked(False)
            self.set_valsou_check.setEnabled(True)

    # DTM METHODS

    def click_add_dtm(self):
        """ Read the DTM files provided by the user"""
        logger.debug('adding DTM ...')

        # ask the file path to the user
        # noinspection PyCallByClass
        selections, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Add DTM file",
                                                               QtCore.QSettings().value("dtm_import_folder"),
                                                               "Supported formats (*.bag *.csar);; "
                                                               "BAG file (*.bag);;CSAR file (*.csar);;"
                                                               "All files (*.*)")
        if len(selections) == 0:
            logger.debug('adding dtm: aborted')
            return
        last_open_folder = os.path.dirname(selections[0])
        if os.path.exists(last_open_folder):
            QtCore.QSettings().setValue("dtm_import_folder", last_open_folder)

        for selection in selections:
            selection = os.path.abspath(selection).replace("\\", "/")
            self._add_dtm(selection=selection)

    def _add_dtm(self, selection):

        if selection in self.prj.inputs.dtm_paths:
            logger.info("File already existing in the current project")
            return

        self.prj.inputs.dtm_paths.append(selection)
        self._update_input_dtm_list()
        self.dtm_loaded()

    def _update_input_dtm_list(self):
        self.input_dtm.clear()
        for input_dtm_path in self.prj.inputs.dtm_paths:
            new_item = QtWidgets.QListWidgetItem()
            if os.path.splitext(input_dtm_path)[-1] in [".bag", ]:
                new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 'bag.png')))
            elif os.path.splitext(input_dtm_path)[-1] in [".csar",]:
                new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 'csar.png')))
            new_item.setText(input_dtm_path)
            new_item.setFont(GuiSettings.console_font())
            new_item.setForeground(GuiSettings.console_fg_color())
            self.input_dtm.addItem(new_item)

    def make_dtm_context_menu(self, pos):
        logger.debug('context menu')

        remove_act = QtWidgets.QAction("Remove files", self, statusTip="Remove DTM files",
                                       triggered=self.remove_dtm_files)

        menu = QtWidgets.QMenu(parent=self)
        # noinspection PyArgumentList
        menu.addAction(remove_act)
        # noinspection PyArgumentList
        menu.exec_(self.input_dtm.mapToGlobal(pos))

    def remove_dtm_files(self):
        logger.debug("user want to remove DTM files")

        self.prj.inputs.dtm_paths.clear()
        self._update_input_dtm_list()
        self.dtm_unloaded()

    # Feature File methods

    def click_add_ff(self):
        """ Read the feature files provided by the user"""
        logger.debug('adding feature files ...')

        # ask the file path to the user
        # noinspection PyCallByClass
        selections, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Add S57 Feature Files",
                                                               QtCore.QSettings().value("ff_import_folder"),
                                                               "S57 file (*.000);;All files (*.*)")
        if len(selections) == 0:
            logger.debug('adding s57: aborted')
            return
        last_open_folder = os.path.dirname(selections[0])
        if os.path.exists(last_open_folder):
            QtCore.QSettings().setValue("ff_import_folder", last_open_folder)

        for selection in selections:
            selection = os.path.abspath(selection).replace("\\", "/")
            self._add_ff(selection=selection)

    def _add_ff(self, selection):

        if selection in self.prj.inputs.ff_paths:
            logger.info("File already existing in the current project")
            return

        self.prj.inputs.ff_paths.append(selection)

        self._update_input_ff_list()
        self.ff_loaded()

    def _update_input_ff_list(self):
        """ update the FF list widget """
        self.input_ff.clear()
        for input_ff_path in self.prj.inputs.ff_paths:
            new_item = QtWidgets.QListWidgetItem()
            if os.path.splitext(input_ff_path)[-1] == ".000":
                new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 's57.png')))
            new_item.setText(input_ff_path)
            new_item.setFont(GuiSettings.console_font())
            new_item.setForeground(GuiSettings.console_fg_color())
            self.input_ff.addItem(new_item)

    def make_ff_context_menu(self, pos):
        logger.debug('FF context menu')

        remove_act = QtWidgets.QAction("Remove files", self, statusTip="Remove the FF files",
                                       triggered=self.remove_ff_files)

        menu = QtWidgets.QMenu(parent=self)
        # noinspection PyArgumentList
        menu.addAction(remove_act)
        # noinspection PyArgumentList
        menu.exec_(self.input_ff.mapToGlobal(pos))

    def remove_ff_files(self):
        logger.debug("user want to remove FF files")

        self.prj.inputs.ff_paths.clear()
        self.ff_unloaded()
        self._update_input_ff_list()

    # AUX METHODS

    def click_clear_data(self):
        """ Clear all the read data"""
        logger.debug('clear data')
        self.prj.clear_inputs()

        self.input_dtm.clear()
        self.dtm_unloaded()

        self.input_ff.clear()
        self.ff_unloaded()

    def click_output_kml(self):
        """ Set the KML output"""
        self.prj.params.write_kml = self.output_kml.isChecked()
        QtCore.QSettings().setValue("qax_export_kml", self.prj.params.write_kml)

    def click_output_shp(self):
        """ Set the Shapefile output"""
        self.prj.params.write_shp = self.output_shp.isChecked()
        QtCore.QSettings().setValue("qax_export_shp", self.prj.params.write_shp)

    def click_output_project_folder(self):
        """ Set the output project folder"""
        self.prj.params.project_folder = self.output_prj_folder.isChecked()
        QtCore.QSettings().setValue("qax_export_project_folder", self.prj.params.project_folder)

    def click_output_subfolders(self):
        """ Set the output in sub-folders"""
        self.prj.params.subfolders = self.output_subfolders.isChecked()
        QtCore.QSettings().setValue("qax_export_subfolders", self.prj.params.subfolders)

    def click_add_folder(self):
        """ Read the grids provided by the user"""
        logger.debug('set output folder ...')

        # ask the output folder
        # noinspection PyCallByClass
        selection = QtWidgets.QFileDialog.getExistingDirectory(self, "Set output folder",
                                                               QtCore.QSettings().value("qa_export_folder"),)
        if selection == "":
            logger.debug('setting output folder: aborted')
            return
        logger.debug("selected path: %s" % selection)

        self._add_folder(selection)

    def _add_folder(self, selection):

        path_len = len(selection)
        logger.debug("folder path length: %d" % path_len)
        if path_len > 140:

            msg = 'The selected path is %d characters long. ' \
                  'This may trigger the filename truncation of generated outputs (max allowed path length: 260).\n\n' \
                  'Do you really want to use: %s?' % (path_len, selection)
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setWindowTitle("Output folder")
            msg_box.setText(msg)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
            reply = msg_box.exec_()

            if reply == QtWidgets.QMessageBox.No:
                return

        try:
            self.prj.outputs.output_folder = Path(selection)

        except Exception as e:  # more general case that catches all the exceptions
            msg = '<b>Error setting the output folder to \"%s\".</b>' % selection
            msg += '<br><br><font color=\"red\">%s</font>' % e
            # noinspection PyCallByClass,PyArgumentList
            QtWidgets.QMessageBox.critical(self, "Output Folder Error", msg, QtWidgets.QMessageBox.Ok)
            logger.debug('output folder NOT set: %s' % selection)
            return

        self.output_folder.clear()
        new_item = QtWidgets.QListWidgetItem()
        new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 'folder.png')))
        new_item.setText("%s" % self.prj.outputs.output_folder)
        new_item.setFont(GuiSettings.console_font())
        new_item.setForeground(GuiSettings.console_fg_color())
        self.output_folder.addItem(new_item)

        QtCore.QSettings().setValue("qax_export_folder", self.prj.outputs.output_folder)

        logger.debug("new output folder: %s" % self.prj.outputs.output_folder)

    def click_default_output(self):
        """ Set default output data folder """
        self.prj.outputs.output_folder = self.prj.outputs.default_output_folder()
        self._add_folder(selection=self.prj.outputs.output_folder)
    
    def click_open_output(self):
        """ Open output data folder """
        logger.debug('open output folder: %s' % self.prj.outputs.output_folder)
        self.prj.outputs.open_output_folder()

    def click_generate_checks(self):
        """ Read the feature files provided by the user"""
        logger.debug('generate checks ...')

    # QA JSON methods

    def click_add_json(self):
        """ Read the feature files provided by the user"""
        logger.debug('adding feature files ...')

        # ask the file path to the user
        # noinspection PyCallByClass
        selections, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Add QA JSON Files",
                                                               QtCore.QSettings().value("json_import_folder"),
                                                               "QA JSON file (*.json);;All files (*.*)")
        if len(selections) == 0:
            logger.debug('adding json: aborted')
            return
        last_open_folder = os.path.dirname(selections[0])
        if os.path.exists(last_open_folder):
            QtCore.QSettings().setValue("json_import_folder", last_open_folder)

        for selection in selections:
            selection = os.path.abspath(selection).replace("\\", "/")
            self._add_json(selection=selection)

    def _add_json(self, selection):

        self.prj.inputs.json_path = selection

        self._update_json_list()
        self.json_loaded()

    def _update_json_list(self):
        """ update the FF list widget """
        self.qa_json.clear()
        if self.prj.inputs.json_path is not None:
            new_item = QtWidgets.QListWidgetItem()
            if os.path.splitext(self.prj.inputs.json_path)[-1] == ".json":
                new_item.setIcon(QtGui.QIcon(os.path.join(self.parent_win.media, 'json.png')))
            new_item.setText(self.prj.inputs.json_path)
            new_item.setFont(GuiSettings.console_font())
            new_item.setForeground(GuiSettings.console_fg_color())
            self.qa_json.addItem(new_item)

    def make_json_context_menu(self, pos):
        logger.debug('JSON context menu')

        remove_act = QtWidgets.QAction("Remove file", self, statusTip="Remove the JSON file",
                                       triggered=self.remove_json_file)

        menu = QtWidgets.QMenu(parent=self)
        # noinspection PyArgumentList
        menu.addAction(remove_act)
        # noinspection PyArgumentList
        menu.exec_(self.qa_json.mapToGlobal(pos))

    def remove_json_file(self):
        logger.debug("user want to remove JSON file")

        self.prj.inputs.json_path = None
        self.json_unloaded()
        self._update_json_list()

    # interaction methods

    def dtm_loaded(self):
        logger.debug("DTM loaded")

    def dtm_unloaded(self):
        logger.debug("DTM unloaded")

    def ff_loaded(self):
        logger.debug("FF loaded")

    def ff_unloaded(self):
        logger.debug("FF unloaded")

    def json_loaded(self):
        logger.debug("JSON loaded")

    def json_unloaded(self):
        logger.debug("JSON unloaded")

    # common
    @classmethod
    def click_open_manual(cls):
        logger.debug("open manual")
        Helper.explore_folder("https://www.hydroffice.org/manuals/qax/user_manual_qax_data_inputs.html")
