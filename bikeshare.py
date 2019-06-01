import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all',
          'january', 'february', 'march', 'april',
          'may', 'june', 'july', 'august',
          'september', 'october', 'november', 'december']

DAYS = ['all',
        'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']

def validate_input(data_set, input_description):    
    """
    Asks user to specify a value and checks if it is correct (available in the data_set).
    
    Args:
        (list) data_set - correct values for the user input
        (str) input_description - the name of the user input value

    Returns:
        (str) city - user input, one value from the data_set
    """
    # The source of the validation concept: 
    # https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
    # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
    
    while True:
        val = input("Enter the name of the " + input_description + " to analyze (" + ", ".join(data_set).title() + "): ");
        try:
            if val.lower() not in data_set:
                raise ValueError
        except ValueError:
            print("Unknown " + input_description + ". Please try again.")
            continue
        else:
            return val

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = validate_input(list(CITY_DATA.keys()), 'city')
    month = validate_input(MONTHS, 'month')
    day = validate_input(DAYS, 'day')
    
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
    ### Approach like in the "Practice Problem/Solution #3".
    
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day Of Week'] = df['Start Time'].dt.weekday_name
    
    if month.lower() != 'all':
        df = df[df['Month'] == MONTHS.index(month.lower())]
        
    if day.lower() != 'all':
        df = df[df['Day Of Week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    ### Approach like in the "Practice Problem/Solution #1".
    
    # TO DO: display the most common month
    print('Most Popular Month:', MONTHS[df['Month'].mode()[0]].title())

    # TO DO: display the most common day of week
    print('Most Popular Day Of Week:', df['Day Of Week'].mode()[0])

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    print('Most Popular Start Hour:', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

     ### Solution similar to the "Practice Problem/Solution #1"
    
    # TO DO: display most commonly used start station
    print('Most Popular Start Station:', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most Popular End Station:', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most Popular Combination Of Start-End Stations:', df['Station Combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The Total Travel Time:', df['Trip Duration'].sum()/60/60, 'hours')

    # TO DO: display mean travel time
    print('The Mean Travel Time:', df['Trip Duration'].mean()/60, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts Of User Types:')
    for k, v in user_types.items():
        print(k, '=', v)

    ### Gender and Birth Year need to be checked if they exist in data.
        
    # TO DO: Display counts of gender
    print('\nCounts Of User Gender:')
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        for k, v in gender.items():
            print(k, '=', v)
    else:
        print("Data is not available.")
                

    # TO DO: Display earliest, most recent, and most common year of birth
    print('\nBirth Statistics:')
    if 'Birth Year' in df.columns:
        print('Earliest Year Of Birth:', df['Birth Year'].min())
        print('Most Recent Year Of Birth:', df['Birth Year'].max())
        print('Most Common Year Of Birth:', df['Birth Year'].mode()[0])      
    else:
        print("Data is not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data for the user request."""
    
    # Clear extra columns if they exist (errors = 'ignore')
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    df.drop(['Month', 'Day Of Week', 'Start Hour', 'Station Combination'], axis=1, inplace=True, errors='ignore')
    id_counter = 0
    while True:
        val = input("Would you like to view individual trip data? Type yes/no: ");
        try:
            if val.lower() not in ['yes', 'no']:
                raise ValueError
        except ValueError:
            print("Unknown value. Please try again.")
            continue
        else:
            if val == 'yes':
                print(df[id_counter:id_counter+5])
                id_counter+=5;
            else:                
                break

def main():
    print("Welcome in BikeShare Analyzer!")
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Check if there are available data to analyze
        if df.empty:
            print("No data available with the selected filters.")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)        
            display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
