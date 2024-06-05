import hashlib
import json
from time import time

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time(), [], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        previous_hash = self.get_last_block().hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def proof_of_work(self, block, difficulty=2):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_new_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine(self):
        if not self.pending_transactions:
            return False
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1,
                          timestamp=time(),
                          transactions=self.pending_transactions,
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.pending_transactions = []
        return new_block.index

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * 2) and
                block_hash == block.compute_hash())

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Using the blockchain
blockchain = Blockchain()

# Adding some transactions
blockchain.add_new_transaction({"sender": "Alice", "recipient": "Bob", "amount": 50})
blockchain.add_new_transaction({"sender": "Bob", "recipient": "Alice", "amount": 25})

# Mining a block
blockchain.mine()

# Checking the blockchain
for block in blockchain.chain:
    print(vars(block))
