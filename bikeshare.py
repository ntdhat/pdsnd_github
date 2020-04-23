import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS_OF_WEEK = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def display_raw_data(df, rows=5):
    """
    Ask user for displaying a few rows of raw data from city data.
    
    Args:
        (DataFrame) df - city raw data
        (int) rows - (optional) number of rows to be display each time
    """
    print()
    
    should_display = ''
    while should_display not in ['yes', 'no']:
        prompt = 'Would you like to see some raw data? (Yes/No) - '
        should_display = input(prompt).lower()
    
    current = 0
    while (should_display == 'yes') and (current < len(df)):
        print(df[current : current+rows])
        current += rows
        
        print()
        
        should_display = ''
        while should_display not in ['yes', 'no']:
            prompt = 'Would you like to see more raw data? (Yes/No) - '
            should_display = input(prompt).lower()


def get_city():
    """
    Get user input for city (Chicago, New York city, Washington).
    
    Return:
        (str) city - name of the city
    """
    
    prompt = '\nWhich data you want to see, Chicago, New York city, or Washington? - '
    city = input(prompt).lower()
    while city not in CITY_DATA:
        prompt = 'Invalid city\'s name! Enter Chicago, New York city, or Washington. - '
        city = input(prompt).lower()
    
    return city

def get_filters():
    """
    Asks user to specify month, and day to analyze.

    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    time_filter = get_time_filter()
        
    month = day = 'all'
    if time_filter == 'month' or time_filter == 'both':
        month = get_month_filter()
    if time_filter == 'day' or time_filter == 'both':
        day = get_day_filter()

    print('-'*40)
    return month, day

        
def get_time_filter():
    """
    Get user input for filter method (by month, day of week, or none)
    
    Return:
        (str) time_filter - method user input ('month', 'day', 'both', or 'none')
    """
    
    prompt = "\nWould you like to filter the data by 'month', 'day', 'both' or 'none'? - "
    time_filter = input(prompt).lower()
    while time_filter not in ['month', 'day', 'both', 'none']:
        prompt = "Invalid input! Make sure you enter 'month', 'day', 'both' or 'none'. - "
        time_filter = input(prompt).lower()
    
    return time_filter

    
def get_month_filter():
    """
    Get user input for month (all, january, february, ... , june)
    
    Return:
        (str) month - name of the month (in lower case)
    """
    
    prompt = '\nWhich month: January, February, March, April, May, or June? - '
    month = input(prompt).lower()
    while month not in MONTHS:
        prompt = 'Invalid input! Please enter January, February, March, April, May, or June. - '
        month = input(prompt).lower()
    
    return month

    
def get_day_filter():
    """
    Get user input for day of week (all, monday, tuesday, ... sunday)
    
    Return:
        (str) day - name of the day of week (in lower case)
    """
    
    prompt = '\nEnter the day of week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. - '
    day = input(prompt).lower()
    while day not in DAYS_OF_WEEK:
        prompt = 'Invalid input! Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. - '
        day = input(prompt).lower()
    
    return day


def load_data(city):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
    Returns:
        (DataFrame) df - containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = None
    try:
        df = pd.read_csv(f'{CITY_DATA[city]}')
    except:
        # handle loading file errors
        print(f"File not found. Could't load '{CITY_DATA[city]}'")
        print('-'*40)
    
    return df


def prepare_data(df, month, day):
    """
    Prepare data for analyzing

    Args:
        (DataFrame) df - Original city's data loaded from a file.
        (str) month - Name of the month to filter by, or "all" to apply no month filter.
        (str) day - Name of the day of week to filter by, or "all" to apply no day filter.

    Returns:
        (DataFrame) df - City data filtered by month and day.
    """
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_index = MONTHS.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month_index]
        

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (DataFrame) df - city data
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    occurrences = (df['month'] == month).sum()
    print(f"Common month: {month} ({occurrences} occurrences)")

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    occurrences = (df['day_of_week'] == day).sum()
    print(f"Common day of week: {day} ({occurrences} occurrences)")

    # display the most common start hour
    hour = df['start_hour'].mode()[0]
    occurrences = (df['start_hour'] == hour).sum()
    print(f"Common start hour: {hour} ({occurrences} occurrences)")

    print("\nThis calculating took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        (DataFrame) df - city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start = df['Start Station'].mode()[0]
    occurrences = (df['Start Station'] == start).sum()
    print(f"Most common start station: {start} ({occurrences} occurrences)")

    # display most commonly used end station
    end = df['End Station'].mode()[0]
    occurrences = (df['End Station'] == end).sum()
    print(f"Most common end station: {end} ({occurrences} occurrences)")

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' --> ' + df['End Station']
    trip = df['trip'].mode()[0]
    occurrences = (df['trip'] == trip).sum()
    print(f"Most frequent trip: {trip} ({occurrences} occurrences)")

    print("\nThis calculating took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (DataFrame) df - city data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ' + str(df['Trip Duration'].sum()) + ' (seconds)')

    # display mean travel time
    print('Mean travel time: ', str(df['Trip Duration'].mean()) + ' (seconds)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (DataFrame) df - city data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user type:')
    print(df['User Type'].value_counts())

    # Display counts of gender
    print('\nCounts of gender:')
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('There\'s no gender data.')
    print()

    # Display earliest, most recent, and most common year of birth
    print('\nBirth year stats:')
    if 'Birth Year' in df.columns:
        print('Earlies: ', int(df['Birth Year'].min()))
        print('Most recent: ', int(df['Birth Year'].max()))
        print('Most common: ', int(df['Birth Year'].mode()[0]))
    else:
        print('There\'s no birth year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def should_start_over():
    """
    Get user input whether we should start the program over.
    
    Return:
        (boolean) - True for should starting over and False for should not
    """
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    return restart.lower() == 'yes'

def main():
    while True:
        print('-'*40)
        print('\nHELLO! LET\'S EXPLORE SOME US BIKESHARE DATA!\n')
        
        city = get_city()
        df = load_data(city)
        if df is None:
            if should_start_over() == False:
                break
            continue
        
        display_raw_data(df)
            
        month, day = get_filters()
    
        df = prepare_data(df, month, day)
    
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
    
        if should_start_over() == False:
            break


if __name__ == "__main__":
	main()
