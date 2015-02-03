import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

LATITUDE_INDEX = 128
LONGITUDE_INDEX = 129
ZIP_CODE_INDICES = [28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126]

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below

def get_avg_latlng():
    data = readCSV('permits_hydepark.csv')
    total_lat = 0
    total_lng = 0
    for i in range(len(data)):
        total_lat += float(data[i][LATITUDE_INDEX])
        total_lng += float(data[i][LONGITUDE_INDEX])
    avg_lat = float(total_lat) / len(data)
    avg_lng = float(total_lng) / len(data)
    print 'Average latitude: ' + str(avg_lat)
    print 'Average longitude: ' + str(avg_lng)

def zip_code_barchart():
    data = readCSV('permits_hydepark.csv')
    dict = {}
    for i in range(len(data)):
        for j in ZIP_CODE_INDICES:
            key = data[i][j]
            if key != '':
                if key in dict:
                    dict[key] += 1
                else:
                    dict[key] = 1
    zip_codes = sorted(dict.keys())
    zip_code_occurences = [dict[k] for k in zip_codes]
    N = len(zip_codes)
    ind = np.linspace(0, N, N)
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(ind, zip_code_occurences, width)
    ax.set_title("Hyde Park Contractor Zip Codes")
    ax.set_ylabel('Occurences')
    ax.set_ylabel('Zip Codes')
    ax.xaxis.set_ticks(ind)
    ax.set_xticklabels(zip_codes)
    plt.savefig('zip_code_barchart.jpg')

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == 'latlng':
            get_avg_latlng()
        elif arg == 'hist':
            zip_code_barchart()
        else:
            print 'Please enter an argument (latlng, hist)'

if __name__ == '__main__':
    main()