# Anaid Garcia
# COMPSCI 383 Homework 0
# Version: 2/6/2021
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


import sys
import csv
import datetime
from datetime import timedelta
import pandas as pd
import numpy as np



# Exercise 0. (8 points)
#
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: datetime.date
      mileage: integer
      location: string
      gallons: float
      price: float (you'll need to get rid of the '$')

    Do not return a tuple for the header row.  And for the love of all that's holy, do not use
    primitive string functions for parsing (use the csv modules instead).

    Hint: to parse the date field, use the strptime function in the datetime module, and then
    use datetime.date() to create a date object.

    See:
      https://docs.python.org/3/library/csv.html
      https://docs.python.org/3/library/datetime.html

    """
    mustard_data = pd.read_csv(file_name)

    # to get rid of the '$' char I used the .replace method in pandas I replaced all the $ with an empty string
    mustard_data['price per gallon'] = mustard_data['price per gallon'].replace(r'[$]','', regex=True)

    # Declaring types for columns
    mustard_data['price per gallon'] = pd.to_numeric(mustard_data['price per gallon'])

    # mustard_data['mileage'] = mustard_data['mileage'].astype('int')
    # mustard_data['price per gallon'] = pd.to_numeric(mustard_data['price per gallon'], downcast='float')
    # mustard_data['gallons'] = pd.to_numeric(mustard_data['gallons'], downcast='float')
    # mustard_data['mileage'] = pd.to_numeric(mustard_data['mileage'], downcast='integer')
    # '%d/%m/%y %H:%M:%S' strptime
    mustard_data['date'] = pd.to_datetime(mustard_data['date'], format = '%m/%d/%Y')

    rows = [(mustard_data.iloc[x]) for x in range(0,len(mustard_data))]  # this list should contain one tuple per row

    #### below is an alternative way to create a tuple but is i
    # records = mustard_data.to_records(index=False)
    # rows = list(records)
    # print(mustard_data.dtypes)
    return rows  # a list of (date, mileage, location, gallons, price) tuples




# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.

    Hint: calculate by multiplying the price per gallon with the  number of gallons for each row.
    """
    count = 0
    # singled out all the gallons and price per gallon and multiplied them based on index
    PerGal = [lis[4] for lis in rows]
    Gal = [lis[3] for lis in rows]
    index = []
    for x in range(0,len(PerGal)):
        count = (float(PerGal[x]) * float(Gal[x]))+ float(count)
    return float(count)  # fix this line to return a float


# Helper function for Exercise 2. and 3.
# this helper function creates a dictionary of loactions
#
def dictionary_Locs(rows):
    Locs = [lis[2] for lis in rows]
    thisdict= {}
    count = 0
    for x in range(0,len(Locs)):
        if Locs[x] in thisdict:
            temp = thisdict[Locs[x]]
            thisdict[Locs[x]] = temp + 1
        else:
            thisdict[Locs[x]] = 1
    return thisdict


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once.

    Hint: store the locations and counts (as keys and values, respectively) in a dictionary,
    then count up the number of entries with a value equal to one.
    """
    '''
    for this function I am going to use a dictionary so I need to parse through the list of locations and if location in not in the dictionary then I need to add
    it and then add a one
    if it is there then I need to get the value and add one to it and set it to the new value which would be one more than the original
    '''
    DictLocs = dictionary_Locs(rows)
    count = 0
    for x in DictLocs.keys():
        if DictLocs[x] == 1:
            count = 1 + count
    return count   # fix this line to return an int


# Exercise 3. (7 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.

    Each list item should be a two-element tuple of the form (name, count).  For example, your
    function might return a list of the form:
      [ ("Honolulu, HI", 42), ("Shermer, IL", 19), ("Box Elder, MO"), ... ]

    Hint: store the locations and counts in a dictionary as above, then convert the dictionary
    into a list of tuples using the items() method.  Sort the list of tuples using sort() or
    sorted().

    See:
      https://docs.python.org/3/tutorial/datastructures.html#dictionaries
      https://docs.python.org/3/howto/sorting.html#key-functions
    """
    DictLocs = dictionary_Locs(rows)

    SortedDict = sorted (DictLocs, key = DictLocs.get, reverse = True)
    Temp = [SortedDict[x] for x in range(0,10) ]
    return [(Temp[x], DictLocs[Temp[x]]) for x in range(0,len(Temp))]  # fix this line to return a list of strings

# Exercise 4. (7 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as
    designated by the two-letter abbreviation at the end of the location string (keys).

    The return value should be a Python dictionary of the form:
      { "CA": 42, "HI": 19, "MA": 8675309, ... }

    Hint: to do this, you'll need to pull apart the location string and extract the state
    abbreviation.  Note that some of the entries are malformed, and containing a state code but no
    city name.  You still want to count these cases (of course, if the location is blank, ignore
    the entry.
    """
    Locs = [lis[2] for lis in rows]
    ComaSplit = [Locs[x].split(",") for x in range (0,len(Locs))]
    thisdict= {}
    for x in range(0,len(ComaSplit)):
        if ComaSplit[x][1] in thisdict:
            temp = thisdict[ComaSplit[x][1]]
            thisdict[ComaSplit[x][1]] = temp + 1
        else:
            thisdict[ComaSplit[x][1]] = 1

    return thisdict  # fix this line to return a dictionary mapping strings to ints


# Exercise 5. (7 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar that refueling took place.

    That is, if you ignore the year, how many different days had entries? (This number should be
    less than or equal to 366!)

    Hint: the easiest way to do this is create a token representing the calendar day.  These could
    be strings (using strftime()) or integers (using date.toordinal()).  Store them in a Python set
    as you go, and then return the size of the set.

    See:
      https://docs.python.org/3/library/datetime.html#date-objects
    """
    set = {''}
    date = [lis[0] for lis in rows]
    count = 0
    MonDay = []
    # for x in range(0,len(date)):
    #     tempMon = str(date[x].month)
    #     tempDay = str(date[x].day)
    #     MonDay = [ tempMon + tempDay] + MonDay
    for x in range(0,len(date)):
        date[x].strftime("%M, %D")
        MonDay = [ date[x].strftime("%m, %d")] + MonDay


    # MonDayInt = [int(MonDay[x]) for x in range(0,len(MonDay))]
    set.update(MonDay)

    return len(set)-1  # this is returning the length minus one bc it always contains an empty int in the first index


# Exercise 6. (7 points)
#
# couts all the num of months in the data
def countDict(rows):
    thisdict = {}
    date = [lis[0] for lis in rows]
    for x in range(0,len(date)):
        if date[x].strftime("%B") in thisdict:
            temp = thisdict[date[x].strftime("%B")]
            thisdict[date[x].strftime("%B")] = temp + 1
        else:
            thisdict[date[x].strftime("%B")] = 1
    return thisdict


def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each
    month of the year (keys).

    The dictionary you return should have 12 entries, with full month names as keys, and floats as
    values.  For example:
        { "January": 3.12, "February": 2.89, ... }
    // I can do 12 arrays for each month or I can multiply and divide as I go (i would need to do a test case and see if it would work if I were to do it as I go or if I wer
    to do it all in one go ) I can also do a nested loop
    I can isolate only the date and price per gallon only get the month and then go from there

    See:
      https://docs.python.org/3/library/datetime.html
    """
    thisdict = {}

    date = [lis[0] for lis in rows]
    PerGal = [lis[4] for lis in rows]
    month = date[3].strftime("%B")
    division = countDict(rows)
    for x in range(0,len(date)):
        if date[x].strftime("%B") in thisdict:
            temp = thisdict[date[x].strftime("%B")]
            thisdict[date[x].strftime("%B")] = temp + PerGal[x]
        else:
            thisdict[date[x].strftime("%B")] = PerGal[x]

    for x in thisdict.keys():
        thisdict[x] = float(thisdict[x])/float(division[x])

    return thisdict # fix this line to return a dictionary


# Exercise 7. (4 points)
#
def these_are_my_words():
    """Return a string constructed from the course syllabus and code of conduct."""

    word1 = "be"  # Change this string to be the i-th word of the Homework Lateness Policy
                   # of the Course Syllabus found on Moodle, where i is the first digit of your
                   # Spire ID (don't forget to start counting at 0).

    word2 = "of"  # Change this string to the j-th word of the Expected Behavior section
                   # of the Code of Conduct found on Moodle, where j is the last digit of your
                   # Spire ID (don't forget to start counting at 0).

    return " ".join([word1, word2])


# EXTRA CREDIT (+0 points, do this for fun and glory)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

    The periods should not overlap.  You should find them in a greedy manner; that is, find the
    highest mileage thirty-day period first, and then select the next highest that is outside that
    window).



        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    df = pd.DataFrame(rows)
    modDf = df.groupby(pd.Grouper(key="date", freq="30D")).sum()
    sortDf = modDf.sort_values(by = 'mileage', ascending=False)
    ThirtyDates = [(sortDf.iloc[x]) for x in range(0,30)]
    mileage = [lis[0] for lis in ThirtyDates]


    hiThirty = [(ThirtyDates[x].name,ThirtyDates[x].name + timedelta(days = 30), mileage[x]) for x in range(0,30)]


    return hiThirty   # fix this line to return a list of tuples


# The main() function below will be executed when your program is run to allow you to check the
# output of each function.
def main(file_name):
    read_data(file_name) #this was added
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))
    #
    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))
    #
    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))
    #
    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")
    #
    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")
    #
    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))
    #
    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")
    #
    words = these_are_my_words()
    print("Exercise 7: {}\n".format(words))
    #
    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    # print("")



#########################

if __name__ == '__main__':

    data_file_name = "mustard_data.csv"
    main(data_file_name)
