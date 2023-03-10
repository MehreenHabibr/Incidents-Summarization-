import io
import requests
import sqlite3
import urllib.request
import re
import argparse
import PyPDF2
import tempfile

def fetchincidents(url):

    '''
    This function opens a given URL and reads its data. The function takes a string parameter 'url' which contains the URL of the incident summary report.
    The function returns the data from a PDF file as bytes.
    '''
    if (re.search(r'incident', url)):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        return data
    else:
        print(' Please provide correct  URL')

def extractincidents(data):
    '''
    The function takes data in bytes from a PDF file as input. It extracts each row from the file and handles any edge cases that may arise. 
    The output is a list of strings, with each element representing an element in a row.
    '''
    rowsList = []
    fp = tempfile.TemporaryFile()
    fp.write(data)
    fp.seek(0)
    pdf_Reader = PyPDF2.pdf.PdfFileReader(fp)
    page_count = pdf_Reader.getNumPages()
    for page_number in range(page_count):
            page = pdf_Reader.getPage(page_number).extractText().split("\n")
            if page_number == 0:
                page = clean_first_page(page)
            elif page_number == page_count - 1:
                page = clean_last_page(page)
            else:
                page = clean_other_pages(page)
            for row in page:
                rowsList.append(row)
    cleaned_data = handle_edge_cases(rowsList)
    return cleaned_data

def clean_first_page(page):
    """
    It removes the headings, column names, and any whitespace characters present in the list and returns the updated list.
    """
    clean_page = []
    for line in page:
        line = line.strip()  # remove whitespace characters
        if re.match(r'^(\d{1,2}\/){2}\d{4} \d{1,2}:\d{2}$', line):
            continue  # skip date/time line
        if re.match(r'^Location.*Nature.*$', line):
            continue  # skip header row
        if re.match(r'^\s*$', line):
            continue  # skip empty lines
        clean_page.append(line)
    return clean_page

def clean_other_pages(page):
    """
    It removes the last item in the list and returns the updated list.
    """
    return page[:-1]
def clean_last_page(page):
    """
    The function takes a list of strings as an input parameter, which represents the elements on a PDF page. It removes the last two items from the list and returns the updated list.
    """
    return page[:-2]


def handle_edge_cases(rowsList):
    """
    This function deals with exceptional cases in each row of a PDF file. If column 4 (Nature) is missing in the PDF, it inserts the value "Unknown Nature" in that column.
    If column 3 (Location) is separated into multiple blocks, the function combines them. The input parameter is a list of strings, where each element corresponds to a row in the PDF.
    """
    List = []
    List_final = []
    pointer = 0
    count = 0
    while pointer < len(rowsList):

        if count < 5:
            List.append(rowsList[pointer])
            count = count +1
            pointer = pointer +1
        searchIndex = find_match_index(List)
        if count == 5 and searchIndex == 0:
            tempList = []
            for i in range(0, 2):
                tempList.append(List[i])
            location = List[2] + " " + List[3]
            tempList.insert(2, location)
            tempList.insert(3, List[len(List)-1])
            tempList.insert(4, rowsList[pointer])
            pointer = pointer +1
            List = tempList
        if count == 5 or pointer == len(rowsList):
            searchIndex = find_match_index(List)
            if searchIndex == 4:
                for i in range(0, searchIndex + 1):
                    List_final.append(List[i])
                count = 0
                List = []
            elif searchIndex == 3:
                for i in range(0, searchIndex):
                    List_final.append(List[i])
                notNULLValues = 4 - searchIndex
                for times in range(0, notNULLValues):
                    List_final.append("NULL")
                List_final.append(List[searchIndex])
                pointer -= notNULLValues
                count = 0
                List = []
            elif searchIndex == 2:
                for i in range(0, searchIndex):
                    List_final.append(List[i])
                noUnknownValues = 4 - searchIndex
                for times in range(0, notNULLValues):
                    List_final.append("NULL")
                List_final.append(List[searchIndex])
                pointer =pointer - notNULLValues


                count = 0 
                List = []
    return List_final

def find_match_index(st):
    """
    This function searches for a particular pattern within a string using regular expressions. It takes a partition list as input to find the index of a location identifier.
    It returns the index of the matching string in the list, or 0 if there is no match.
    """
    for i, item in enumerate(st):
        if re.search(r"OK(\d{7})", item) or re.search(r"1400([0-9]{1})", item) or re.search(r"EMSSTAT", item):
            return i
    return 0

def createdb():
    """
    Creates an SQLite database and inserts table .
    """
    conn = sqlite3.connect("normanpd.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS incidents")
    cur.execute(
        """CREATE TABLE incidents
            (incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT)"""
    )
    conn.commit()
    return conn


def populatedb(conn, incidents):
    """
        Inserts incidents data into database
    """
    cur = conn.cursor()

    insert = [tuple(incidents[i:i+5]) for i in range(0, len(incidents), 5)]

    cur.executemany("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", insert)
    conn.commit()


def status(conn):
    """
        prints the nature of incidents and no of times it appear
    """
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT NATURE, COUNT(*)  FROM INCIDENTS GROUP BY nature ORDER BY count(*) DESC, nature ASC"
    ).fetchall()
    for i in rows:

         print(i[0], "| ", i[1])
    
    conn.close()

