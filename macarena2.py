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
from macarena_config import my_wallets, my_api_key, json, requests, clear_screen, tqdm
from macarena_db import db, Trx

clear_screen()

# Load all available wallets with associated transactions
all_trx = []
wa_progress = tqdm(total=len(my_wallets), desc="Loading data from Etherscan for {} wallets".format(len(my_wallets)))
for current_wallet in my_wallets:
    requestUrl = "https://api.etherscan.io/api?module=account&action=txlist&address={}&apikey={}".format(current_wallet, my_api_key)
    response = json.loads(requests.get(requestUrl).text)["result"]
    wa_progress.update(1)
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
        trx_obj = {
            "hash": hash,
            "blockNumber": blockNumber,
            "value": value,
            "gasPrice": gasPrice,
            "gas": gas,
            "gasUsed": gasUsed
        }
        all_trx.append(trx_obj)
    
wa_progress.close()

print ('\nLoaded all transactions for all wallets\n')

# open Trx table for all transactions that tx_value = None
# and update the tx_value and tx_gas_used
# hash, tx_block, timestamp, tx_from, tx_to, tokenID, token, tx_value, tx_fee, tx_gas_price, tx_eth_price, nft_symbol, nft_address
trx_to_upd = Trx.query.filter(Trx.tx_value == None).all()
tx_progress = tqdm(total=len(trx_to_upd), desc="Updating transactions")
for tx in trx_to_upd:
    current_hash = tx.hash
    tx_progress.update(1)
    # search current_hash in all_trx
    for trx_obj in all_trx:
        if trx_obj["hash"] == current_hash:
            tx.tx_value = trx_obj["value"]
            tx.tx_block = trx_obj["blockNumber"]
            tx.tx_gas_used = trx_obj["gasUsed"]
            tx.tx_gas_price = trx_obj["gasPrice"]
            tx.tx_gas = trx_obj["gas"]
            db.session.commit()
            break
tx_progress.close()

print ('\nUpdated all transactions\n')