#############################################
# Macarena - DB
# (c)2022, Raskitoma.com
#--------------------------------------------
# Master DB utility functions for bot
#-------------------------------------------- 
# TODO
#-------------------------------------------- 
from flask_sqlalchemy import SQLAlchemy
from macarena_config import app, dump_datetime

# Creating SQLAlchemy db instance
db = SQLAlchemy(app)

class Trx(db.Model):
    '''
    Transaction Table
    '''
    __tablename__ = 'trx'
    hash = db.Column('hash', db.String(128), primary_key=True)
    tx_block = db.Column('tx_block', db.Integer)
    timestamp = db.Column('timestamp', db.DateTime, default=db.func.now())
    tx_from = db.Column('tx_from', db.String(128))
    tx_to = db.Column('tx_to', db.String(128))
    tokenID = db.Column('tokenID', db.Integer)
    token = db.Column('token', db.Text)
    tx_value = db.Column('tx_value', db.Float)
    tx_gas = db.Column('tx_gas', db.Float)
    tx_gas_price = db.Column('tx_gas_price', db.Float)
    tx_gas_used = db.Column('tx_gas_used', db.Float)
    nft_symbol = db.Column('nft_symbol', db.String(128))
    nft_address = db.Column('nft_address', db.String(128))

    def __init__(self, hash, tx_block, timestamp, tx_from, tx_to, tokenID, token, tx_value, tx_gas, tx_gas_price, tx_gas_used, nft_symbol, nft_address):
        self.hash = hash
        self.tx_block = tx_block
        self.timestamp = timestamp
        self.tx_from = tx_from
        self.tx_to = tx_to
        self.tokenID = tokenID
        self.token = token
        self.tx_value = tx_value
        self.tx_gas = tx_gas
        self.tx_gas_price = tx_gas_price
        self.tx_gas_used = tx_gas_used
        self.nft_symbol = nft_symbol
        self.nft_address = nft_address
     
    def __repr__(self):
        return f'hash: {self.hash}, tx_block: {self.tx_block}, timestamp: {dump_datetime(self.timestamp)}, tx_from: {self.tx_from}, tx_to: {self.tx_to}, tokenID: {self.tokenID}, token: {self.token}, tx_value: {self.tx_value}, tx_gas: {self.tx_gas}, tx_gas_price: {self.tx_gas_price}, tx_gas_used: {self.tx_gas_used}, nft_symbol: {self.nft_symbol}, nft_address: {self.nft_address}'

    @property
    def serialize(self):
        '''
        Just to return object data in an easy, serializable way
        '''
        return {
            'hash': self.hash,
            'tx_block': self.tx_block,
            'timestamp': dump_datetime(self.timestamp),
            'tx_from': self.tx_from,
            'tx_to': self.tx_to,
            'tokenID': self.tokenID,
            'token': self.token,
            'tx_value': self.tx_value,
            'tx_gas': self.tx_gas,
            'tx_gas_price': self.tx_gas_price,
            'tx_gas_used': self.tx_gas_used,
            'nft_symbol': self.nft_symbol,
            'nft_address': self.nft_address
        }


class EtherTrx(db.Model):
    '''
    Transaction Table from Etherscan
    '''
    __tablename__ = 'ether_trx'
    hash = db.Column('hash', db.String(128), primary_key=True)
    blockNumber = db.Column('blockNumber', db.Integer)
    timeStamp = db.Column('timeStamp', db.DateTime, default=db.func.now())
    tx_from = db.Column('from', db.String(128))
    tx_to = db.Column('to', db.String(128))
    contractAddress = db.Column('contractAddress', db.String(128))
    value = db.Column('value', db.Float)
    gas = db.Column('gas', db.Float)
    gasPrice = db.Column('gasPrice', db.Float)
    gasUsed = db.Column('gasUsed', db.Float)

    def __init__(self, hash, blockNumber, timeStamp, tx_from, tx_to, contractAddress, value, gas, gasPrice, gasUsed):
        self.hash = hash
        self.blockNumber = blockNumber
        self.timeStamp = timeStamp
        self.tx_from = tx_from
        self.tx_to = tx_to
        self.contractAddress = contractAddress
        self.value = value
        self.gas = gas
        self.gasPrice = gasPrice
        self.gasUsed = gasUsed

    def __repr__(self):
        return f'hash: {self.hash}, blockNumber: {self.blockNumber}, timeStamp: {dump_datetime(self.timeStamp)}, tx_from: {self.tx_from}, tx_to: {self.tx_to}, contractAddress: {self.contractAddress}, value: {self.value}, gas: {self.gas}, gasPrice: {self.gasPrice}, gasUsed: {self.gasUsed}'

    @property
    def serialize(self):
        '''
        Just to return object data in an easy, serializable way
        '''
        return {
            'hash': self.hash,
            'blockNumber': self.blockNumber,
            'timeStamp': dump_datetime(self.timeStamp),
            'tx_from': self.tx_from,
            'tx_to': self.tx_to,
            'contractAddress': self.contractAddress,
            'value': self.value,
            'gas': self.gas,
            'gasPrice': self.gasPrice,
            'gasUsed': self.gasUsed
        }
        

# Initialize DB
db.create_all()

#############################################
# EoF