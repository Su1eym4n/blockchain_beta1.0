from hashlib import sha256
import json
import time

from flask import Flask
from random import seed
from random import randint


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        hstr = json.dumps(self.__dict__, sort_keys=True)
        return sha256(hstr.encode()).hexdigest()


class Blockchain:
    # security level
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    # creates first block
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    #retruns last block
    @property
    def last_block(self):
        return self.chain[-1]

    #adding block after verification
    def add_block(self, block, proof):

        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False


        block.hash = proof
        self.chain.append(block)
        return True

    #checks if the block starts with 2 zeros
    def is_valid_proof(self, block, block_hash):

        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    #creating hash that will satisfy security level
    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    #adding unconfirmed transaction (It will not be added to chain until verified)
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)


    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index


app = Flask(__name__)
blockchain = Blockchain()

print("Genesis Chain")
print(blockchain.last_block.__dict__)


x = 0

seed(1)
commands = ["buy", "sell", "exchange"]
print("Mining started")
while x <= 5:
    num = randint(0, 2)
    word = commands[num]

    blockchain.add_new_transaction(word)
    blockchain.mine()
    print(blockchain.last_block.__dict__)
    x = x + 1


print("All blockchain")
for block in blockchain.chain:
    print(block.__dict__)

#
#
# @app.route('/chain', methods=['GET'])
# def get_chain():
#     chain_data = []
#     for block in blockchain.chain:
#         chain_data.append(block.__dict__)
#     return json.dumps({"length": len(chain_data),
#                        "chain": chain_data})
#
#
# # In[45]:
#
#
#
# app.run(debug=True, port=5000)

