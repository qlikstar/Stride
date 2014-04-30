Stride
======

Python Doctors - Question
===========================

Inputs:

doctors.txt -- a text file containing doctor 5000 records, each record is in a json formatted object. Each line contains a single doctor object.

driver.py -- a python file that is the main application driver

model.py -- a class file representing a Provider object, also enabled with a sqlalchemy ORM to allow for easy integration with a postgres rdbms.

app_config.ini -- a configuration file that is used by model.py for database configuration

zip_geo.csv -- a csv file containing zipcodes and their respective latitude and longitude (for use in bonus question only)


Challenge objective: Load and parse a file containing doctor records, and load them into the database:


Read the doctors.txt file in using python and load each record into a dictionary object (hint: look at the json.loads library).

For each record, parse the name attribute into separate variables for firstname, lastname, and credentials (hint: use the re module). Extra credit for identifying a record is a duplicate based on the name and address data.

After parsing each record, create an object instance for each provider

Enable database storage using Postgresql for the provider objects. Most of this code exists in what is provided, you simply need to connect a running database to it.

Extend the driver.py to accept a query option which runs a query against the database to select the distinct number of doctors in each zipcode. Write the result records to a csv file.


Bonus: Extend your code to use geo coordinates. For each doctor record, append a latitude and longitude value using the zip_geo.csv file to each doctor’s record. Extend your data model to support the POINT data type which allows for distance based queries. Create a query that counts the number of doctors within an X-mile readius of the inputted zipcode, where X is a integer value.


Code dependencies:

pip -- python package manager (is preinstalled on most machines). It’s similar to homebrew or apt, only specific to python.

psycopg2 -- module for the postgres database driver. You can install with pip.

sqlalchemy -- module for database ORM. You can install with pip.

Postgres -- database system.

argparse (in driver.py) and ConfigParser (in models.py) are modules which may need to be installed using pip.
