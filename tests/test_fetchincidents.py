from types import NoneType
import sqlite3
import pytest
from io import StringIO
import PyPDF2
#from project0 import project0
from os import path
#from ../..project0 import project0
import sys
sys.path.append(path.abspath('../project0'))
#from cs5493sp23-project0.project0
import project0

import warnings
warnings.filterwarnings("ignore", message=".*U.*mode is deprecated:DeprecationWarning")
@pytest.fixture(scope='module')



def test_fetchincidents_for_valid_url():
    valid_url = 'https://www.normanok.gov/sites/default/files/documents/2023-02/2023-02-01_daily_incident_summary.pdf'
    extract = project0.fetchincidents(valid_url)

    assert len(extract) > 0


def test_fetchincidents_for_invalid_url():
    invalid_url = 'https://www.normanok.gov.pdf'
    extract = project0.fetchincidents(invalid_url)

    assert isinstance(extract, NoneType)
