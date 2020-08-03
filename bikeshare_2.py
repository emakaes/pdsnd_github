import time
import pandas as pd
import numpy as np
import calendar

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please select a city: Chicago, New York City or Washington: ").lower()
    while city not in CITY_DATA:
        city = input("Input not valid, please select a city: chicago, new york city or washington: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june"]
    month = input("Please select a month from this list: january, february, march, april, may, june. Select all, for all months: ").lower()
    while month not in months:
        month = input("input not valid: please select a month from this list: january, february, march, april, may, june. Insert all, for all months: ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Please select the day. Select all, for all days: ').lower()
    while day not in days:
        day = input('input non valid: please select a day. Insert all, for all days: ').lower()

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('Most frequent month of travel: ' + calendar.month_name[df['month'].value_counts().idxmax()]) #from stackoverflow

    # TO DO: display the most common day of week
    print('Most frequent day of the week of travel: ' + str(df['day_of_week'].value_counts().idxmax()))

    # TO DO: display the most common start hour
    print('Most frequent hour of travel: ' + str(df['Start Time'].dt.hour.value_counts().idxmax()) + 'h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most common start station: ' + df['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('Most common end station: ' + df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    df['Stations'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most common combination of start and end station: ' + df['Stations'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    print('Total travel time: ' + str((df['End Time'] - df['Start Time']).sum()))

    # TO DO: display mean travel time
    print('Mean travel time: ' + str((df['End Time'] - df['Start Time']).mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts of ' + str(df.groupby(['User Type']).size()))

    # TO DO: Display counts of gender
    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('\nCounts of ' + str(df.groupby(['Gender']).size()))
        print('\nEarliest year of birth: ' + str(int(df['Birth Year'].min())))
        print('Most recent year of birth: ' + str(int(df['Birth Year'].max())))
        print('Most common year of birth: '+ str(int(df['Birth Year'].value_counts().idxmax())))

    else:
        print('\nThere is no data about the customers for Washington.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        show_data = 'yes'
        count = 0
        while show_data == 'yes':
            show_data = input('Would you like to see 5 rows of the data? Enter yes or no.\n').lower()
            if show_data != 'yes':
                break
            else:
                print(df.iloc[count:count+5])
                count += 5

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
