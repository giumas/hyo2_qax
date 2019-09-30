from hyo2.abc.lib.helper import Helper
from pathlib import Path
from PySide2 import QtCore, QtGui, QtWidgets
from typing import List, NoReturn
import logging
import os
import re

from hyo2.qax.app.gui_settings import GuiSettings
from hyo2.qax.lib.config import QaxConfigSurveyProduct

logger = logging.getLogger(__name__)


class SurveyProductWidget(QtWidgets.QWidget):
    """ Widget to support selection of one or more files for a *single* survey
    product. """

    # emitted when a new file is selected
    files_added = QtCore.Signal(QaxConfigSurveyProduct)
    # emitted when a list of selected files is cleared
    files_removed = QtCore.Signal(QaxConfigSurveyProduct)

    def __init__(self, survey_product: QaxConfigSurveyProduct, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.survey_product = survey_product
        hbox = QtWidgets.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignTop)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        self.selected_files = []

        left_space = 100

        label_layout = QtWidgets.QVBoxLayout()
        label_layout.setAlignment(QtCore.Qt.AlignTop)
        label = QtWidgets.QLabel("{}:".format(survey_product.name))
        label.setMinimumWidth(left_space)
        label_layout.addWidget(label)
        hbox.addLayout(label_layout)

        self.file_list = QtWidgets.QListWidget()
        hbox.addWidget(self.file_list)
        self.file_list.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.file_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(
            self.__make_context_menu)
        self.file_list.setAlternatingRowColors(True)
        self.file_list.setMaximumHeight(100)
        # Enable dropping onto the input ss list
        self.file_list.setAcceptDrops(True)
        self.file_list.installEventFilter(self)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignTop)
        self.add_file_button = QtWidgets.QPushButton()
        button_layout.addWidget(self.add_file_button)
        self.add_file_button.setFixedHeight(GuiSettings.single_line_height())
        self.add_file_button.setFixedWidth(GuiSettings.single_line_height())
        self.add_file_button.setText(" + ")
        self.add_file_button.setToolTip(
            "Add (or drag-and-drop) the survey {} files"
            .format(survey_product.name))
        hbox.addLayout(button_layout)

        self.add_file_button.clicked.connect(self._click_add)

    def eventFilter(self, obj, e):
        """ Captures events for the purpose of supporting drag and drop of
        files onto the appropriate file lists
        """
        # note for a drop event to be handled, the drag enter or drag move
        # events must be accepted.

        # drag events
        if (
            (e.type() == QtCore.QEvent.DragEnter) or
            (e.type() == QtCore.QEvent.DragMove)
        ):
            if (obj is not self.file_list) and (not e.mimeData().hasUrls):
                e.ignore()
                return False

            for url in e.mimeData().urls():
                dropping_file = str(url.toLocalFile())
                extension = os.path.splitext(dropping_file)[-1].lower()
                extension = extension.lstrip('.')
                acceptable_extensions = [
                    ft.extension for ft in self.survey_product.file_types]
                if extension in acceptable_extensions:
                    e.accept()
                    return True
                e.ignore()
                return True

        # drop events
        if (
            e.type() == QtCore.QEvent.Drop and
            obj is self.file_list and
            e.mimeData().hasUrls()
        ):
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                dropped_file = str(url.toLocalFile())

                logger.debug("dropped file: %s" % dropped_file)
                extension = os.path.splitext(dropped_file)[-1].lower()
                extension = extension.lstrip('.')
                acceptable_extensions = [
                    ft.extension for ft in self.survey_product.file_types]
                if extension in acceptable_extensions:
                    self.selected_files.append(dropped_file)
                    self._update_file_list()
                    self.files_added.emit(self.survey_product)
                else:
                    # note: the following code is never called as only
                    # accepted drag events (enter and move) will make it here.
                    # And we validate for valid extensions in the enter and
                    # move handlers above. non acceptable_extensions events
                    # are ignored.
                    names = [
                        "- {}".format(ft.formatted_name())
                        for ft in self.survey_product.file_types]
                    msg = (
                        'Drag-and-drop is only possible with the ' +
                        'following file extensions:\n' +
                        '{}\n'.format("\n".join(names)) +
                        'Dropped file:\n'
                        '{}'.format(dropped_file))
                    # noinspection PyCallByClass,PyArgumentList
                    QtWidgets.QMessageBox.critical(
                        self, "Drag-and-drop Error", msg,
                        QtWidgets.QMessageBox.Ok)
            return True

        # if event not handled defer to default event handler
        return QtWidgets.QMainWindow.eventFilter(self, obj, e)

    def _click_add(self):
        """ Add files selected by user. Opens file selection dialog
        """
        import_folder_name = "{}_import_folder".format(
            self.survey_product.clean_name())

        filters = []
        if len(self.survey_product.file_types) > 0:
            all_ext = [
                "*.{}".format(ft.extension)
                for ft in self.survey_product.file_types]
            all_formats = "Supported formats ({})".format(" ".join(all_ext))
            filters.append(all_formats)
            for ft in self.survey_product.file_types:
                filters.append("{} (*.{})".format(ft.name, ft.extension))
        filters.append("All files (*.*)")

        # ask the file path to the user
        # noinspection PyCallByClass
        selections, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Add {} file".format(self.survey_product.name.lower()),
            QtCore.QSettings().value(import_folder_name),
            ";; ".join(filters))
        if len(selections) == 0:
            logger.debug('adding raw: aborted')
            return
        last_open_folder = os.path.dirname(selections[0])
        if os.path.exists(last_open_folder):
            QtCore.QSettings().setValue(import_folder_name, last_open_folder)

        selected_files = [
            os.path.abspath(selection).replace("\\", "/")
            for selection in selections
        ]
        self.selected_files = selected_files
        self._update_file_list()
        self.files_added.emit(self.survey_product)

    def __make_context_menu(self, pos):
        remove_action = QtWidgets.QAction(
            "Remove files",
            self,
            statusTip="Remove {} files".format(
                self.survey_product.name.lower()),
            triggered=self.remove_files)

        menu = QtWidgets.QMenu(parent=self)
        menu.addAction(remove_action)
        menu.exec_(self.file_list.mapToGlobal(pos))

    def remove_files(self) -> NoReturn:
        """ Clears the list of selected files """
        logger.debug("user want to remove raw files")
        self.file_list.clear()
        self.selected_files.clear()
        self.files_removed.emit(self.survey_product)

    def _update_file_list(self) -> NoReturn:
        self.file_list.clear()
        for selected_file in self.selected_files:
            file_item = QtWidgets.QListWidgetItem()
            file_item.setText(selected_file)
            file_item.setFont(GuiSettings.console_font())
            file_item.setForeground(GuiSettings.console_fg_color())

            path = Path(selected_file)
            matching_file_type = self.survey_product.matching_file_type(path)
            if (
                (matching_file_type is not None) and
                (matching_file_type.icon is not None)
            ):
                file_type_icon = QtGui.QIcon(os.path.join(
                    GuiSettings.media(), matching_file_type.icon))
                file_item.setIcon(file_type_icon)

            self.file_list.addItem(file_item)


class SurveyProductGroupBox(QtWidgets.QGroupBox):
    """ Widget to support selection of survey products (the input files) that
    will be passed to the check tools. Widget includes multiple
    `SurveyProductWidget` instances.
    """

    # emitted when a new file is selected, in one of the survey prod widgets
    files_added = QtCore.Signal(QaxConfigSurveyProduct)
    # emitted when a list or all survey product lists of files are cleared
    files_removed = QtCore.Signal(QaxConfigSurveyProduct)

    def __init__(self, parent_win, prj):
        QtWidgets.QGroupBox.__init__(self, "Survey Products")
        self.setStyleSheet("QGroupBox::title { color: rgb(155, 155, 155); }")

        self.prj = prj
        self.parent_win = parent_win
        self.survey_product_widgets = []

        main_layout = QtWidgets.QVBoxLayout()
        self.survey_products_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.survey_products_layout)

        self.setLayout(main_layout)

        # clear data
        hbox = QtWidgets.QHBoxLayout()
        main_layout.addLayout(hbox)
        hbox.addStretch()
        self.clear_button = QtWidgets.QPushButton()
        hbox.addWidget(self.clear_button)
        self.clear_button.setFixedHeight(GuiSettings.single_line_height())
        # button_clear_data.setFixedWidth(GuiSettings.single_line_height())
        self.clear_button.setText("Clear data")
        self.clear_button.setToolTip('Clear all data loaded')
        # noinspection PyUnresolvedReferences
        self.clear_button.clicked.connect(self._click_clear_data)
        # info
        manual_button = QtWidgets.QPushButton()
        hbox.addWidget(manual_button)
        manual_button.setFixedHeight(GuiSettings.single_line_height())
        manual_button.setFixedWidth(GuiSettings.single_line_height())
        icon_info = QtCore.QFileInfo(
            os.path.join(GuiSettings.media(), 'small_info.png'))
        manual_button.setIcon(QtGui.QIcon(icon_info.absoluteFilePath()))
        manual_button.setToolTip('Open the manual page')
        manual_button.setStyleSheet(
            "QPushButton { background-color: rgba(255, 255, 255, 0); }\n"
            "QPushButton:hover "
            "{ background-color: rgba(230, 230, 230, 100); }\n")
        # noinspection PyUnresolvedReferences
        manual_button.clicked.connect(self._click_open_manual)
        hbox.addStretch()

    def _click_clear_data(self):
        logger.debug("clearing selected input files")
        for sp_widget in self.survey_product_widgets:
            sp_widget.remove_files()

    def _click_open_manual(self):
        logger.debug("open manual")
        Helper.explore_folder(
            "https://www.hydroffice.org/"
            "manuals/qax/user_manual_qax_data_inputs.html")

    def _on_files_added(self, survey_product: QaxConfigSurveyProduct):
        # propogate events up GUI component tree to parent
        self.files_added.emit(survey_product)

    def _on_files_removed(self, survey_product: QaxConfigSurveyProduct):
        # propogate events up GUI component tree to parent
        self.files_removed.emit(survey_product)

    def update_survey_products(
            self, survey_products: List[QaxConfigSurveyProduct]
            ) -> NoReturn:
        """ Updates the various lists of files based on the `survey_products`
        list
        """
        # clear all items from survey products layout
        for sp_widget in self.survey_product_widgets:
            sp_widget.setParent(None)
        self.survey_product_widgets.clear()

        for survey_product in survey_products:
            sp_widget = SurveyProductWidget(survey_product, self)
            sp_widget.files_added.connect(self._on_files_added)
            sp_widget.files_removed.connect(self._on_files_removed)
            self.survey_products_layout.addWidget(sp_widget)
            self.survey_product_widgets.append(sp_widget)
