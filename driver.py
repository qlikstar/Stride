import json # json library
import re   # regex library
import os.path 
import argparse # argument parser library
from sqlalchemy.sql import label, select
import time

# import our Provider model class and database session elements
from model import engine, Session, Base, func
from model import Provider, Zip_geo

# Write to CSV file
def write_csv(result):
    if os.path.isfile('output.csv'):
        with open('output.csv', 'a') as f:
            f.write (result.Zipcode +','+ str(result.Count) +'\n' )
    else:
        with open('output.csv', 'w') as f:
            f.write ('Zipcode,Count of Doctors\n')


# Query to count the number of doctors by zipcode
def count_distinct(db_enabled):

    # if db is enabled, then open a session with the database
    if db_enabled:
        session = Session()

        # if db is enabled, then query the database and w
        results = session.query(label ('Zipcode', Provider.zipcode),
            label('Count', func.count(Provider.firstname+Provider.lastname+Provider.credentials))).group_by(Provider.zipcode).order_by('"Count" desc').all()    
    
        session.close()
        
        # Write the output to CSV file
        for result in results:
            write_csv(result)
            
        print 'Data saved to output.csv'



# Insert ZIPCODE information in the table
def add_zipdata(db_enabled, zipcode, latitude, longitude):
    
    # if db is enabled, then open a session with the database
    if db_enabled:
        session = Session()

    # create an instance of the Zip_Geo type
    zip_geo= Zip_geo(zipcode=zipcode, latitude=latitude, longitude=longitude)

    # if db is enabled, then add to the recordset and commit the txn
    if db_enabled:
        session.add(zip_geo)
        session.commit()
        session.close()
                  
    return zip_geo


# this method creates a Provider instance and optionally adds the user to a db session
def add_provider(db_enabled, lastname, firstname, credentials, addr1, addr2, city, zipcode, state,latitude, longitude):

    # if db is enabled, then open a session with the database
    if db_enabled:
        session = Session()

        # create an instance of the Provider type
        provider = Provider(lastname=lastname, firstname=firstname,
                            credentials=credentials, addr1=addr1, addr2=addr2,
                            city=city, zipcode=zipcode,state=state,
                            latitude=latitude, longitude=longitude)


    #To check if the record already exists in database 
    p = select([Provider.firstname]).where(Provider.firstname+Provider.lastname+Provider.credentials
                                           +Provider.addr1+Provider.addr2 == firstname+lastname+credentials+addr1+addr2)

    res = session.execute(p)
    prov_data = res.fetchone()
    session.close()    

    #To check if record exists, then this step will be skipped
    if not(prov_data):
        session = Session()
        # To fetch the Geographical coordinates from Zip_geotable 
        z = select([Zip_geo.latitude, Zip_geo.longitude]).where(Zip_geo.zipcode == zipcode)
        result = session.execute(z)
        geo_data = result.fetchone()

        if geo_data:
            latitude = geo_data.latitude
            longitude= geo_data.longitude
            #print db_enabled, lastname, firstname, credentials, addr1, addr2, city, zipcode, state,latitude, longitude
            
            
            # create an instance of the Provider type
            provider = Provider(lastname=lastname, firstname=firstname,
                                credentials=credentials, addr1=addr1, addr2=addr2,
                                city=city, zipcode=zipcode,state=state,
                                latitude=latitude, longitude=longitude)            
            

            # if db is enabled, then add to the recordset and commit the txn
            session.add(provider)
            session.commit()
            session.close()
                
    return provider


#Parsing the zip geo codes
def parse_zipgeo(data, db_enabled=True):
    
    output = filter(None, data.split('\n'))
        
    for record in output:
        zipdata = filter(None, record.split(','))
        add_zipdata(db_enabled, str(zipdata[4].strip()), str(zipdata[6].strip()), str(zipdata[7].strip())) 



# parse each record, creating Provider object instance for all valid records
# if db_enabled, then also insert into the databases
def parse_records(data, db_enabled=True):

    jsondict = {}
    output = filter( None, data.split('\n') )
    
    for record in output:

        # hint: you can call add_provider from here as you handle each record
        jsondict = json.loads(record)
        extname  = jsondict['name'].split(',')
        addr1    = jsondict['Address1'].strip()
        addr2    = jsondict['Address2'].strip()
        city     = jsondict['City'].strip()
        zipcode  = jsondict['Zipcode'].strip()
        state    = jsondict['State'].strip()
        
        name = map(lambda x: x.strip(), extname)
        lastname = name[0]
        try:
            firstnameplus = name[1]
        except IndexError:
            firstnameplus = 'Not Found'
            
        if firstnameplus == 'Not Found':
            firstnameplus = lastname
            lastname = '' 
        
        
        listop = re.match('(?P<first>.*)\s+(?P<credentials>[A-Z]{2,3})', firstnameplus)

        if listop:
            credentials = (listop.group("credentials")) 
            firstname = (listop.group("first")) 
        else:
            firstname = firstnameplus
            credentials = ''
        latitude  = ''
        longitude = ''    
            
        add_provider(db_enabled,str(lastname),str(firstname),str(credentials),str(addr1),
                     str(addr2),str(city),str(zipcode),str(state),latitude, longitude)

# implement a method to read the file
# the result should be a list containing an entry for each line/record
# each record can also be represented as a list containing the record details
def read_file(filename):

    # code goes here to read the file into the file_data list
    with open(filename , 'r') as f: 
        file_data = f.read()
    return file_data


if __name__ == "__main__":
    global_start = time.time()
    print 'Welcome to the magical world of Python'

    # handle file here!
    parser = argparse.ArgumentParser(description = "Provider data load and extract tool")
    parser.add_argument('-load', action='store', dest='load_files',
                        help='load a provider file',required=False)

    args = parser.parse_args()
    
    files = args.load_files.split(',')

    if files[0]:
  
        #Read Zip_geo.csv file
        start = time.time()
        print 'Loading geolocation file: ' + files[0]
        zipgeo_data = read_file(filename=files[0])
        parse_zipgeo(data=zipgeo_data)
        end   = time.time()
        print 'Completed loading Geo location file in ' + str(end-start) + ' seconds'
         
    if files[1]:    
        # Read doctors.txt file
        start = time.time()
        print 'Loading provider file: ' + files[1]
        file_data = read_file(filename=files[1])
        parse_records(data=file_data)
        end   = time.time()
        print 'Completed loading doctors datafile in ' + str(end-start) + ' seconds'
        
                     
    # Count the number of doctors by zipcode and writes it to a csv file    
    count_distinct(True)
    print 'Completed... Counting doctors by zipcodes ..!!'
    # now process the records in the file
    print 'Job completed successfully ... in ' + str(time.time()-global_start) + ' seconds'
    