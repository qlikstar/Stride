from sqlalchemy.sql import select
import geopy.distance

# import our Provider model class and database session elements
from model import Session
from model import Provider, Zip_geo


# Function to find the patient location and the doctors around
def find_distance(patient_location, miles):
    
        session = Session()
        p = select([Provider.latitude, Provider.longitude])
        result = session.execute(p)
        doc_data = result.fetchall()

        doc_count = 0

        # Checks for each doctor's location in the database
        for coordinates in doc_data:
            doc_location =  geopy.Point(coordinates.latitude,coordinates.longitude )
            dist = geopy.distance.distance(patient_location, doc_location).miles
            
            if dist < float(miles):
                doc_count = doc_count + 1
        
        if doc_count == 0:
            print  'No doctors found near you in ' + str(miles)+ ' miles'
        else:
            print str(doc_count) + ' doctors found near you in ' + str(miles)+ ' miles'




def get_coordinates(zipcode , miles):
        session = Session()
        # To fetch the Geographical coordinates from Zip_geotable 
        z = select([Zip_geo.latitude, Zip_geo.longitude]).where(Zip_geo.zipcode == zipcode)
        result = session.execute(z)
        #print result
        geo_data = result.fetchone()
        
        #If zipcode exists in database
        if geo_data:
            latitude = geo_data.latitude
            longitude= geo_data.longitude
            patient_loc = geopy.Point(latitude,longitude )
            #print latitude,longitude
            find_distance(patient_loc, miles)
        else:
            print 'Zipcode not found. Please enter a valid zipcode'
        session.close()
  
 
# Main #    
if __name__ == '__main__':
    zipcode = raw_input('Enter your zipcode : ')
    miles   = raw_input('Enter miles you want to search :')
    get_coordinates(zipcode , miles)