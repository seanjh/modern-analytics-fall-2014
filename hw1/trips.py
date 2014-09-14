#!/usr/bin/env python

import csv
from math import asin, sqrt, sin, cos, pi
from numpy import array
from datetime import datetime

class TripData(object):
    def __init__(self, filename):
        with open(filename, 'r') as infile:
            reader = csv.DictReader(infile)

            line = next(reader)
            self.fieldnames = reader.fieldnames
            
            self.data = [line]

            for row in reader:
                self.data.append(row)

class Coordinate(object):
    EARTH_RADIUS_KM = 6356.752

    # http://en.wikipedia.org/wiki/Haversine_formula
    @classmethod
    def haversine(cls, coord1, coord2):
        return 2.0 * Coordinate.EARTH_RADIUS_KM * asin(
                sqrt(
                        sin(
                            (coord2.latitude_radians - coord1.latitude_radians) / 2.0
                        ) ** 2
                        + (
                            cos(coord1.latitude_radians)
                            * cos(coord2.latitude_radians)
                            * sin(
                                (coord2.longitude_radians - coord1.longitude_radians) / 2.0
                            ) ** 2)
                    )
            )

    def __init__(self, lat_deg, lon_deg):
        self.latitude = lat_deg
        self.longitude = lon_deg
        self._latitude_radians = None
        self._longitude_radians = None

    @property
    def latitude_radians(self):
        if not self._latitude_radians:
            self._latitude_radians = self.latitude * pi / 180
        return self._latitude_radians
    @latitude_radians.setter
    def latitude_radians(self, value):
        self._latitude_radians = float(value)
        self.latitude = self._latitude_radians * 180.0 / pi

    @property
    def longitude_radians(self):
        if not self._longitude_radians:
            self._longitude_radians = self.longitude * pi / 180
        return self._longitude_radians
    @longitude_radians.setter
    def longitude_radians(self, value):
        self._longitude_radians = float(value)
        self.longitude = self._latitude_radians * 180.0 / pi
    

class Trip(object):

    def __init__(self, trip_dict):
        self.medallion = trip_dict.get('medallion')
        self.hack_license = trip_dict.get('hack_license')
        self.vendor_id = trip_dict.get('vendor_id')
        self.pickup_datetime = datetime.strptime(
                trip_dict.get('pickup_datetime'),
                "%Y-%m-%d %H:%M:%S"
            )
        self.dropoff_datetime = datetime.strptime(
                trip_dict.get('dropoff_datetime'),
                "%Y-%m-%d %H:%M:%S"
            )
        self.trip_time_in_secs = int(trip_dict.get('trip_time_in_secs'))
        self.trip_distance = float(trip_dict.get('trip_distance'))
        self.pickup_coords = Coordinate(
            float(trip_dict.get('pickup_latitude')),
            float(trip_dict.get('pickup_longitude'))
            )
        self.dropoff_coords = Coordinate(
            float(trip_dict.get('dropoff_latitude')),
            float(trip_dict.get('dropoff_longitude'))
            )
        '''self.pickup_longitude = float(trip_dict.get('pickup_longitude'))
        self.pickup_latitude = float(trip_dict.get('pickup_latitude'))
        self.dropoff_longitude  = float(trip_dict.get('dropoff_longitude'))
        self.dropoff_latitude = float(trip_dict.get('dropoff_latitude'))
        self.pickup_vector = array([
                float(trip_dict.get('pickup_longitude')),
                float(trip_dict.get('pickup_latitude'))
            ])
        self.dropoff_vector = array([
                float(trip_dict.get('dropoff_longitude')),
                float(trip_dict.get('dropoff_latitude'))
            ])'''


#http://www.geomidpoint.com/example.html
#http://www.geomidpoint.com/calculation.html
def _cartesian_coords(lat_degrees, lon_degrees):
    lat_radians = lat_degrees * pi / 180
    lon_radians = lon_degrees * pi / 180

    x = cos(lat_radians) * cos(lon_radians)
    y = cos(lat_radians) * sin(lon_radians)
    z = sin(lat_radians)
    return array([x, y, z])

def _combined_cartesian(*args):
    assert len(args) > 1
    x = sum([coords[0] for coords in args]) / len(args)
    y = sum([coords[1] for coords in args]) / len(args)
    z = sum([coords[2] for coords in args]) / len(args)
    return array([x, y, z])

def geographic_midpoint(*args):
    assert len(args) > 1
    mid_cc = _combined_cartesian([_cartesian_coords(a) for a in args])
    
    lon = atan(mid_cc[1], mid_cc[0]) ** 2
    hyp = sqrt(mid_cc[0] ** 2 + mid_cc[1] ** 2)
    lat = atan(mid_cc[2], hyp) ** 2

    return array([
            lat * 180 / pi,
            lon * 180 / pi
        ]
        )

def spherical_law_costines():
    pass