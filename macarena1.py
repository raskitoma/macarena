#############################################
# Macarena - macarena1.py
# (c)2022, Raskitoma.com
#--------------------------------------------
# Master Script to Retrieve Data related to NFT
# Transfers from Etherscan.io based on a set of wallets
# declared on settings.ini file
# Needs macarena.py to update transaction values later
#-------------------------------------------- 
# TODO
#-------------------------------------------- 
# Initializing

from datetime import datetime
from macarena_config import selenium_create_browser, my_wallets, time, BeautifulSoup, clear_screen, tqdm
from macarena_db import db, Trx

clear_screen()

# create selenium browser object
browser = selenium_create_browser()

for current_wallet in my_wallets:
    # get html source code
    html_source = "https://etherscan.io/tokentxns-nft?a={}".format(current_wallet)
    # Get initial page
    browser.get(html_source)
    # get text inside xpath: //*[@id="ContentPlaceHolder1_divTopPagination"]/nav/ul/li[3]/span/strong[2]
    # this is the number of pages
    pages = int(browser.find_element("xpath","//*[@id='ContentPlaceHolder1_divTopPagination']/nav/ul/li[3]/span/strong[2]").text)

    transactions = []

    pg_progress = tqdm(total=pages, desc="Loading NFT trxtransf for wallet {}".format(current_wallet))

    for i in range(1, pages+1):
        time.sleep(2.5)
        browser.get(html_source + "&p=" + str(i))
        # get table object with id divSTContainer
        table = browser.find_element("id","divSTContainer")
        # get the source code of the table
        table_source = table.get_attribute("innerHTML")
        # create soup object
        soup = BeautifulSoup(table_source, "html.parser")
        # get all rows in the table
        rows = soup.find_all("tr")
        # remove fist 2 rows (header and empty row)
        rows.pop(0)
        rows.pop(0)
        # iterate between rows
        for row in rows:
            # skip first cell (empty)
            cells = row.find_all("td")
            cells.pop(0)
            # get transaction hash
            tx_hash = cells[0].text
            # get transaction date
            tx_date = cells[1].text
            # convert tx_date to datetime
            tx_date = datetime.strptime(tx_date, "%Y-%m-%d %H:%M:%S")
            # get transaction From
            tx_from = cells[3].text
            # get transaction To
            tx_to = cells[5].text
            # get transaction TokenID
            tx_tokenid = cells[6].text
            # get transaction TokenName
            tx_tokenname = cells[7].text

            # Search tx_hash in database
            trx = Trx.query.filter_by(hash=tx_hash).first()
            if trx is None:
                # if not found, create new trx object
                trx = Trx(tx_hash, None ,tx_date, tx_from, tx_to, tx_tokenid, tx_tokenname, None, None, None, None, None, None)
                # add to database
                db.session.add(trx)
                # commit to database
                try:
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
            else:
                # if found, skip
                continue
        pg_progress.update(1)
    pg_progress.close()

print("Done")