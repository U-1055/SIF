import json
from abc import abstractmethod
from pathlib import Path
from src.gui.interfaces import config
from src.gui.interfaces import ConfigStruct

class CaseFields:
    TEST_NUM = 'test_num'
    TEST_CONTENT = 'test_content'

test_case = {
    CaseFields.TEST_NUM: '',
    CaseFields.TEST_CONTENT: config
}


class BaseTest:
    """
    The base test class that provides methods for operations with test cases.
    :param case_dir: a directory that contains the test cases.
    """
    def __init__(self, case_dir: Path):
        self._case_dir = case_dir

    def get_test_case(self, num: int) -> dict:
        """
        Returns a test case by given number. Test case is in format: {TEST_NUM: a num of the test, TEST_CONTENT: config}
        """
        cases = tuple(self._case_dir.iterdir())
        with open(Path(cases[num]), 'rb') as case:
            return json.load(case)

    def check_config(self, case_num: int, config_: ConfigStruct):
        cases = tuple(self._case_dir.iterdir())
        with open(Path(cases[case_num]), 'rb') as test_case:
            test_case = json.load(test_case)
        assert test_case[CaseFields.TEST_CONTENT] == config_[CaseFields.TEST_CONTENT],\
            (f'The config must be equal with the test config. Config: \n{config_[CaseFields.TEST_CONTENT]}\n'
             f'Test_config: \n{test_case[CaseFields.TEST_CONTENT]}')
        print(f'Test complete || Case: {case_num}')
