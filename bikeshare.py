import csv
import pprint
import datetime
import time
import numpy as np

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

## Constants
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    result = None
    while not result:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').lower().strip()
        if city.startswith('c'):
            result = chicago
        elif city.startswith('n'):
            result = new_york_city
        elif city.startswith('w'):
            result = washington

    print("Great!  We'll use the {} file.".format(result))
    return result

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (int) specified month as 1 (Jan), 2 (Feb), etc..
    '''
    result = None
    while not result:
        try:
            month = input('\nWhich month? January, February, March, April, May, or June?\n').lower().strip()
            newDate = datetime.datetime.strptime(month,"%B")
            monthNum = newDate.month
            if (monthNum>6):
                continue
            print("Using {} for month number".format(monthNum))
            return monthNum
        except ValueError:
            correctDate = False

def get_day(month):
    '''Asks the user for a day and returns the specified day.

    Args:
        (int) month as int, 1=Jan, etc..  data is for 2017, so not leap year
    Returns:
        (int) validated day of month as int
    '''
    year=2017
    correctDate = None
    while not correctDate:
        try:
            day = int(float(input('\nWhich day? Please type your response as an integer.\n').lower().strip()))
            newDate = datetime.datetime(year, month, day)
            return day
        except ValueError:
            correctDate = False

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.

    Args:
        none.
    Returns:
        a tuple that is like one of these examples:
         ('none') - for no filtering
         ('month',1) - for filtering for data in January (Feb=2, Mar=3, etc..)
         ('day',1,31) - for filtering for data on January 31
    '''
    result = None
    while not result:
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n').lower().strip()
        if time_period.startswith('m'):
            month = get_month()
            result = ('month',month)
        elif time_period.startswith('d'):
            month = get_month()
            day = get_day(month)
            result = ('day',month,day)
        elif time_period.startswith('n'):
            result = ('none',)

    print("We'll use '{}' as a time period filter.".format(result))
    return result

def popular_month(city_file, time_period):
    '''
      Calculate the most popular month based on the filtered input and print it out
    Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
        time_period: the filter that was used to restrict the data
    Return:
        none
    '''
    # 13 elements, 0 not used, 1-based indexing for totaling data by month
    monthsAccum = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for row in city_file:
        monthsAccum[row['startTime'].month] += 1
    maxIx = 1 # let Jan be the most popular to start
    for i in range(1,13):
        if monthsAccum[i] > monthsAccum[maxIx]:
            maxIx = i
    # just want some day with the maxIx month so strftime will print out the formated month name
    monDate = datetime.datetime(2017,maxIx,1)
    print("The most popular month for filter {} is {} with {} occurances".format(time_period,monDate.strftime('%B'),monthsAccum[maxIx]))

def popular_day(city_file, time_period):
    '''
     Calculate the most popular day of week (Monday, Tuesday, etc.) for start time and print it out
    Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
        time_period: the filter that was used to restrict the data
    Return:
        none
    '''
    # 0-based indexing for totaling data by day of week Monday=0, Sunday=6
    daysAccum = [0,0,0,0,0,0,0]
    for row in city_file:
        daysAccum[row['startTime'].weekday()] += 1
    maxIx = 0 # let Monday be the most popular to start
    for i in range(0,7):
        if daysAccum[i] > daysAccum[maxIx]:
            maxIx = i
    # May 1, 2017 was a Monday, so adding maxIx will give us a day with the right name
    # can use strftime() to print out the full day name from index
    dayDate = datetime.datetime(2017,5,1+maxIx)
    print("The most popular day of the week for filter {} is {} with {} occurances".format(time_period,dayDate.strftime('%A'),daysAccum[maxIx]))


def popular_hour(city_file, time_period):
    '''
     Calculate the most popular hour of day for start time and print it out
    Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
        time_period: the filter that was used to restrict the data
    Return:
        none
    '''
    # 0-based indexing for totaling data by hour of day (0-23)
    hoursAccum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for row in city_file:
        hoursAccum[row['startTime'].hour] += 1
    maxIx = 0 # let 00 be the most popular hour to start
    for i in range(0,24):
        if hoursAccum[i] > hoursAccum[maxIx]:
            maxIx = i
    print("The most popular hour of the day for filter {} is {} with {} occurances".format(time_period,maxIx,hoursAccum[maxIx]))


def trip_duration(city_file, time_period):
    '''
    Calculate the total trip duration and average trip duration and print them out
    Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
        time_period: the filter that was used to restrict the data
    Return:
        none
    '''
    totalSeconds = 0;
    numTrips = 0;
    for row in city_file:
        totalSeconds += row['dur']
        numTrips +=1
    print("The total trip duration is {} seconds and the average trip duration is {} seconds for filter {} computed over {} trips"
                        .format(totalSeconds,(totalSeconds/numTrips),time_period,numTrips))


def build_dest_array(city_file, stnNames):
    '''
    Build up a list of station names from the city_file and a two dimensional array that counts the
    number of trips between stations (start=row, end=column)

    Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
        stnNames: list of names of stations, initially empty, will be filled in
    Returns:
        a two dimensional array that counts the number of trips between stations
    '''
    trips = None  # special case the start
    for row in city_file:
        s = row['start']
        e = row['end']
        newNames = 0
        if s not in stnNames:
            stnNames.append(s)
            newNames += 1
        if e not in stnNames:
            stnNames.append(e)
            newNames += 1
        # Add anything?
        if newNames > 0:
            # special case first one
            if type(trips) == type(None):
                trips = np.zeros((newNames, newNames))
            else:
                newSize = len(stnNames)
                oldSize = newSize - newNames
                # expand trips by adding new row and column
                trips = np.vstack((trips, np.zeros((newNames, oldSize)) ))
                trips = np.hstack((trips, np.zeros((newSize, newNames)) ))
        # now find indexes.  start is row, end is column
        si = stnNames.index(s)
        ei = stnNames.index(e)
        # record another trip between the two endpoints
        trips[si, ei] += 1
    return trips


def popular_stations(stnNames, trips):
    '''
    Find the most popular start station and most popular end station and print them out.

    Args:
        stnNames: list of station names, provides indexes into trips matrix
        trips: two dimensional matrix (start=rows, end=columns) of trip frequencies
    Returns:
        none
    '''
    starts = np.sum(trips, axis=1)  # sum across rows
    ends   = np.sum(trips, axis=0)  # sum down columns

    psi = np.argmax(starts)
    popularStart = stnNames[ psi ]
    pei = np.argmax(ends)
    popularEnd   = stnNames[ pei ]

    print("Using the supplied filter,")
    print("\tThe most popular start station is '{}' with {} trips originating there".format(popularStart,int(starts[psi])))
    print("\tThe most popular end station is '{}' with {} trips ending there".format(popularEnd,int(ends[pei])))


def popular_trip(stnNames, trips):
    '''
    Find the the most popular trip and print it out.

    Args:
        stnNames: list of station names, provides indexes into trips matrix
        trips: two dimensional matrix (start=rows, end=columns) of trip frequencies
    Returns:
        none
    '''
    maxTrip = np.argmax(trips) # raveled index
    maxStartIx = maxTrip // len(stnNames) # compute row
    maxEndIx = maxTrip % len(stnNames) # compute column
    maxTripOccurs = int(trips[maxStartIx, maxEndIx])
    print("Using the supplied filter,")
    print("\tThe most popular trip is from '{}' to '{}' which occurred {} times"
          .format(stnNames[maxStartIx], stnNames[maxEndIx], maxTripOccurs))


def users(city_file, time_period):
    '''
    Calculate the counts of each user type and print them out
        Args:
            city_file: a list of dictionaries as loaded by load_city_file(), below
            time_period: the filter that was used to restrict the data
        Return:
            none
    '''
    userTypeAccum = {'C':0, 'S':0, 'U':0}
    for row in city_file:
        utype = row['utype']
        if utype in userTypeAccum:
            userTypeAccum[utype] += 1
    print("Using the supplied filter, the trips per user type were as follows:")
    print("\tSubscriber: {}, Customer: {}, Unkonwn: {}".format(userTypeAccum['S'],userTypeAccum['C'],userTypeAccum['U']))


def gender(city_file, time_period):
    '''
    Calculate the counts of trips by each gender and print them out
        Args:
            city_file: a list of dictionaries as loaded by load_city_file(), below
            time_period: the filter that was used to restrict the data
        Return:
            none
    '''
    genderTypeAccum = {'M':0, 'F':0, 'U':0}
    for row in city_file:
        gtype = row['gender']
        if gtype in genderTypeAccum:
            genderTypeAccum[gtype] += 1
    print("Using the supplied filter, the trips per gender were as follows:")
    print("\tMale: {}, Female: {}, Unkonwn: {}".format(genderTypeAccum['M'],genderTypeAccum['F'],genderTypeAccum['U']))


def birth_years(city_file, time_period):
    '''
    Calculate the earliest, most recent, and most popular birth years and print them out
        Args:
            city_file: a list of dictionaries as loaded by load_city_file(), below
            time_period: the filter that was used to restrict the data
        Return:
            none
    '''
    yobAccum = {}
    maxBirthYear = 0
    minBirthYear = 999999
    for row in city_file:
        yob = row['yob']
        if yob == 0:
            continue # skip if not specified
        if yob not in yobAccum:
            yobAccum[yob] = 1
        else:
            yobAccum[yob] += 1
        if yob < minBirthYear:
            minBirthYear = yob
        if yob > maxBirthYear:
            maxBirthYear = yob
    mostPopularYear = 0
    for yob in yobAccum:
        if mostPopularYear == 0 or yobAccum[yob] > yobAccum[mostPopularYear]:
            mostPopularYear = yob
    if mostPopularYear == 0:
        print("Using the supplied filter, there were no birth year data available")
    else:
        print("Using the supplied filter, the birth year stats were as follows:")
        print("\tEarliest: {}, most recent: {} and most popular year of birth: {} with {} occurrences"
              .format(minBirthYear,maxBirthYear,mostPopularYear,yobAccum[mostPopularYear]))


def display_data(city_file):
    '''
    Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

     Args:
        city_file: a list of dictionaries as loaded by load_city_file(), below
    Return:
        none
    '''
    if not promptToContinue('Would you like to view individual trip data?'):
        return

    pp = pprint.PrettyPrinter(indent=4)
    print("here are some lines of data")
    cnt = 0
    for row in city_file:
        pp.pprint(row)
        cnt += 1
        if cnt % 5 == 0:
            if not promptToContinue('Would you like to view five more rows?'):
                return


def promptToContinue(prompt):
    '''
    Present a prompt and collect a yes or now answer

    Args:
        prompt: prompt string to display
    Returns:
        True or False
    '''
    answer = None
    while not answer:
        display = input(prompt+
                        '\nType \'yes\' or \'no\'. ').lower().strip()
        if display.startswith('y'):
            answer = 'yes'
        elif display.startswith('n'):
            answer = 'no'
    return answer == 'yes'


def load_city_file(city, time_period):
    '''Load data from the specified file into an in-memory structure for analysis

    Args:
        city: (str) name of a .csv file to load
        time_period: tuple, as returned by get_time_period() above
    Returns:
        a list of dictionaries, each one representing a row from the file
        the time_period filter is applied to the data read
    '''
    city_file = []
    cnt = 0
    foundMatch = False
    with open(city) as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            startTime = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT)
            # Data is sorted.  So after we find the first match, we can stop
            # reading if we ever find a non-match
            if time_period[0]=='month' and startTime.month != time_period[1]:
                if foundMatch:
                    # means we're done
                    break
                else:
                    # keep looking
                    continue
            if time_period[0]=='day' and (startTime.month != time_period[1] or startTime.day != time_period[2]):
                if foundMatch:
                    # means we're done
                    break
                else:
                    # keep looking
                    continue
            foundMatch = True  #from this point on, we'll read until we find a non-match or read all data
            rowDict = {}
            rowDict['startTime'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT)
            rowDict['endTime'] = datetime.datetime.strptime(row['End Time'], DATETIME_FORMAT)
            rowDict['dur'] = int(float(row['Trip Duration']))
            rowDict['start'] = row['Start Station']
            rowDict['end'] = row['End Station']
            if row['User Type'] == 'Customer':
                rowDict['utype'] = 'C'
            elif row['User Type'] == 'Subscriber':
                rowDict['utype'] = 'S'
            else:
                rowDict['utype'] = 'U'
            if 'Gender' not in row:
                rowDict['gender'] = 'U'
            else:
                if row['Gender'] == 'Male':
                    rowDict['gender'] = 'M'
                elif row['Gender'] == 'Female':
                    rowDict['gender'] = 'F'
                else:
                    rowDict['gender'] = 'U'
            if 'Birth Year' in row:
                try:
                    rowDict['yob'] = int(float(row['Birth Year']))
                except ValueError:
                    rowDict['yob'] = 0
            else:
                rowDict['yob'] = 0
            city_file.append(rowDict)
            cnt += 1
            # print a . every 10000 rows
            if cnt % 10000 == 0:
                print('.', sep='', end='', flush=True)
                #break # uncomment break to exit after first 10000 rows

    return city_file

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()

    # Filter by time period (month, day, none)
    # value is a tuple like ('none') or ('month',1) or ('day',1,31)
    time_period = get_time_period()

    # load the data file into list of dictionaries
    start_time = time.time()
    city_file = load_city_file(city, time_period)
    print("\nLoaded {} records from {} using filter".format(len(city_file), city, time_period))
    print("That took %s seconds." % (time.time() - start_time))

    if len(city_file) == 0:
        print("No statistics to compute becuase the filter selected no trips.")
    else:
        firstOrNext = 'first'


        # What is the most popular month for start time?
        if time_period[0] == 'none':
            print('\nCalculating the {} statistic...'.format(firstOrNext))
            start_time = time.time()

            popular_month(city_file, time_period)

            print("That took %s seconds." % (time.time() - start_time))
            firstOrNext = 'next'


        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        if time_period[0] == 'none' or time_period[0] == 'month':
            print("\nCalculating the {} statistic...".format(firstOrNext))
            start_time = time.time()

            popular_day(city_file, time_period)

            print("That took %s seconds." % (time.time() - start_time))
            firstOrNext = 'next'



        # What is the most popular hour of day for start time?
        print("\nCalculating the {} statistic...".format(firstOrNext))
        start_time = time.time()

        popular_hour(city_file, time_period)

        print("That took %s seconds." % (time.time() - start_time))
        firstOrNext = 'next'


        # What is the total trip duration and average trip duration?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        trip_duration(city_file, time_period)

        print("That took %s seconds." % (time.time() - start_time))

        # Build up a list of station names and a two dimensional array that counts the
        # number of trips between stations
        print("\nComputing trip matrix...")
        start_time = time.time()
        stnNames = []
        trips = build_dest_array(city_file, stnNames)
        print("That took %s seconds." % (time.time() - start_time))



        # What is the most popular start station and most popular end station?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        popular_stations(stnNames, trips)

        print("That took %s seconds." % (time.time() - start_time))



        # What is the most popular trip?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        popular_trip(stnNames, trips)

        print("That took %s seconds." % (time.time() - start_time))



        # What are the counts of each user type?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        users(city_file, time_period)

        print("That took %s seconds." % (time.time() - start_time))




        # What are the counts of gender?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        gender(city_file, time_period)

        print("That took %s seconds." % (time.time() - start_time))



        # What are the earliest, most recent, and most popular birth years?
        print("\nCalculating the next statistic...")
        start_time = time.time()

        birth_years(city_file, time_period)

        print("That took %s seconds." % (time.time() - start_time))


        # Display five lines of data at a time if user specifies that they would like to
        display_data(city_file)


    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()

if __name__ == "__main__":
	statistics()
