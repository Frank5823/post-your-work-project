import time
import pandas as pd
import numpy as np

#lists of possible entries to filter the available data
#theese are needed to filter by the users input
cities =["chicago","new york city", "washington"]
days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
months=["january","february","march","april","may","june","july","august","september", "october","november","december"]
options=['day','month','both','none']

#import the data from csv files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#get user input for city (chicago, new york city, washington)
def city_input():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("please select one of the following 3 cities: chicago, new york city, washington: ").lower()
    while city not in cities:
        city = input("You typed: " + city + ". Please select only one of the 3 available cities (chicago, new york city, or washington):  ").lower()
    return city
#get user input for filter (month, day,both, or none)
def filter_input():
    selection=input("Do you want to filter by month, day, both, or not at all? type (month, day, both, or none): ").lower()
    while selection not in options:
        selection = input("You typed: " + selection + ". Please select day, month, both, or none ").lower() 
    return selection
#get user input for month
def month_input():
    month = input("which month do you want to anlayse?: ").lower()
    while month not in months:
        month = input("You typed: " + month + ". Please select a valid month: ").lower()               
    return month
#get user input for day
def day_input():
    day = input("which day do you want to anlayse?: ").lower()
    while day not in days:
        day = input("You typed: " + day + ". Please select a valid day").lower()
    return day

#Loads data for the specified city and filters by month and day if applicable.
def load_data():
    city=city_input()
    selection=filter_input()
    if selection == 'both':
        month= month_input()
        day=day_input()
    elif selection=='month':
        month= month_input()
        day='all'
    elif selection=='day':
        day=day_input()
        month='all'
    elif selection=='none':
        day='all'
        month='all'
    print('You filter by:' + selection)    
    print('You selected: ' + city +' '+ month+' '+day)
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        month = months.index(month) + 1   
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]
    
    print(df.head())
    return df, city, month, day

 #   Args:
 #       (str) city - name of the city to analyze
 #       (str) month - name of the month to filter by, or "all" to apply no month filter
 #       (str) day - name of the day of week to filter by, or "all" to apply no day filter
 #   Returns:
 #       df - Pandas DataFrame containing city data filtered by month and day
 #   """
#
#
#   return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
#   display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Popular month:', popular_month)
    #: display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular day:', popular_day)
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*90)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    gb = df.groupby(["Start Station", "End Station"]).size()
    kombination = gb.idxmax()
    anzahl = gb.max()
    print("\nthe most common combination of start and end sation is: ", kombination, "with", anzahl, "trips ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*90)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("the total travel time was: ", total_travel_time, "seconds")
    # TO DO: display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("the mean travel time was: ", mean_travel_time, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*90)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types    
    if 'User Type' in df.columns:
        print(df['User Type'].value_counts())
    else:
        print('No user type data available for', city)
        
    # Display counts of gender        
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print('No gender data available for', city)

      # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('\nThe earliest birth year is:', earliest)
        print('The most recent birth year is:', most_recent)
        print('The most common birth year is:', most_common)
    else:
        print('\nNo birth year data available for', city)
    # TO DO: 

       
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*90)

def main():
    while True:
        #city, month, day = get_filters()
        df, city, month, day = load_data()

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
