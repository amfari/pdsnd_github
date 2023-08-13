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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (True):
        city = input("Please put in the name of the city (chicago, new york city, washington):").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city selected, please enter a valid city name from these options (chicago, new york city, washington): ")
    # TO DO: get user input for month (all, january, february, ... , june)
    while (True):
        month = input("Please put in the month (all, january, february, ... , june):").lower()
        if month in ["all", "january", "february", "march", "april", "may", "june"]:
            break
        else:
            print("Invalid month selected, please enter a valid month from these options (all, january, february, ... , june): ")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while (True):
        day = input("Please put in the day of the week (all, monday, tuesday, ... sunday):").lower()
        if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            break
        else:
            print("Invalid day selected, please enter a valid day of the week from these options (all, monday, tuesday, ... sunday): ")


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
    file = CITY_DATA[city]
    df = pd.read_csv(file)

    df['Month'] = pd.to_datetime(df['Start Time']).dt.month
    df['Day of Week'] = pd.to_datetime(df['Start Time']).dt.day_name()
    
    if month != 'all':
        month_num = pd.to_datetime(month, format='%B').month
        df = df[df['Month'] == month_num]

    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    
    df.drop(columns=['Month', 'Day of Week'], inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    
    df['Start Time Datetime'] = pd.to_datetime(df['Start Time'])
    
    # reference: https://www.geeksforgeeks.org/python-statistics-mode-function/
    most_common_month = df['Start Time Datetime'].dt.month.mode()[0]
    print(f"The most common month is: {most_common_month}")

    # TO DO: display the most common day of week
    most_common_day = df['Start Time Datetime'].dt.day_name().mode()[0]
    print(f"The most common day of the week is: {most_common_day}")

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time Datetime'].dt.hour.mode()[0]
    print(f"The most common start hour is: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {most_common_start_station}")

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {most_common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax() #https://www.w3schools.com/python/pandas/ref_df_idxmax.asp
    print(f"The most frequent combination of start and end stations is:\n{most_common_combination[0]} to {most_common_combination[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print("Counts of User Types:")
    print(user_type_counts)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:")
        print(gender_counts)
    else:
        print("\nGender information is not available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nBirth Year Statistics:")
        print(f"Earliest year of birth: {int(earliest_birth_year)}")
        print(f"Most recent year of birth: {int(most_recent_birth_year)}")
        print(f"Most common year of birth: {int(most_common_birth_year)}")
    else:
        print("\nBirth Year information is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    """Display raw data if asked for. With first yes, will show first 5 rows of raw data. For the next yes, will show 5 rows after, etc."""
    row_index = 0
    while True:
        display_data = input("Would you like to see (next) 5 lines of raw data? Enter yes or no: ")
        if display_data.lower() == 'yes':
            print(df.iloc[row_index:row_index+5])
            row_index += 5
        else:
            break
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
            
def test_main():
    while True:
        city = "chicago"
        month = "january" 
        day = "Monday"
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

main()
            
if __name__ == "__main__":
	main()
