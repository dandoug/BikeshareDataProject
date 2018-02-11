# Bikeshare Data Project
This project is the code for the Bikeshare Data analysis project as part of the Udacity Learning Python.

The [bikeshare.py](bikeshare.py) script is an interactive terminal program that will
prompt for responses then then investigate one of three data files to
answer the following questions:

* What is the most popular month for start time?
* What is the most popular day of week for start time?
* What is the most popular hour of day for start time?
* What is the total trip duration and average trip duration?
* What is the most popular start station and most popular end station?
* What is the most popular trip?
* What are the counts of each user type?
* What are the counts of gender?
* What are the earliest, most recent, and most popular birth years?

## Data Files
Data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six (6) columns:

* Start Time (e.g. 2017-01-01 00:07:57)
* End Time (e.g. 2017-01-01 00:20:53)
* Trip Duration (in seconds, e.g., 776)
* Start Station (e.g. Broadway & Barry Ave)
* End Station (e.g. Sedgwick St & North Ave)
* User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:

* Gender
* Birth Year

The original files, which can be accessed [here](https://www.divvybikes.com/system-data), had more columns and they differed in format in many cases. 

Even after wrangling, the data files are too large to be stored directly in github.
The post-wrangled data files can be downloaded separately
and extracted from [bikeshare.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/February/5a7a8bf0_bikeshare/bikeshare.zip)

## Resources
* [Stackoverflow.com post about converting csv file to list of dictionaries](https://stackoverflow.com/questions/21572175/convert-csv-file-to-list-of-dictionaries/21572244)