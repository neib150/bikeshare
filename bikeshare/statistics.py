import calendar
import os
import sys
import time

import numpy as np
import pandas as pd

CITY_DATA = {"Chicago": "chicago.csv",
             "New York City": "new_york_city.csv",
             "Washington": "washington.csv"}

MONTH_NAMES_ABBR = calendar.month_abbr[1:7]
MONTH_NAMES_ABBR.append("All")

DAY_NAMES_ABBR = calendar.day_abbr[:]
DAY_NAMES_ABBR.append("All")

MY_PATH = os.path.abspath(os.path.dirname(__file__))


def get_input_message(counter, filter_name, input_options):
    if not counter:
        message = "Please select a {} from this list you want to analyse: {}  ".format(filter_name, input_options)
    else:
        message = "Please try again, only enter a {} from this list: {}  ".format(filter_name, input_options)
    return message


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("Hello! Let\"s explore some US Bike Share data!")
    city = None
    month = None
    weekday = None
    counter = 0

    while city not in CITY_DATA:
        city = input(get_input_message(counter, "city", list(CITY_DATA.keys()))).title()
        counter += 1

    counter = 0
    while month not in MONTH_NAMES_ABBR:
        while month not in MONTH_NAMES_ABBR:
            month = input(get_input_message(counter, "month", MONTH_NAMES_ABBR)).title()
            counter += 1

    counter = 0
    while weekday not in DAY_NAMES_ABBR:
        while weekday not in DAY_NAMES_ABBR:
            weekday = input(get_input_message(counter, "day of the week", DAY_NAMES_ABBR)).title()
            counter += 1

    return city, month, weekday


def load_data(filename, city, month, day_name):
    """
    Loads data for the specified city and filter by month and day if filtering is needed

    If input file cannot be opened we abort the program
    If 'All' was selected for either month or day, we reset the variables to None
    'All' is chosen to provide a more non-technical user-friendly end-user experience

    Args:
        (str) city - name of the city to analyze
        (str) month - short name of the month to filter by, or "all" to apply no month filter
        (str) day - short name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        city - If city is 'All' is reset to None
        month - if month is 'All' it's reset to None
    """

    message = "\nYou have selected to analyse {} for month {} in weekday {}".format(city, month, day_name)
    print(message)
    print("-" * len(message))

    print('\nLoading file {} .........\n'.format(filename))

    # normalize column names and types across data sets
    column_names = ('recno', 'start_time', 'end_time', 'trip_duration', 'start_station', 'end_station',
                    'user_type', 'gender', 'birth_year')
    column_types = {'recno': 'int64',
                    'trip_duration': 'int64',
                    'start_station' : 'string',
                    'end_station': 'string',
                    'user_type': 'string',
                    'gender': 'string',
                    'birth_year': 'float64'}
    delimiter = ','

    try:
        df = pd.read_csv(filename,
                         delimiter=delimiter,
                         index_col=0,
                         engine='python',
                         names=column_names,
                         skiprows=1,
                         dtype=column_types)
    except Exception as e:
        message = "Could not read the file successfully: {}".format(e)
        print(message)
        sys.exit(1)

    # Parse date fields and handle missing values in the gender field
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df["gender"] = df["gender"].fillna("Unknown")

    # Add new columns that match user input values to help us filter the dataset
    df["weekday"] = df["start_time"].dt.strftime("%a")
    df["month"] = df["start_time"].dt.strftime("%b")

    # Filter the dataset on month and weekday only if 'All' is not selected
    if month == "All":
        month = None
    if month:
        df = df[df["month"] == month]

    if day_name == "All":
        day_name = None
    if day_name:
        df = df[df["weekday"] == day_name]

    return df, month, day_name


def time_stats(df, month, day_name):
    """Displays statistics on the most frequent times of travel."""

    print("Calculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month if "all" was selected
    if not month:
        most_popular_month = df["month"].mode()[0]
        print("The most popular month is {}".format(most_popular_month))

    # display the most common day of week if "all" was selected
    if not day_name:
        most_popular_weekday = df["weekday"].mode()[0]
        print("The most popular day of the week is {}".format(most_popular_weekday))

    # display the most popular start hour by weekday, by first rounding to the nearest hour to get a better average
    df["nearest_start_hour"] = df["start_time"].dt.round("1h").dt.strftime('%H:00')
    popular_start_time = df.groupby('weekday', as_index=False) \
        .agg({'nearest_start_hour': lambda x: pd.Series.mode(x)[0]}) \
        .rename(columns={'weekday': 'Day of Week', 'nearest_start_hour': 'Most popular start time'})
    # sort by day of week, for this day name needs to be converted to day number
    popular_start_time.index = popular_start_time['Day of Week'].map(lambda x: time.strptime(x, '%a').tm_wday + 1)
    popular_start_time = popular_start_time.sort_index()
    print("The most popular start hour for each day of the week is: \n\n{}".format(popular_start_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print("\nCalculating the top 5 most popular start and end stations...\n")
    start_time = time.time()

    # display the top 5 most popular start stations
    popular_start_stations = df["start_station"].value_counts()[:5].to_frame().reset_index()
    popular_start_stations.columns = ["Station", "start_count"]
    print("Top 5 most popular start stations: \n{}".format(popular_start_stations.to_string()))

    # display the top 5 most popular end stations
    print("\n")
    popular_end_stations = df["end_station"].value_counts()[:5].to_frame().reset_index()
    popular_end_stations.columns = ["Station", "end_count"]
    print("Top 5 most popular end stations: \n{}".format(popular_end_stations.to_string()))

    # display most frequent combination of start station and end station trip
    start, stop = df[["start_station", "end_station"]] \
        .groupby(["start_station", "end_station"]) \
        .size() \
        .sort_values(ascending=False).index[0]
    print("\nMost frequent combination of start station and end station: {} => {}\n"
          .format(start, stop))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print("Total travel time of {} is {}".format(city, pd.to_timedelta(df["trip_duration"], unit="s").sum()))

    # display mean travel time
    print("Total average trip duration is {}".format(pd.to_timedelta(df["trip_duration"], unit="s").mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def remove_negative_outliers(data, std_away_from_mean):
    """
    Identify and remove negative outliers from a numpy array.

    Outliers are normally defined as 3 x standard deviations away from the mean.
    Function give flexibility to remove only more extreme outliers, only on the lower range.
    Upper outliers are ignored.

    Args:
        (numpy array) data: numpy array containing a list of values
        (int) m: number of standard deviations away from mean we should remove from the data

    Returns:
        numpy array - with negative outliers are removed
    """

    u = np.mean(data)
    s = np.std(data)
    filtered = data[(data - u) > (std_away_from_mean * s) * -1]
    return filtered


def user_stats(df):
    """Displays statistics on Bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["user_type"].value_counts()
    print("User types statistics: \n{}".format(user_types.to_string()))

    # Display counts of gender
    user_gender = df["gender"].value_counts()
    print("\nGender Statistics: \n{}".format(user_gender.to_string()))

    # Calculate and display descriptive statistics of the year of birth using numpy for faster performance
    birth_year_with_outliers = df['birth_year'].dropna().to_numpy(dtype=int)
    if birth_year_with_outliers.size > 0:
        # Remove negative outliers from birth year to remove very old cyclist that does not represent the population
        birth_year_without_outliers = remove_negative_outliers(data=birth_year_with_outliers, std_away_from_mean=3)
        oldest = birth_year_without_outliers.min()
        youngest = birth_year_without_outliers.max()
        average = int(birth_year_without_outliers.mean())
        variation = int(birth_year_without_outliers.std().round(3))
        most_common = str(pd.Series(birth_year_without_outliers).mode()[0])
        print("\nBirth year statistics with outliers removed: \n")
        print("Youngest birth year:        {}".format(youngest))
        print("Oldest birth year:          {}".format(oldest))
        print("Most common birth year:     {}".format(most_common))
        print("Average birth year:         {}".format(average))
        print("Standard Deviation: {} years".format(variation))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def read_file(filename):
    """A generator function to read a file lazily. Print a defined number of lines from the raw data"""
    while True:

        # Read one line from the file
        data = filename.readline()

        # Break if end of file is reached
        if not data:
            break

        # Yield as we only want to read a certain amount of data and to remember which lines was last printed
        yield data


def print_raw_data(filename):
    """Print raw data 5 lines at a time at user request"""

    raw_request = True
    first_time = True
    another = ""
    answer = {"yes": True, "no": False}

    while raw_request:
        user_input = input("\nWould you like to print {} 5 lines of raw data? Enter yes or no.\n"
                           .format(another)).lower()
        print_raw_request = answer.get(user_input, "error")
        if print_raw_request == "error":
            print("\nPlease enter only 'yes' or 'no'")
            continue
        elif print_raw_request:
            if first_time:
                first_time = False
                another = "another"
                try:
                    file = open(filename)
                    file_gen = read_file(file)
                except Exception as e:
                    print("\nError occurred, cannot open file {}".format(e))
                # first time we want to print also the heading
                lines = 6
            else:
                lines = 5

            for i in range(lines):
                print(next(file_gen))
        else:
            if not first_time:
                file.close()
            break


def main(city, month, day_name):
    input_filename = os.path.join(MY_PATH + '/data/' + CITY_DATA[city])
    df, month, day_name = load_data(input_filename, city, month, day_name)
    time_stats(df, month, day_name)
    station_stats(df)
    trip_duration_stats(df, city)
    user_stats(df)

    if __name__ == "__main__":
        return input_filename


def webapp_main(city, month, day_name):
    """
    Entry point from web application to statistical calculations

    Redirect print statements to an output file only when called from webapp

    Args:
        (str) city - name of the city to analyze example 'Chicago'
        (str) month - short name of the month to filter by (e.g. Jan), or "All" to apply no month filter
        (str) day - short name of the day of week (e.g. Mon, Tue) to filter by, or "All" to apply no day filter

    Returns:
        out_filename - location where the statistical results or errors are stored so it can be printed to html
    """
    temp = sys.stdout
    out_filename = os.path.join(MY_PATH + '/data/output')
    sys.stdout = open(out_filename, 'w')
    try:
        main(city, month, day_name)
    except:
        #   error messages are re-routed to output file and will be printed out in webapp afterwards
        pass

    sys.stdout = temp
    return out_filename


if __name__ == "__main__":
    """
    Run statistical calculations by calling directly the python program without the webapp plug-in

    User input are collected via the terminal instead, and output are printed to console
    By running the statistical analysis without the webapp plug-in users get an extra choice to see raw input
    """
    while True:

        city_input, month_input, day_name_input = get_filters()
        in_filename = main(city_input, month_input, day_name_input)

        print_raw_data(in_filename)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() == "no":
            print("Goodbye !!!")
            break
