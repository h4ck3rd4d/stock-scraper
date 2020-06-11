#! python3

# stockscraper.py asks user for ticker symbol and date range. 
# Scrapes yahoo finance for the high, low, open, close and volume for
# given ticker and date range.
# Data will be saved to a csv for later use.

import requests, bs4, os, csv

# Gather ticker and date range from user

def get_ticker():
    global ticker
    ticker = input("Enter ticker symbol: ex. AAPL, MSFT, FB... ")
    # validate user input
    while True:
        if not ticker.isalpha():
            ticker = input("Enter a valid ticker symbol, no numbers: ex. AAPL, MSFT, FB... ")
            continue
        if len(ticker) < 1 or len(ticker) > 5:
            ticker = input("Enter a valid ticker symbol between 1-5 characters long: ex. AAPL, MSFT, FB... ")
            continue
        else:
            ticker = ticker.upper()
            print(f"Ticker symbol {ticker} accepted. ")        
            return ticker
    

## TO-DO add functionality to collect more than 50 days of data. Currently website initialy loads 5 months
## until user scrolls down page to display full year
## need to figure out how to capture this
## for now capping range at 50 days

def get_date_range():
    global date_range
    date_range = int(input("Enter how many days of past data (1-50): "))

    while True:
        if date_range < 1 or date_range > 50:
            date_range = int(input("Enter how many days of past data (1-50): "))
            continue
        else:
            print(f"Will gather data from {date_range} day/s in the past. ")
            return date_range

def get_stock_data():
    ticker = get_ticker()
    date_range = get_date_range()

    # Use requests to download html from https://finance.yahoo.com/quote/TICKER/history?p=TICKER
    res = requests.get(f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}')

    # Use bs4 to parse html
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # TO-DO check to see if any data was returned. For example, if a string that passes the TICKER validator above
    # isn't an actual stock TICKER, there won't be any data returned


    # select the table data for date, open, high, low, close, adj close, and volume
    myElems = soup.select('td > span')
    global data
    data = [] # list that will hold all the ticker data

    counter = 7 # used to count through myElems[], starts at 7 to not include current day's price info


    for i in range(date_range):
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
def save_data():
    
    dataKeys = ["Date","Open","High","Low","Close","Volume"] # key values for data
    
    fileName = f'{ticker}{date_range}days.csv'
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
        

