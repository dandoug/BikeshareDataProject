import csv
import pprint
import datetime
import time

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
            print("Using {} for month nmber".format(monthNum))
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
            result = ('none')

    print("We'll use '{}' as a time period filter.".format(result))
    return result

def popular_month(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular month for start time?
    '''
    # TODO: complete function


def popular_day(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    '''
    # TODO: complete function


def popular_hour(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular hour of day for start time?
    '''
    # TODO: complete function


def trip_duration(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the total trip duration and average trip duration?
    '''
    # TODO: complete function


def popular_stations(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular start station and most popular end station?
    '''
    # TODO: complete function


def popular_trip(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What is the most popular trip?
    '''
    # TODO: complete function


def users(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of each user type?
    '''
    # TODO: complete function


def gender(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the counts of gender?
    '''
    # TODO: complete function


def birth_years(city_file, time_period):
    '''TODO: fill out docstring with description, arguments, and return values.
    Question: What are the earliest, most recent, and most popular birth years?
    '''
    # TODO: complete function


def display_data():
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        none.
    Returns:
        TODO: fill out return type and description (see get_city for an example)
    '''
    display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. ')
    # TODO: handle raw input and complete function

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
            rowDict['dur'] = int(row['Trip Duration'])
            rowDict['start'] = row['Start Station']
            rowDict['end'] = row['End Station']
            if row['User Type'] == 'Customer':
                rowDict['utype'] = 'C'
            elif row['User Type'] == 'Subscriber':
                rowDict['utype'] = 'S'
            else:
                rowDict['utype'] = 'U'
            if row['Gender'] == 'Male':
                rowDict['gender'] = 'M'
            elif row['Gender'] == 'Female':
                rowDict['gender'] = 'F'
            else:
                rowDict['gender'] = 'U'
            if row['Birth Year']:
                rowDict['yob'] = int(float(row['Birth Year']))
            else:
                rowDict['yob'] = 0
            city_file.append(rowDict)
            cnt += 1
            # print a . every 10000 rows
            if cnt % 10000 == 0:
                #print('.', sep='', end='', flush=True)
                break

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
    print("That took %s seconds." % (time.time() - start_time)

    print('Calculating the first statistic...')
    start_time = time.time()

    # What is the most popular month for start time?
    if time_period[0] == 'none':
        # TODO: call popular_month function and print the results
        foo='bar'

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period[0] == 'none' or time_period[0] == 'month':
        # TODO: call popular_day function and print the results
        foo='bar'

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular hour of day for start time?
    # TODO: call popular_day function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the total trip duration and average trip duration?
    # TODO: call trip_duration function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    # TODO: call popular_stations function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What is the most popular trip?
    # TODO: call popular_trip function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of each user type?
    # TODO: call users function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the counts of gender?
    # TODO: call gender function and print the results

    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()

    # What are the earliest, most recent, and most popular birth years?
    # TODO: call birth_years function and print the results

    print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data()

    # Restart?
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
