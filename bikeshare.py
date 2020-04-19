import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    global city, month, day
    # Get user input for city (chicago, new york city, washington)
    while True:
        city_input = input('Please enter c for Chicago, n for New York City, or w for Washington: ')
        if str(city_input.lower()) not in ('c', 'n', 'w'):
            print("Not an appropriate choice.")
        else:
            if city_input.lower() == 'c':
                city = 'chicago'
            elif city_input.lower() == 'n':
                city = 'new york city'
            elif city_input.lower() == 'w':
                city = 'washington'
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        month_input = input('Please enter all for no month filter,\n jan for January,\n feb for February,\n mar for March,\n apr for April, \n may for May,\n jun for June: ')
        if str(month_input.lower()) not in ('all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun'):
            print("Not an appropriate choice.")
        else:
            if month_input.lower() == 'all':
                month = 'all'
            elif month_input.lower() == 'jan':
                month = 'january'
            elif month_input.lower() == 'feb':
                month = 'february'
            elif month_input.lower() == 'mar':
                month = 'march'
            elif month_input.lower() == 'apr':
                month = 'april'
            elif month_input.lower() == 'may':
                month = 'may'
            elif month_input.lower() == 'jun':
                month = 'june'
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input('Please enter all for no day of week filter,\n mon for Monday,\n tue for Tuesday,\n wed for Wednesday,\n thu for Thursday, \n fri for Friday,\n sat for Saturday,\n sun for Sunday: ')
        if str(day_input.lower()) not in ('all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'):
            print("Not an appropriate choice.")
        else:
            if day_input.lower() == 'all':
                day = 'all'
            elif day_input.lower() == 'mon':
                day = 'monday'
            elif day_input.lower() == 'tue':
                day = 'tuesday'
            elif day_input.lower() == 'wed':
                day = 'wednesday'
            elif day_input.lower() == 'thu':
                day = 'thursday'
            elif day_input.lower() == 'fri':
                day = 'friday'
            elif day_input.lower() == 'sat':
                day = 'saturday'
            elif day_input.lower() == 'sun':
                day = 'sunday'
            break
    print('\nYour filters are:')
    print('City:', city.title(), ', Month:', month.capitalize(), ', Day of Week:', day.capitalize())
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # use the index of the months list to get the corresponding int
    if month != 'all':
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    # ask if user wants to see the first rows of data frame
    user_query = input('Would you like to see the first few rows of the data frame? Then type yes: ')
    if user_query == 'yes':
        print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month, if no filter set
    if month == 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        popular_month = df['month'].mode()[0]
        print('Most Common Month:', months[popular_month - 1].capitalize())
    else:
        print('The data is already filtered by month:', month.capitalize())

    # Display the most common day of week, if no filter set
    if day == 'all':
        popular_dow = df['day_of_week'].mode()[0]
        print('Most Common Day of Week:', popular_dow)
    else:
        print('The data is already filtered by day of week:', day.capitalize())

    # Display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # Display most frequent combination of start station and end station trip
    df['start_end_combination'] = df['Start Station'] + ' -- ' + df['End Station']
    popular_combination = df['start_end_combination'].mode()[0]
    print('Most Popular Trip:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Auxiliary fct: Conversion of seconds into Days:Hours:Minutes:Seconds
def convert_time(sec):
    sec_in_min = 60
    sec_in_hr = 60 * sec_in_min
    sec_in_day = 24 * sec_in_hr

    days = sec // sec_in_day
    hours = (sec - days*sec_in_day) // sec_in_hr
    minutes = (sec - days*sec_in_day - hours*sec_in_hr) // sec_in_min
    seconds = sec - (days*sec_in_day + hours*sec_in_hr + minutes*sec_in_min)
    converted_time = [int(days), int(hours), int(minutes), seconds]

    return converted_time


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    converted_total_time = convert_time(total_travel_time)
    print('Total Travel Time:', total_travel_time, 'seconds OR {} days, {} hours, {} minutes, and {} seconds'.format(*converted_total_time))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    converted_mean_time = convert_time(mean_travel_time)
    print('Mean Travel Time:', mean_travel_time, 'seconds OR {} days, {} hours, {} minutes, and {} seconds'.format(*converted_mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types are:')
    user_count = df['User Type'].value_counts()
    print(user_count)

    # Display counts of gender
    if city in ('chicago', 'new york city'):
        print('\nGender distribution is:')
        gender_count = df['Gender'].value_counts()
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        birth_earliest = df['Birth Year'].min()
        print('\nEarliest year of birth: {}'.format(int(birth_earliest)))
        birth_latest = df['Birth Year'].max()
        print('Most recent year of birth: {}'.format(int(birth_latest)))
        popular_birth_year = df['Birth Year'].mode()[0]
        print('Most common year of birth:', int(popular_birth_year))
    else:
        print('\nNo data about gender and birth year available!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
