import datetime
import hashlib
import json

class Block:
    def __init__(self, block_index, time_created, transactions, previous_hash, nonce ):
        self.block_index = block_index
        self.time_created = time_created 
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash_value(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    # Proof of work (PoW)
    def mine(self, difficulty):
        target = '0' * difficulty # Target determines the PoW. Which means that the block must start with a 0, and diffiulty determines how many of 0s should be there
        while not self.hash_value.startswith(target):
            self.nonce +=1
            self.hash = self.hash_value
        # Block is only valid if the target is met
        
class Transactions:
    """
    User transactions amount
    """
    def __init__(self, transaction_id, sender, receiver, data):
        self.ids = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.data = data
    
    def to_dict(self):
        return {
            "Sender: ": self.sender,
            "Receiver: ": self.receiver,
            "Transaction amount: ": self.data,
        }
        
    

class Blockchain: 
    # This class will store data which a normal blockchain should have
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')
        self.pending_transaction = [] # Store blocks that are pending for validation
    
    

    # Add block
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'transactions': [tx.to_dict() for tx in self.pending_transactions],
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.pending_transactions = []  # clear the pool after mining
        self.chain.append(block)
        return block

    # Get previous block
    def get_previous_block(self):
        return self.chain[-1] 
    
    # Chain integreity 
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True
        
    def insert_transaction(self,transaction):
        if self.validate_transaction(transaction):
            self.pending_transaction.append(transaction)
            return True
        else:
            return False
        
    def validate_transaction(self, transaction):
        if not isinstance (transaction, Transactions):
            return False
        
        if not transaction.sender or not transaction.receiver or transaction.data is None:
            return False
        return True