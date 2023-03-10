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


@pytest.fixture
def setup_database():
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS incidents")
    cur.execute("""CREATE TABLE incidents
            (incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT)""")
    yield con
    con.close()

@pytest.fixture
def setup_test_data(setup_database):
    cur = setup_database
    incidents = ['2/6/2023 23:17', '2023-00001877', '17901 E STATE HWY 9 HWY', 'Breathing Problems', '14005', '2/6/2023 23:22', '2023-00006619', 'Unknown Nature', 'Unknown Nature', '14009']
    yield cur, incidents

def test_populatedb(setup_test_data):
    cur, incidents = setup_test_data
    project0.populatedb(cur, incidents)
    rows = cur.execute('select * from incidents')
    assert len(rows.fetchall()) == 2
