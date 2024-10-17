# We need the time library to measure the time it takes to run certain calculations
# The pandas library is used to load and manipulate the data
# The numpy library is used to perform statistical calculations
# The typing library is used to add type hints to improve code readability

import time
import pandas as pd
import numpy as np
from typing import Tuple, Dict

# Constants
CITY_DATA: Dict[str, str] = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS: Tuple[str, ...] = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all')
DAYS: Tuple[str, ...] = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')

def get_filters() -> Tuple[str, str, str]:
    """
    Prompts user to specify a city, month, and day to analyze.

    Returns:
        Tuple[str, str, str]: A tuple containing:
            - city: name of the city to analyze
            - month: name of the month to filter by, or "all" to apply no month filter
            - day: name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input("Enter the name of the city you want to analyze (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please try again.")

    # Get user input for month
    while True:
        month = input("Enter the name of the month you want to filter by (or 'all' to apply no month filter): ").lower()
        if month in MONTHS:
            break
        print("Invalid month. Please try again.")

    # Get user input for day of week
    while True:
        day = input("Enter the name of the day you want to filter by (or 'all' to apply no day filter): ").lower()
        if day in DAYS:
            break
        print("Invalid day. Please try again.")

    print('-'*40)
    return city, month, day

def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        city (str): Name of the city to analyze.
        month (str): Name of the month to filter by, or "all" to apply no month filter.
        day (str): Name of the day of week to filter by, or "all" to apply no day filter.

    Returns:
        pd.DataFrame: Pandas DataFrame containing city data filtered by month and day.
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (pd.DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Helper function to display most common values
    def display_most_common(column: str, title: str) -> None:
        value_counts = df[column].value_counts()
        max_values = value_counts[value_counts == value_counts.max()].sort_index()
        for value, count in max_values.items():
            print(f"The most common {title} is: {value.title() if type(value) == str else value} with {count} trips.")

    display_most_common('month', 'month')
    display_most_common('day_of_week', 'day of week')

    # Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    display_most_common('start_hour', 'start hour')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def station_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (pd.DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Helper function to display most common stations
    def display_most_common_station(column: str) -> None:
        value_counts = df[column].value_counts()
        max_stations = value_counts[value_counts == value_counts.max()].sort_index()
        for station, count in max_stations.items():
            print(f"The most common {column.lower()} is: {station} with {count} trips.")

    display_most_common_station('Start Station')
    display_most_common_station('End Station')

    # Display most frequent combination of start station and end station trip
    combined_stations = df.groupby(['Start Station', 'End Station']).size()
    most_common = combined_stations[combined_stations == combined_stations.max()]
    for (start, end), count in most_common.items():
        print(f"The most common combination of stations is: {start} to {end} with {count} trips.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def trip_duration_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print(f"The total travel time is: {total_travel_time / 3600:.2f} hours")
    print(f"The mean travel time is: {mean_travel_time / 60:.2f} minutes")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def user_stats(df: pd.DataFrame) -> None:
    """
    Displays statistics on bikeshare users.

    Args:
        df (pd.DataFrame): The DataFrame containing the bikeshare data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender if available
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())

    # Display birth year statistics if available
    if 'Birth Year' in df.columns:
        birth_year = df['Birth Year'].dropna()
        print(f"The earliest year of birth is: {int(birth_year.min())}")
        print(f"The most recent year of birth is: {int(birth_year.max())}")
        print(f"The most common year of birth is: {int(birth_year.mode().iloc[0])}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)

def show_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Asks the user if they want to view raw data.

    Args:
        df (pd.DataFrame): The DataFrame containing the raw data.

    Returns:
        pd.DataFrame: The DataFrame containing the bikeshare data.
    """
    while True:
        raw_data = input('\nWould you like to view the raw data? Enter yes or no.\n')
        if raw_data.lower() != 'yes':
            break
        else:
            number_of_rows = int(input('Enter the number of rows you want to view: '))
            while number_of_rows > df.shape[0]:
                print(f'The number of rows is greater than the total number ({df.shape[0]}) of rows in the DataFrame.')
                number_of_rows = int(input('Enter the number of rows you want to view: '))
            print(df.head(number_of_rows))
            break

def main() -> None:
    """
    Main function to run the bikeshare data analysis program.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
