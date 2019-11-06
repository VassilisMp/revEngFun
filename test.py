import csv

with open('VESSEL_9002_BATCH_4225.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)
    print(f'Processed {line_count} lines.')

import fileinput

with fileinput.FileInput('VESSEL_9002_BATCH_4225.csv', inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace('\t', ''), end='')
