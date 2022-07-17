#############################################
# Macarena - macarena3.py
# (c)2022, Raskitoma.com
#--------------------------------------------
# Script to obtain token profit data from 
#  Macarena DB transaction
# Can run as long as macarena.db has data
#-------------------------------------------- 
# TODO
#-------------------------------------------- 
# Initializing
from macarena_config import delete_csv_files, my_wallets, clear_screen, tqdm, pd, DATA_FOLDER, get_year_month, datetime
from macarena_db import db

clear_screen()
delete_csv_files()

year_month =  get_year_month()

simple_mode = False
if year_month is None:
    simple_mode = True

# Load all available wallets with associated transactions
all_trx = []
wa_progress = tqdm(total=len(my_wallets), desc="Review {} wallets".format(len(my_wallets)))
for current_wallet in my_wallets:
    current_trx = []
    # get all tokens for current wallet
    sql_tokens = "SELECT * FROM vw_tokens"
    tokens = db.engine.execute(sql_tokens).fetchall()
    tc_progress= tqdm(total=len(tokens), desc="Token {} - wallet {}".format(len(tokens), current_wallet))
    for token in tokens:
        my_token = token.token
        if not simple_mode:
            my_year = year_month[0]
            my_month = year_month[1]
            # get last day of my_year and my_month
            last_day = pd.Timestamp(datetime(int(my_year), int(my_month), 1) + pd.tseries.offsets.MonthEnd()).day
            transaction_dating = " AND timestamp <= '{}-{}-{}'".format(my_year, my_month, last_day)


        sql_transactions = "select trx.timestamp, trx.hash, trx.tx_block, trx.tx_from, trx.tx_to, trx.tokenID, trx.token, trx.tx_value, \
            IF(STRCMP(trx.tx_to,'" + current_wallet +  "')=0, 'BUY','SELL') as trx_action \
            from trx where (trx.tx_to = '" + current_wallet +  "' or trx.tx_from = '" + current_wallet +  "') \
            and token = \"" + my_token + "\"  \
            and tx_value is not null \
                " + transaction_dating  +  " \
            order by trx.timestamp asc"
        transactions = db.engine.execute(sql_transactions).fetchall()
        # if no transactions, skip
        if len(transactions) == 0:
            continue
        # locate first transaction where trx_action is BUY
        first_buy_trx = None
        for trx in transactions:
            if trx.trx_action == "BUY":
                first_buy_trx = trx.tx_value
                first_buy_date = trx.timestamp
                break
        # locate last transaction where trx_action is SELL
        last_sell_trx = None
        for trx in reversed(transactions):
            if trx.trx_action == "SELL":
                last_sell_trx = trx.tx_value
                last_sell_date = trx.timestamp
                break
        # get profit
        try:
            profit = last_sell_trx - first_buy_trx
        except:
            profit = 0

        # get profit percentage
        try:
            profit_percentage = (profit / first_buy_trx) * 100
        except:
            profit_percentage = 0

        # create a new Trx object
        new_trx = {
            "wallet": current_wallet,
            "token": my_token,
            "first_buy_trx": first_buy_trx,
            "first_buy_date": first_buy_date,
            "last_sell_trx": last_sell_trx,
            "last_sell_date": last_sell_date,
            "profit": profit,
            "profit_percentage": profit_percentage
        }
        current_trx.append(new_trx)
        all_trx.append(new_trx)
        tc_progress.update(1)
    tc_progress.close()
    # create csv file from all_trx
    df = pd.DataFrame(current_trx)
    df.to_csv(DATA_FOLDER + "{}_profits.csv".format(current_wallet), index=False)    
    wa_progress.update(1)
wa_progress.close()


df = pd.DataFrame(all_trx)
df.to_csv(DATA_FOLDER + "allwallets_profits.csv", index=False)
print("Done")
#############################################
# End of file