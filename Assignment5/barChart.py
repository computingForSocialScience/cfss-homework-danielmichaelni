import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    # open necessary files
    f_artists = open('artists.csv')
    f_albums = open('albums.csv')

    # create readers for each file
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums)

    # read header line from csv files
    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    artist_names = []
    
    decades = range(1900,2020, 10)
    decade_dict = {}
    for decade in decades:
        decade_dict[decade] = 0
    
    for artist_row in artists_rows:
        # skip the row if it is blank
        if not artist_row:
            continue
        
        # extract info from row and add artist name to artist_names list
        artist_id,name,followers, popularity = artist_row
        artist_names.append(name)

    for album_row  in albums_rows:
        # skip the row if it is blank
        if not album_row:
            continue

        # extract info from row and increment decades_dict accordingly
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades:
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break

    x_values = decades
    y_values = [decade_dict[d] for d in decades]
    return x_values, y_values, artist_names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()
    
    # plot a bar graph of number of albums per decade
    fig , ax = plt.subplots(1,1)
    ax.bar(x_vals, y_vals, width=10)

    # set labels
    ax.set_xlabel('decades')
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ', '.join(artist_names))
    plt.show()


    
