# Homework 4- problem 2: searching CPS
# Matt Mauer
# 11/5/2019

# An interactive data-query library for Chicago Public Schools
# public datasets.

import webbrowser
import csv
import math

class School():
    # Receive dictionary of data from CPS 
    # instance and assign attribute values
    # by calling dictionary values by key
    def __init__(self, data):
        self.id = data['School_ID']
        self.name = data['Short_Name']
        self.network = data['Network']
        self.address = data['Address']
        self.zip = data['Zip']
        self.phone = data['Phone']
        # Split string of grades into list
        self.grades = data['Grades'].split(', ')
        # location attribute assigned a Coordinate class object
        # that accepts two floats
        lat, longt = float(data['Lat']), float(data['Long'])
        self.location = Coordinate.fromdegrees(lat, longt)
    # create method to open webpage for specific instance of School
    # using string of url, id attribute,
    # and function imported from webbrowser
    def open_website(self):
        url = ("http://schoolinfo.cps.edu/schoolprofile/" +
        "SchoolDetails.aspx?SchoolId=" + self.id)
        webbrowser.open_new_tab(url)
    # To return a distance, call the distance method of the 
    # Coordinate class on a specified coord object
    # and the location attribute of our school
    def distance(self, coord):
        return coord.distance(self.location)
    # Return a clean string that contains all address 
    # information with necesary newline character
    def full_address(self):
        return self.address + '\nCHICAGO, IL ' + self.zip
    # Overwrite repr method to clearly display school name and id
    def __repr__(self):
        return self.name.strip()

class Coordinate():
    # Construct a latitude-longitude pair as radians
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
    # Create a Coordinate instance from a pair of degrees
    @classmethod
    def fromdegrees(cls, latitude, longitude):
        latitude *= math.pi / 180
        longitude *= math.pi / 180
        return cls(latitude, longitude)
    # Calculate the distance between to Coordinates using the 
    # Haversine formula
    def distance(self, coord):
        # For legibility, first redefine our variables
        x1, y1 = self.latitude, self.longitude
        x2, y2, earth2 = coord.latitude, coord.longitude, 3961*2
        # Break the Haversine formula into three parts
        d1 = math.sin((x2 - x1) / 2) ** 2
        d2 = math.cos(x2) * math.cos(x1) * math.sin((y2 - y1) / 2) ** 2
        dist = earth2 * math.asin(math.sqrt(d1 + d2))
        return dist
    # Convert the latitude and longitude attributes to degrees and return them as a tuple
    def as_degrees(self):
        dlat = self.latitude * 180 / math.pi
        dlong = self.longitude * 180 / math.pi
        return dlat, dlong
    # Call as_degrees to get the coordinates in the right format,
    # construct the formated string with these degrees, and open the url
    def show_map(self):
        x, y = self.as_degrees()
        url = "http://maps.google.com/maps?q=" + str(x) + "," + str(y)
        webbrowser.open_new_tab(url)
    # Display object as latitude-longitude pair in degrees
    def __repr__(self):
        x, y = self.as_degrees()
        return str(x) + ', ' + str(y)

class CPS():
    # Initialize a CPS by reading in a csv file, 
    # reading each line into a dictionary,
    # instantiate each dictionary/row as a School, 
    # and appending that school to 
    # a list of schools.
    def __init__(self, filename):
        self.schools = []
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.schools.append(School(row))
    # Return a filtered list of School instances that has a distance
    # less than specified radius by using School.distance method.
    def nearby_schools(self, coord, radius=1.0):
        step = filter(lambda x: x.distance(coord) < radius, self.schools)
        return list(step)
    # Returns a list of schools filtered by testing whether maping
    # input grades are in a School object's grade attribute
    # all returns true.
    def get_schools_by_grade(self, *grades):
        f = lambda s: all(map(lambda g: g in s.grades, grades))
        return list(filter(f, self.schools))
    # Return a filtered list of School instances that have a network
    # attribute matching the input network. Not case sensitive.
    def get_schools_by_network(self, network):
        f = lambda x: x.network.lower() == network.lower()
        return list(filter(f, self.schools))
