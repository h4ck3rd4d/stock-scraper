#! python3

# stockscraper.py asks user for ticker symbol and date range. 
# Scrapes yahoo finance for the high, low, open, close and volume for
# given ticker and date range.
# Data will be saved to a csv for later use.

import requests, bs4, os

# Gather ticker and date range from user

TICKER = input("Enter ticker symbol: ex. AAPL, MSFT, FB... ")
# validate user input
while True:
    if not TICKER.isalpha():
        TICKER = input("Enter a valid ticker symbol, no numbers: ex. AAPL, MSFT, FB... ")
        continue
    if len(TICKER) < 1 or len(TICKER) > 5:
        TICKER = input("Enter a valid ticker symbol between 1-5 characters long: ex. AAPL, MSFT, FB... ")
        continue
    else:
        TICKER = TICKER.upper()
        print(f"Ticker symbol {TICKER} accepted. ")        
        break
    
DATE_RANGE = int(input("Enter how many days of past data (1-50): "))

## TO-DO add functionality to collect more than 50 days of data. Currently website initialy loads 5 months
## until user scrolls down page to display full year
## need to figure out how to capture this
## for now capping range at 50 days

# validate user input
while True:
    if DATE_RANGE < 1 or DATE_RANGE > 50:
        DATE_RANGE = int(input("Enter how many days of past data (1-50): "))
        continue
    else:
        print(f"Gathering data for {TICKER} from {DATE_RANGE} day/s in the past. ")
        break

# Use requests to download html from https://finance.yahoo.com/quote/TICKER/history?p=TICKER
res = requests.get(f'https://finance.yahoo.com/quote/{TICKER}/history?p={TICKER}')

# Use bs4 to parse html
soup = bs4.BeautifulSoup(res.text, 'html.parser')

# TO-DO check to see if any data was returned. For example, if a string that passes the TICKER validator above
# isn't an actual stock TICKER, there won't be any data returned


# select the table data for date, open, high, low, close, adj close, and volume
myElems = soup.select('td > span')

data = [] # list that will hold all the ticker data

counter = 7 # used to count through myElems[], starts at 7 to not include current day's price info

dataKeys = ["Date","Open","High","Low","Close","Volume"] # key values for data


## nested for loop to add all stock info to data[]
##for i in range(DATE_RANGE):
##    column = {} # dictionary that will combine keys from dataKeys with values from dataValues(below)
##    dataValues = []
##    for j in range(7): # there are 7 fields in table (date, open, high, low, close, adj. close, volume)
##        if j == 5: # we don't need the adj. close data
##            counter += 1
##            
##        else:
##            if i > 0 and myElems[counter].text.strip() == data[i-1]['Date']:
##                counter += 2
##                j = 0         
##            else:
##                dataValues.append(myElems[counter].text.strip()) #strips html and only appends the actual text
##                counter += 1
##        
##    data.append(dict(zip(dataKeys, dataValues))) #combine the keys(dataKeys) and values(dataValues) and appends to data[]

for i in range(DATE_RANGE):
    column = []
    for j in range(7):
        if j == 5:
            counter += 1
        elif myElems[counter].text.strip() == 'Dividend':
            column.append(myElems[counter].text.strip())

            data.append(column)
            counter += 1
            break
        else:
            column.append(myElems[counter].text.strip())
            counter += 1
            
    data.append(column)
# output collected data to csv file

import csv

fileName = f'{TICKER}{DATE_RANGE}days.csv'
path = os.path.abspath(os.getcwd())
print(f'Saving {fileName} to {path} ...')
outputFile = open(os.path.join(path,fileName), 'w', newline='')
outputDictWriter = csv.DictWriter(outputFile, dataKeys)
outputDictWriter.writeheader()
outputCsvWriter = csv.writer(outputFile)
for row in data:
    if 'Dividend' in row:
        continue
    else:
        outputCsvWriter.writerow(row)

outputFile.close()
print(f'Data saved to file {path}\{fileName}')
        

