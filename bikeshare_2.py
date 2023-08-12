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
    # get user input for city (chicago, new york city, washington). 
    city = input("Which city data would you like to enter? Please type in Chicago, New York City, or Washington:\n").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input ("There is no data available for that. Please enter valid city: ")

    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to enter? Please type in January, February, March, April, May, June, or 'all' for no month filter:\n").lower()
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = input("There is no data available for that. Please enter valid month or 'all': ")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to enter? Please type in Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all' for no day filter:\n").lower()
    while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("There is no data available for that. Please enter valid month or 'all': ")
    
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
    
    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # separate Start Time into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if not all
    if month != 'all':
        # using index of month for corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create new dataframe
        df = df[df['month'] == month]

    # filter by day if not all
    if day != 'all':
        # filter by day to create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is:", df['month'].mode()[0])

    # display the most common day of week
    print("The most common day of week  is:", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most common start hour is:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is:", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is:", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + " to " + df['End Station']
    print("The most frequent combination of start station and end station trip is:", df['combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    print("The total travel time is {} days, {} hours, {} minutes, and {} seconds.".format(days, hours, minutes, seconds))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("The mean travel time is", mean_duration/60, "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The user type counts are:\n",df['User Type'].value_counts(),'\n')

    # Display counts of gender, exclude Washington
    if city != 'washington':
        print("The user gender counts are:\n",df['Gender'].value_counts(),'\n')

        # Display earliest, most recent, and most common year of birth
        ea_year_of_birth = int(df['Birth Year'].min())
        mr_year_of_birth = int(df['Birth Year'].max())
        mc_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
        print("The earliest year of birth is:",ea_year_of_birth,'\n'"The most recent year of birth is:",mr_year_of_birth,'\n'"The most common year of birth is:",mc_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data (df):
    """Use descriptive statistics to answer questions about the data. Raw data is displayed upon request by the user.
    Your script should prompt the user if they want to see 5 lines of raw data,
    Display that data if the answer is 'yes',
    Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
    Stop the program when the user says 'no' or there is no more raw data to display."""
    
    while True:
        raw_data = input("Would you like to see 5 lines of raw data? Enter 'yes' to see data, or 'no' to stop:\n").lower()
        if raw_data == 'no':
            break
        else:
            row = 0
            row = row+5
            print(df.head(row))
 

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()