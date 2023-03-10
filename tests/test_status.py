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
    incidents = ['2/6/2023 23:17', '2022-00001877', '17901 E STATE HWY 9 HWY', 'Breathing Problems', '14005', '2/6/2023 23:17', '2022-00002403', '17901 E STATE HWY 9 HWY', 'Breathing Problems', 'EMSSTAT', '2/6/2023 23:18', '2023-00006620', '1357 12TH AVE NE', 'Contact a Subject', 'OK0140200']
    insert = [tuple(incidents[i:i+5]) for i in range(0, len(incidents), 5)]

    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", insert)

    yield con
    con.close()

def test_status(setup_database, capfd):
    con= setup_database
    project0.status(con)
    out, err = capfd.readouterr()
    assert out == 'Breathing Problems | 2\nContact a Subject | 1\n'
