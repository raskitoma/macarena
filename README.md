# Macarena

A simple script that connects to etherscan.io and api.etherscan.io and obtains transactions and profit for NFT tokens transfers from a set list of wallets.

## Usage

Install requirements with `pip install -r requirements.txt`

Create a mysql database with the schema included in this repository: [macarena.sql](macarena.sql)

To generate data, run scripts in the following order:

1. Grab all NFT trade transactions for the wallets described in settings.ini using `python macarena1.py`
2. Run `python macarena2.py` and `python macarena2b.py` to complete transaction data for all transactions in the database.
3. Run `python macarena3.py` to obtain profit data for each of the wallets as csv files.

> Repeat steps 1 and 2 to update transaction data for current or new wallets
