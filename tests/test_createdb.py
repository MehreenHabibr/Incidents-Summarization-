
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
#import warnings
#warnings.filterwarnings("ignore", message=".*U.*mode is deprecated:DeprecationWarning")
#@pytest.fixture(scope='module')



sys.path.append(path.abspath('../project0'))
@pytest.fixture
def database_creation():
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS incidents")
    cur.execute("""CREATE TABLE incidents
            (incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT)""")
    yield conn
    conn.close()

def test_createdb(database_creation):
    conn = project0.createdb()
    assert isinstance(conn, type(database_creation))
    conn.close()

