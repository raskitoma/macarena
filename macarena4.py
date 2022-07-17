#############################################
# Macarena - macarena4.py
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
from macarena_db import db, Profitable

clear_screen()
delete_csv_files()


# Load all available wallets with associated transactions
all_trx = []
sql_token_ids = "SELECT * FROM vw_token_id"
tokenids = db.engine.execute(sql_token_ids).fetchall()
wa_progress = tqdm(total=len(tokenids))
for tokenid in tokenids:
    # get buy transaction for this token
    sql_buy = "select yyyy, mmmm, tx_value, tx_gas from vw_trx_wallets where tx_action='BUY' and tx_value is not null and tokenID={} order by timestamp asc limit 1".format(tokenid[0])
    buy_trx = db.engine.execute(sql_buy).fetchall()
    for trx in buy_trx:
        buy_date = trx.yyyy + '-' + trx.mmmm
        buy_price = float(trx.tx_value)
        buy_gas = float(trx.tx_gas)
    # get sell transaction for this token
    sql_sell = "select yyyy, mmmm, tx_value, tx_gas, token from vw_trx_wallets where tx_action='SELL' and tx_value is not null and tokenID={} order by timestamp desc limit 1".format(tokenid[0])
    sell_trx = db.engine.execute(sql_sell).fetchall()
    for trx in sell_trx:
        sell_date = trx.yyyy + '-' + trx.mmmm
        sell_price = float(trx.tx_value)
        sell_gas = float(trx.tx_gas)
        token = trx.token
    # get profit for this token
    try:
        profit = sell_price - buy_price
    except:
        profit = 0
    # get profit percent
    try:
        profit_percent = (profit / buy_price)
    except:
        profit_percent = 0
    # store info into Profitable object
    # search for tokenID in Profitable table
    token_profit = Profitable.query.filter_by(tokenid=tokenid[0]).first()
    if token_profit is None:
        # create new Profitable object
        token_profit = Profitable(token = token,
                                  tokenid=tokenid[0],
                                  buy_date=buy_date,
                                  buy_price=buy_price,
                                  buy_gas=buy_gas,
                                  sell_date=sell_date,
                                  sell_price=sell_price,
                                  sell_gas=sell_gas,
                                  profit=profit,
                                  profit_percent=profit_percent)
        # add to db
        db.session.add(token_profit)
    else:
        # update existing Profitable object
        token_profit.buy_date = buy_date
        token_profit.buy_price = buy_price
        token_profit.buy_gas = buy_gas
        token_profit.sell_date = sell_date
        token_profit.sell_price = sell_price
        token_profit.sell_gas = sell_gas
        token_profit.profit = profit
        token_profit.profit_percent = profit_percent
    # commit to db
    db.session.commit()
    wa_progress.update(1)
wa_progress.close()
print("Done")

#############################################
# End of file