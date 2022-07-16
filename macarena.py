import os, sys
import requests
import json
import pandas as pd
import configparser
import time

# Initializing
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    APPLICATION_PATH = sys._MEIPASS # pylint: disable=no-member
else:
    APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

# clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# request year and month
def get_year_month():
    year = input("Enter year (Enter null for all history): ")
    # if year is empty, return None
    if year == "":
        return None
    # if year is not a number, and has a length of 4, ask again
    elif not year.isdigit() and len(year) == 4:
        print("Year must be a 4 digit number")
        return get_year_month()
    # get month until it has 2 digits and is a number
    month = input("Enter month: ")
    while not month.isdigit() or len(month) != 2:
        print("Month must be a number with 2 digits")
        month = input("Enter month: ")
    return year, month

global config
config = configparser.ConfigParser()
config.read(APPLICATION_PATH + '/settings.ini')

global my_wallets

null_wallet = "0x0000000000000000000000000000000000000000"

try:
    my_wallets = config['GENERAL']['my_wallets'].split(',')
except:
    my_wallets = ''
    print('No wallets configured')
    sys.exit(1)

year_month = get_year_month()
if year_month is None:
    simple_task = True
    print ('No year and month entered, getting data from first tx to last tx...')
else:
    simple_task = False
    Year = year_month[0]
    Month = year_month[1]
    print ('Getting data for ' + Year + '-' + Month + '...')

for current_wallet in my_wallets:
    get_nft_wallet = "https://api.niftyapi.xyz/address/{}/activity"
    request_url = get_nft_wallet.format(current_wallet)
    nfts = json.loads(requests.get(request_url).text)

    transactions = []
    profit_table = []

    for nft in nfts:
        trade_price = nft["trade_price"]
        token_id = nft["token_id"]
        timestamp = nft["timestamp"]
        nft_address = nft["nft"]["address"]
        nft_name = nft["nft"]["name"]
        nft_collection = nft["collection"]["address"]
        get_transaction_history = "https://api.niftyapi.xyz/transfers/{}/{}".format(nft_collection, token_id)
        tx_history = json.loads(requests.get(get_transaction_history).text)
        for tx in tx_history:
            block_number = tx["block_number"]
            transaction_hash = tx["transaction_hash"]
            timestamp = tx["timestamp"]
            to = tx["to"]
            form = tx["from"]
            tx_to = tx["tx_to"]
            tx_from = tx["tx_from"]
            try:
                trade_price = float(tx["trade_price"])/10**18
            except:
                trade_price = 0.0
            appendable = {
                "block_number": block_number,
                "transaction_hash": transaction_hash,
                "timestamp": timestamp,
                "to": to,
                "from": form,
                "tx_to": tx_to,
                "tx_from": tx_from,
                "trade_price": trade_price,
                "token_id": token_id,
                "nft_address": nft_address,
                "nft_name": nft_name,
            }
            transactions.append(appendable)
        
        # get the profit of the nft based on tx_history
        transactions_check = transactions
        # order transactions by timestamp
        transactions_check.sort(key=lambda x: x['timestamp'])
        first_trade_price = 0.0
        for tx in transactions_check:
            if tx['trade_price'] is not None and tx['trade_price'] > 0.0:
                first_trade_price = float(tx['trade_price'])
                start_date = tx['timestamp']
                break
        if not simple_task:
            # check date of last tx from last day of Monht-1
            last_day_of_month = pd.Timestamp(Year + '-' + Month + '-01') - pd.Timedelta(days=1)
            last_day_of_month = last_day_of_month.strftime('%Y-%m-%d')
            for tx in transactions_check:
                if tx['timestamp'] > last_day_of_month and tx['trade_price'] is not None and tx['trade_price'] > 0.0:
                    first_trade_price = float(tx['trade_price'])
                    start_date = tx['timestamp']
                    break   
        last_trade_price = 0.0
        for tx in reversed(transactions_check):
            if tx['trade_price'] is not None and tx['trade_price'] > 0.0:
                last_trade_price = float(tx['trade_price'])
                end_date = tx['timestamp']
                if simple_task:
                    break
                elif end_date[:7] == Year + '-' + Month:
                    break
        # get profit
        profit = last_trade_price - first_trade_price
        # get profit percentage
        try:
            profit_percentage = (profit / first_trade_price) * 100
        except:
            profit_percentage = 0.0
        # get profit percentage rounded to 2 decimal places
        profit_percentage = round(profit_percentage, 2)
        # store profit
        appendable = {
            "token_id": token_id,
            "nft_address": nft_address,
            "nft_name": nft_name,
            "profit": profit,
            "profit_percentage": profit_percentage,
            "start_price": first_trade_price,
            "start_date": start_date,
            "end_price": last_trade_price,
            "end_date": end_date,
        } 
        profit_table.append(appendable) 

    if simple_task:
        my_coda = ''
    else:
        my_coda = Year + '-' + Month
    df = pd.DataFrame.from_dict(transactions)
    df.to_csv("{}_transx_{}.csv".format(current_wallet, my_coda))
    df = pd.DataFrame.from_dict(profit_table)
    df.to_csv("{}_profit_{}.csv".format(current_wallet, my_coda))
    print('Done for ' + current_wallet)
    print('-----------------------------------------------------')
    time.sleep(5)

print('Done')