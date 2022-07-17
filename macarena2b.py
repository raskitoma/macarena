#############################################
# Macarena - macarena2.py
# (c)2022, Raskitoma.com
#--------------------------------------------
# Master Script to update Macarena DB transaction
# data. Must run after macarena1.py
#-------------------------------------------- 
# TODO
#-------------------------------------------- 
# Initializing
from macarena_config import my_wallets, my_api_key, json, requests, clear_screen, tqdm, datetime, dump_datetime,selenium_create_browser, BeautifulSoup
from macarena_db import db, Trx, EtherTrx

clear_screen()

# Load all available wallets with associated transactions
all_trx = []
wa_progress = tqdm(total=len(my_wallets), desc="Loading data from Etherscan for {} wallets".format(len(my_wallets)))
for current_wallet in my_wallets:
    wa_progress.update(1)
    requestUrl = "https://api.etherscan.io/api?module=account&action=txlist&address={}&apikey={}".format(current_wallet, my_api_key)
    response = json.loads(requests.get(requestUrl).text)["result"]
    requestUrl2 = "https://api.etherscan.io/api?module=account&action=txlistinternal&address={}&apikey={}".format(current_wallet, my_api_key)
    response2 = json.loads(requests.get(requestUrl2).text)["result"]
    for trx in response:
        hash = trx["hash"]
        blockNumber = trx["blockNumber"]
        try:
            value = float(trx["value"])/10**18
        except:
            value = 0.0
        try:
            gasPrice = float(trx["gasPrice"])/10**18
        except:
            gasPrice = 0.0
        try:
            gas = float(trx["gas"])
        except:
            gas = 0.0
        try:
            gasUsed = float(trx["gasUsed"])
        except:
            gasUsed = 0.0
        contractAddress = trx["contractAddress"]
        tx_from = trx["from"]
        tx_to = trx["to"]
        timeStamp = trx["timeStamp"]
        timestamp = datetime.fromtimestamp(int(timeStamp))
        ether_trx = EtherTrx.query.filter(EtherTrx.hash == hash).first()
        if ether_trx is None:
            ether_trx = EtherTrx(
                hash=hash,
                blockNumber=blockNumber,
                value=value,
                gasPrice=gasPrice,
                gas=gas,
                gasUsed=gasUsed,
                contractAddress=contractAddress,
                tx_from=tx_from,
                tx_to=tx_to,
                timeStamp=timestamp)
            db.session.add(ether_trx)
    db.session.commit()

    for trx in response2:
        hash = trx["hash"]
        blockNumber = trx["blockNumber"]
        try:
            value = float(trx["value"])/10**18
        except:
            value = 0.0
        try:
            gasPrice = float(trx["gasPrice"])/10**18
        except:
            gasPrice = 0.0
        try:
            gas = float(trx["gas"])
        except:
            gas = 0.0
        try:
            gasUsed = float(trx["gasUsed"])
        except:
            gasUsed = 0.0
        contractAddress = trx["contractAddress"]
        tx_from = trx["from"]
        tx_to = trx["to"]
        timeStamp = trx["timeStamp"]
        timestamp = datetime.fromtimestamp(int(timeStamp))
        ether_trx = EtherTrx.query.filter(EtherTrx.hash == hash).first()
        if ether_trx is None:
            ether_trx = EtherTrx(
                hash=hash,
                blockNumber=blockNumber,
                value=value,
                gasPrice=gasPrice,
                gas=gas,
                gasUsed=gasUsed,
                contractAddress=contractAddress,
                tx_from=tx_from,
                tx_to=tx_to,
                timeStamp=timestamp)
            db.session.add(ether_trx)
    db.session.commit()


wa_progress.close()

print ('\nLoaded all transactions for all wallets\n')

# Getting other empty transactions
trx_to_upd = Trx.query.filter(Trx.tx_value == None).all()
tx_progress = tqdm(total=len(trx_to_upd), desc="Getting transactions hashes")
browser = selenium_create_browser()
for tx in trx_to_upd:
    current_hash = tx.hash
    navigateUrl = "https://etherscan.io/tx/{}".format(current_hash)
    browser.get(navigateUrl)
    tx_progress.update(1)
    # locate element by xpath = "//*[@id='ContentPlaceHolder1_maintable']/div[3]/div[2]/a"
    # and get the text
    try:
        blockNumber = int(browser.find_element("xpath","//*[@id='ContentPlaceHolder1_maintable']/div[3]/div[2]/a").text)
    except:
        blockNumber = 0
    # locate span id = "ContentPlaceHolder1_spanValue"
    try:
        value = float(browser.find_element("id","ContentPlaceHolder1_spanValue").text.split(' ')[0])
    except:
        value = 0.0
    # locate span id = "ContentPlaceHolder1_spanGasPrice"
    try:
        gasPrice = float(browser.find_element("id","ContentPlaceHolder1_spanGasPrice").text.split(' ')[0])
    except:
        gasPrice = 0.0
    # locate span id = "ContentPlaceHolder1_spanTxFee"
    try:
        gasUsed = float(browser.find_element("id","ContentPlaceHolder1_spanTxFee").text.split(' ')[0])
    except:
        gasUsed = 0.0
    # calculate gas
    try:
        gas = gasUsed/gasPrice
    except:
        gas = 0.0
    # update the transaction
    tx.tx_value = value
    tx.tx_gas = gas
    tx.tx_gas_price = gasPrice
    tx.tx_gas_used = gasUsed
    tx.tx_block = blockNumber
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print ("Error updating transaction {}".format(current_hash))

tx_progress.close()

print ('\nUpdated all transactions\n')