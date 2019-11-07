import csv
import fileinput
import os

with open('VESSEL_9002_BATCH_4225.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)
    print(f'Processed {line_count} lines.')

# List all files in a dataFolder using os.listdir
cur_path = os.getcwd()
basepath = cur_path + '/dataFolder/'
files = []
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        files.append(entry)

for fileName in files:
    lines = []
    with open(basepath + fileName, 'r') as file:
        lines = file.readlines()
    newFile = open(basepath+'edited/'+fileName, 'w')

    with open(basepath+fileName, 'r') as file:
        for line in file:
            newFile.write(line.replace('\t', ''))
    newFile.close()
