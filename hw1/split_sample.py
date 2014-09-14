#!/usr/bin/env python

import csv
from trips import TripData

example = TripData('example_data.csv')

outfile_train = open('example_data_training.csv', 'w')
outfile_test = open('example_data_test.csv', 'w')

writer_training = csv.DictWriter(outfile_train, fieldnames=example.fieldnames)
writer_test = csv.DictWriter(outfile_test, fieldnames=example.fieldnames)

writer_training.writeheader()
writer_test.writeheader()

i = 2
for datum in example.:
    if i % 4 == 0:
        writer_training.writerow(datum)
    else:
        writer_test.writerow(datum)
    i += 1

outfile_train.close()
outfile_test.close()