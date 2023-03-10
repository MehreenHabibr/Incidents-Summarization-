**MEHREEN HABIB**
---------
> #### Project Title: CS5293, spring 2023 Project 0
#### Project Description:
 **This project involves taking the URL of an incident summary report from the Norman Police department, if URL does not contain word incidents then we get an error message. Extracting data from the PDF file, and then inserting that data into a database. 
 The project then Print each nature and the number of times it appear.**
 
 #### Installation
  ****
   1. **PyPDF2** - Utility to read and write PDFs with Python
   2. **autopep8** - Tool that automatically formats Python code 
  3. **Pytest** - Testing framework
 4. **Black** - Code formatter

pipenv install

Packages required to run this project are kept in requirements.txt file which automatically installs during installation of pipenv in step 1.

##### PyPDF2==1.26.0


##### pytest==7.2.2

Once, the packages are successfully installed, the project can be executed using

#### python3 main.py --incidents URL.
##### URL must only be a daily incident summary report from Norman Police Department Activity for this project, otherwise an error message will appear.
Pytests can run using below command

pipenv run python -m pytest.
### Assumptions:
1. Assuming there are only five columns (Datetime, Incident Number, Location, Nature and Incident ORI) for each incident. If that is changed, the utility may fail to extract incidents.
2. Assuming URL of Incident Summary report has word incident in it.
3. Assuming Location is split into maximum of 2 lines in any row.
****
### Database Approach
#### **createdb()** This function creates an SQLite database i.e. normanpd.db and inserts the incidents table.
 #### **populatedb(conn, incidents)** This function takes incidents and inserts that data to table created in createdb() method.
 #### **status(conn)** This function prints nature of incidents and number of times it appear.
 ****

Link to VIDEO : https://github.com/MehreenHabibr/cs5293sp23-project0/blob/753bfde028d97498b993c7ce586828828e5ce3a4/Recording%20%232.mp4
