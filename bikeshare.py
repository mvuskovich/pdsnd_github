import pandas as pd
import statistics
from statistics import mode


#print out for a standard error in the program
def invalidation_error():
    print("Not a valid entry. Try again.")


#takes an integer and changes it to the correspodning month
def month_to_string(mon):

    months = ("January","February","March","April","May","June","None")
    month_str = months[mon]
    return month_str

#takes the month and changes it to the corresponding integer
def month_to_int(mon):

    months = ("January","February","March","April","May","June","None")
    month_num = months.index(mon)

    return month_num


#Loads the input data for filtering. However the conditional statements condition the input to process
#either for month or day and both through the use of truth table logic, i.e. if the user filters by day then
#month is assigned a "None" string parameter. If a value is provided for month, which is an integer, the day
#variable receives a value of "". The city parameter will always be provided. Another option would have been to
#create a column with text months, but this would have used more storage memory.

def load_city_data(city,month, day):

    print("city inside function is:" + city)

    file = ""

#loads the csv file based on input from user

    if city == "New York":
        file = 'new_york_city.csv'
    elif city == "Washington":
        file = 'washington.csv'
    elif city == "Chicago":
        file = 'chicago.csv'

#creation of the dataframe

    df = pd.read_csv(file)

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month']  = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day']  = df['Start Time'].dt.weekday_name
    df['start_end'] = df['Start Station'] + '--->' + df['End Station']


    print("Data processed and ready to analyze")

#the select variable serves to further filter the dataframe depending on the selections made by user
    #select = ""


    if month != "None" and day == "":
        select = df[df['month']==month_to_int(month)]
        print("\n"+ city.upper() + ", MONTH, " + month.upper()  + "\n")
    elif month == "None" and day !="":
        select = df[df['day']==day]
        print("\n"+ city.upper() + ", DAY, " + day.upper() + "\n")
    elif month != "None" and day != "":
        select = df[(df['day']== day) & (df['month'] == month_to_int(month))]
        print("\n"+ city.upper() + ", MONTH AND DAY, " + month.upper() + " and " + day.upper() + "\n")


    print("The most popular month for travelling?")
    print("  " + month_to_string(select['month'].mode()[0]))
    print("The most popular day for travelling?")
    print("  " + select['day'].mode()[0])
    print("The most popular hour of the day to start your travels?")
    print("  " + str(select['hour'].mode()[0]))
    print("What was the total travelling done for 2017 through June, and what was the average time spent " +
             "on each trip?")
    travel_times = select['End Time'] - select['Start Time']
    print("  Total: ")
    print("  " + str(travel_times.sum()))
    print("  Average: ")
    print("  " + str(travel_times.mean()))
    print("Below are the most popular star and end stations respectively")
    print("  Start station: ")
    print("  " + select['Start Station'].mode()[0])
    print("  End station: ")
    print("  " + select['End Station'].mode()[0])
    print("What was the most popular trip from start to end?")
    print("  " + select['start_end'].mode()[0])
    print("What is the breakdown of users?")
    users = select['User Type'].value_counts()
    print("  Subscriber: " + str(users[0]))
    print("  Customer: " + str(users[1]))

    #exception for the lack of gender and birthdate in the Washington DC data

    if city !="Washington":

        gender = select['Gender'].value_counts()
        print("What is the breakdown of gender?")
        print("  Male:" + str(gender[0]))
        print("  Female:" + str(gender[1]))
        print("What s the oldest, youngest and most popular year of birth, respectively?")
        print("  Oldest: " + str(int(select['Birth Year'].min())))
        print("  Youngest: " + str(int(select['Birth Year'].max())))
        print("  Most popular: " + str(int(select['Birth Year'].mode()[0])))
    else:
        print("There is no Gender or Birth Date information for Washington")

#this function provides raw data five lines at a time by splicing a dataframe list with start and end
#variables that are summed by 5 every time the user pressed 'y' to continue

def see_raw_data(city):

    start = 0
    end = 5

    if city == "New York":
        file = 'new_york_city.csv'
    elif city == "Washington":
        file = 'washington.csv'
    elif city == "Chicago":
        file = 'chicago.csv'

    df = pd.read_csv(file)

    df['start_end'] = df['Start Station'] + '--->' + df['End Station']

    while True:

        se = df[["Start Station","End Station","start_end","User Type","Gender","Birth Year"]]
        print(se[start:end])
        cont = input("More raw data? 'y' 'n'? ")
        if cont == "y":
            start += 5
            end += 5
        else:
            break

cities = ("Washington", "New York", "Chicago")


#the time_select funtion allows the user to be redirected to the time_selection input prompt rather
#than being redirected to the first input 'city' input prompt.

def time_select():
    while True:

        time_selection = input("Would you like to analyze by month, day, or both? ").lower()


        if time_selection not in times:
            print("Not a valid entry. Try again.")
            continue

        if time_selection == "month":
            month = input("Type month from January to June: ").title()

            if month not in moy:
                invalidation_error()
                continue

            day=""
            load_city_data(city, month, day)
        elif time_selection == "day":
            day = input("Type day of the week: ").title()

            if day not in dow:
                invalidation_error()
                continue

            month="None"
            load_city_data(city, month, day)
        elif time_selection == "both":

            if time_selection not in times:
                invalidation_error()
                continue

            month = input("Type month: ").title()
            day = input("Type day: ").title()
            load_city_data(city, month, day)
        break

#this function asks user if they would like continue to another city

def cont():
    cont_options = ('y','n','q')
    while True:
        cont = input("Would you like to analyze another city? 'y', 'n' or 'q' to quit: ")
        if cont not in cont_options:
            print("Invalid input. Try again.")
            continue
        else:
            break

#Asks user if they would like to see raw data. If yes, the
#raw_data function is called

def raw_repeat():
    raw_options = ('y','n')
    while True:
        see_raw = input("Would you like to see the raw data? 'y' or 'n' ")
        if see_raw not in raw_options:
            print("Invalid input. Try again.")
            continue
        if see_raw == "y":
            see_raw_data(city)
            print("Thanks for using the system. Goodbye!")
            break
        elif see_raw == "n":
            print("Thanks for using the system. Goodbye!")
            break


#this is the main while loop that ties the functions together


while True:

    city = input("Hello! Let's explore some US bikeshare data. " +
                "Would you like to see data for Chicago, New York or Washington? ").title()
    print("City selected = " + city)

    if city not in cities:
        print("City not valid. Try again.")
        continue

    times = ("month","day","both")
    moy = ("January","February","March","April","May", "June")
    dow = ("Monday", "Tuesday", "Wednesday","Thursday", "Friday", "Saturday", "Sunday")

    time_select()

    cont()

    if cont == "q":
        print("Thanks for using the system.")
        break
    elif cont == "y":
        continue
    else:

        raw_repeat()
        break
