from trips import Trip, TripData, Coordinate
d = TripData('example_data_training.csv')
trips = []
for datum in d.data:
    trips.append(Trip(datum))

md = Coordinate.haversine

for i in range(5):
    print("%0.4fkm" % md(trips[i].pickup_coords, trips[i].dropoff_coords))