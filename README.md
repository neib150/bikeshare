### DATE CREATED
11 July 2020

# US BIKESHARE STATISTICS

### DESCRIPTION

This is simply python package that use bike sharing data for 3 major cities in the United States for Chicago, New York City and Washington. 
The package display descriptive statistics about common times of travel, popular stations, trip duration and user information. 
Users are presented with an interactive experience to select a city, month and day of week after which statistics are
 displayed in either console or webapp.

The project was created as part of the Udacity course [Programming for Data Science with Python Nanodegree Program
](https://www.udacity.com/course/programming-for-data-science-nanodegree--nd104)

### FILES USED
Data files were supplied by Udacity to complete this project, which were obtained from [Motivate](https://www.motivateco.com), a bike share system provider.
Data files used are not included in this respositry due to file size.
Udacity should add the data files to directory **'/bikeshare/data/'** before trying to run and rate the project

Files used where:
- chicago.csv
- washington.csv
- new_york_city.csv

Project mainly contains main python file 'statistics.py', with html and css files for the webapp plugin

### SOFTWARE REQUIREMENTS
- Python 3 (Python 3.8 interpreter was used)
- Libraries needed: pandas, numpy, calendar, os, sys, time, Flask
- Data files supplied by Udacity should be copied into directory bikeshare/bikeshare/data/

### INSTALLATION
unzip the file (package will be published to github in the next step of the project)

Option 1: For a console experience: 
```$ cd bikeshare/bikeshare ```
```$ ipython statistics.py```

Option 2: For a web experience: 
```$ cd bikeshare ```
```$ ipython __main__.py```
Open your favorite browser. Enter URL 'http://127.0.0.1:5000/' and enjoy.

### USAGE
The script has two user interfaces:

1) To satisfy all course requirements, run the script in the console. 
The input and output displayed are exactly the same as the webapp, with added feature to display raw data on request. 
 
2) Run the application in a web app for a more friendly user-interface. 
The output displayed are the same as in console, the print statements was instead written to file which is then displayed to html screen.

### EXPECTED STATISTICS
1) **Popular times of travel**
   - Most popular month, but only if user selected all months
   - Most popular day of week, but only if user selected all days
   - Most popular start hour for each day of the week 
     (All starting times are rounded to the nearest hour first )   

2) **Popular stations and trips**
   - 5 most popular start stations
   - 5 most popular end stations
   - 5 most frequent combination of start and stop stations

3) **Trip duration**
   - Total travel time in the city for time periods selected
   - Average travel time for the time periods selected

4) **User info**
   - Counts for each type of user
   - Counts each gender
   - Youngest and oldest cyclists, most common and average age, and the standard deviation after removing outliers of older cyclist.
   
### CREDITS / RESOURCES USED:
1) Udacity extracurricular - Introduction to HTML and CSS
2) HTML element reference - https://developer.mozilla.org/en-US/docs/Web/HTML/Element
3) CSS: https://css-tricks.com/almanac/
4) Web-application tutorial by [Ianertson](https://www.youtube.com/watch?v=Dqd8ZHWErpE) for general FLASH concepts
5) Stack Overflow for general help