from ausseabed.qajson.model import QajsonRoot, QajsonCheck
from ausseabed.qajson.parser import QajsonParser
from ausseabed.qajson.utils import qajson_valid
from collections import defaultdict
from hyo2.abc.lib.helper import Helper
from hyo2.qax.lib import lib_info
from jsonschema import validate, ValidationError, SchemaError, Draft7Validator
from pathlib import Path
from PySide2 import QtCore
from typing import Optional, NoReturn, List
import json
import logging
import os
import time
import traceback

from hyo2.qax.lib.inputs import QAXInputs
from hyo2.qax.lib.params import QAXParams


logger = logging.getLogger(__name__)


class QaCheckSummary():
    """ Class defines properties that make up a summary of a single QA
    check that may have been run multiple times.
    """

    @classmethod
    def __process_check_summary(
            cls,
            data_level: str,
            check: QajsonCheck,
            summaries: dict) -> NoReturn:
        # a name and id tuple is used to reference the summaries
        nid = (check.info.id, check.info.name)
        if nid in summaries:
            summary = summaries[nid]
        else:
            summary = QaCheckSummary(
                id=check.info.id, name=check.info.name,
                version=check.info.version, data_level=data_level)
            summaries[nid] = summary

        summary.add_check(check)

    @classmethod
    def get_summary(cls, qa_json: QajsonRoot) -> List['QaCheckSummary']:
        """ Builds a list of check summaries from the qa json object
        """
        summaries = {}  # tuple of check id and name used as key
        if qa_json.qa is not None:
            for check in qa_json.qa.raw_data.checks:
                QaCheckSummary.__process_check_summary(
                    'raw_data', check, summaries)
            for check in qa_json.qa.survey_products.checks:
                QaCheckSummary.__process_check_summary(
                    'survey_products', check, summaries)

            if qa_json.qa.chart_adequacy is not None:
                for check in qa_json.qa.chart_adequacy.checks:
                    QaCheckSummary.__process_check_summary(
                        'chart_adequacy', check, summaries)

        return list(summaries.values())

    def __init__(self, id: str, name: str, version: str, data_level: str):
        """ Constructor

        :param str id: id of the check that is summarised by this object
        :param str name: name of the check that is summarised by this object
        :param str version: version of the check that is summarised by this
            object
        :param str data_level: data level where the check was found
        """
        self.id = id
        self.name = name
        self.version = version
        self.data_level = data_level
        self.total_executions = 0
        self.failed_executions = 0
        self.failed_execution_files = []
        self.failed_check_state = 0
        self.failed_check_state_files = []
        self.warning_check_state = 0
        self.warning_check_state_files = []

        # collection of checks that make up this summary
        self.checks = []

    def add_check(self, check) -> None:
        """ Adds a check to this summary
        """
        self.checks.append(check)

        if (check.outputs is not None and check.outputs.execution is not None):
            self.total_executions += 1
            if check.outputs.execution.status == 'failed':
                self.failed_executions += 1
                self.failed_execution_files.extend(check.inputs.files)
            if check.outputs.check_state == 'fail':
                self.failed_check_state += 1
                self.failed_check_state_files.extend(check.inputs.files)
            if check.outputs.check_state == 'warning':
                self.warning_check_state += 1
                self.warning_check_state_files.extend(check.inputs.files)

    def __repr__(self) -> str:
        return (
            "id = {} \n"
            "name = {} \n"
            "total_executions = {} \n"
            "failed_executions = {} \n"
            "failed_check_state = {} \n"
        ).format(
            self.id, self.name, self.total_executions, self.failed_executions,
            self.failed_check_state)


# inherits from QObject to support signals
class QAXProject(QtCore.QObject):
    """ Class represents the current QAX project as configured by the user.
    This includes option settings, QA JSON details are persisted elsewhere.
    """

    qa_json_changed = QtCore.Signal(QajsonRoot)
    qa_json_path_changed = QtCore.Signal(Path)

    @classmethod
    def default_output_folder(cls):
        output_folder = Helper(lib_info=lib_info).package_folder()
        # create it if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        return output_folder

    def __init__(self):
        super(QAXProject, self).__init__()

        self._qa_json = None  # QajsonRoot
        self._qa_json_path = None
        self._output_folder = QAXProject.default_output_folder()

        self._p = QAXParams()
        self._i = QAXInputs()

    @property
    def qa_json(self) -> Optional[QajsonRoot]:
        return self._qa_json

    @qa_json.setter
    def qa_json(self, value: Optional[QajsonRoot]) -> NoReturn:
        self._qa_json = value
        self.qa_json_changed.emit(self._qa_json)

    @property
    def qa_json_path(self) -> Optional[Path]:
        return self._qa_json_path

    @qa_json_path.setter
    def qa_json_path(self, value: Optional[Path]) -> NoReturn:
        self._qa_json_path = value
        self.qa_json_path_changed.emit(self._qa_json_path)

    @property
    def output_folder(self) -> Optional[Path]:
        return self._output_folder

    @output_folder.setter
    def output_folder(self, value: Optional[Path]) -> NoReturn:
        self._output_folder = value

    def open_output_folder(self) -> None:
        if self.output_folder:
            Helper.explore_folder(str(self.output_folder))
        else:
            logger.warning('unable to define the output folder to open')

    def get_qa_json_path(self) -> Path:
        if self.qa_json_path is not None:
            return self.qa_json_path
        if self.output_folder is not None:
            return self.output_folder.joinpath('qa.json')
        if QAXProject.default_output_folder() is not None:
            return QAXProject.default_output_folder().joinpath('qa.json')
        raise RuntimeError("could not construct qa json path")

    def save_qa_json(self) -> NoReturn:
        path = self.get_qa_json_path()
        if self.qa_json_path is None or str(path) != str(self.qa_json_path):
            # then set the qa json path to fire events so the ui updates
            # to show where the qa json file was written
            self.qa_json_path = path
        logger.debug("save json to {}".format(path))
        with open(str(path), "w") as file:
            json.dump(self.qa_json.to_dict(), file, indent=4)

    def open_qa_json(self) -> NoReturn:
        path = self.qa_json_path
        qajsonparser = QajsonParser(path)
        self.qa_json = qajsonparser.root

    def get_summary(self) -> List[QaCheckSummary]:
        return QaCheckSummary.get_summary(self.qa_json)

    def is_qajson_valid(self) -> bool:
        ''' Checks if the qa json object is valid. This may return false if the
        user has entered invalid information into the check parameters (for
        example).
        '''
        return qajson_valid(self.qa_json)

    @property
    def params(self) -> QAXParams:
        return self._p

    @params.setter
    def params(self, value: QAXParams) -> None:
        self._p = value

    @property
    def inputs(self) -> QAXInputs:
        return self._i

    @inputs.setter
    def inputs(self, value: QAXInputs) -> None:
        self._i = value

    def clear_inputs(self):
        self._i = QAXInputs()

    def execute_all(self, qa_group: str = "survey_products"):
        checks = self.inputs.qa_json.js['qa'][qa_group]['checks']
        logger.debug("checks: %s" % checks)
        nr_of_checks = len(checks)
        for idx in range(nr_of_checks):
            # TODO
            checks[idx]['outputs']['execution']['status'] = "completed"

    def __repr__(self):
        msg = super().__repr__()
        msg += "\n"
        msg += "%s" % (self._p,)
        msg += "%s" % (self._i,)
        msg += "%s" % (self._o,)
        return msg
