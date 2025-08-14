import datetime
import hashlib
import json

class Block:
    def __init__(self, block_index, time_created, transactions, previous_hash, nonce):
        self.block_index = block_index
        self.time_created = time_created 
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        }
        

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
        """_summary_

        Returns:
            _type_: _description_
        """
        return {
            "Ids" : self.ids,
            "Sender: ": self.sender,
            "Receiver: ": self.receiver,
            "Transaction amount: ": self.data,
        }
        

class Blockchain: 
    # This class will store data which a normal blockchain should have
    def __init__(self):
        self.chain = []
        # self.pending_transaction = [] # Store blocks that are pending for validation
        self.create_block(data = "Test genesis", proof = 1, previous_hash="0", index = 0)

    

    def to_digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        """
        Args:
            new_proof (int): _description_``
            previous_proof (int): _description_
            index (str): _description_
            data (str): _description_
        Returns:
            bytes: _description_
            
        to_digst: takes input data and use a hash function sha256 to produce a string of bytes
        """
        to_digest = str(new_proof ** 2 - previous_proof **2 + index) + data
        return to_digest.encode()
    
    # Proof of work
    def proof_of_work(self, previous_proof: int, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            # print(new_proof)  # optional: uncomment to watch mining progress
            to_digest = self.to_digest(
                new_proof=new_proof,
                previous_proof=previous_proof,
                index=index,
                data=data,
            )
            hash_value = hashlib.sha256(to_digest).hexdigest()
            if hash_value[:4] == "0000":  # Bigger the value the more time it will take to find this proof
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Hash value
    def hash_value(self, block):
        """_summary_

        Args:
            block (_type_): _description_

        Returns:
            _type_: _description_
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
            
    # ---- Block ----
    def mine_block(self, data: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = previous_block["index"] + 1      # <-- was len(self.chain) + 1
        proof = self.proof_of_work(previous_proof, index, data)
        previous_hash = self.hash_value(previous_block)
        block = self.create_block(data=data, proof=proof,
                                previous_hash=previous_hash, index=index)
        return block

    
    # Create block
    def create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            # 'transactions': [tx.to_dict() for tx in self.pending_transactions],
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.pending_transactions = []  # clear the pool after mining
        self.chain.append(block)
        return block
    
    # Get previous block
    def get_previous_block(self) -> dict:
        return self.chain[-1] 
    
    # Chain integreity 
    def is_chain_valid(self) -> bool: ## Job is to make sure that the chain is still valid and no alteration been made
        """  """
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash_value(previous_block):
                return False

            current_proof = previous_block['proof']
            next_index, next_data , next_proof = (
                block["index"],
                block["data"],
                block["proof"],
            )
            hash_value = hashlib.sha256(self.to_digest(new_proof=next_proof, previous_proof=current_proof, 
                                                       index = next_index, data = next_data)).hexdigest()
            if hash_value[:4] != "0000":
                return False
            
            previous_block = block
            block_index +=1
        
        return True
            
              
    # ---- Data Persistence ----
    # Save Blockchain
    def save_chain(self):
        with open("blockchain.json", "w") as f:
            json.dump(self.chain, f , indent=4)

    # Load block chain
    def load_chain(self):
        
         with open("blockchain.json", "r") as f:
             self.chain = json.load(f)

    # ---- Transactions ----
    def check_transactions(self, tx_id: str) -> bool: # Check for duplication transactions_id
        """ Double spend-prevention """
        if not tx_id:
            return False # No tx exists
        
        for transactions in self.pending_transactions:
            if transactions.get("id") == tx_id:
                return True
        for block in self.chain:
            for transactions in block.get("transactions", []):
                if transactions.get("id") == tx_id:
                    return True
        return False
    
    def insert_transaction(self, transaction: Transactions) -> bool:
        """Insert a transaction object into the mempool if valid."""
        if not isinstance(transaction, Transactions):
            return False

        tx = transaction.to_dict()

        if not self.validate_transaction(tx):
            return False

        if self._tx_exists(tx["id"]):
            return False

        self.pending_transactions.append(tx)
        return True

    def validate_transaction(self, tx: dict) -> bool:
        """Check fields are present and amount is valid."""
        sender = tx.get("sender")
        receiver = tx.get("receiver")
        amount = tx.get("amount")

        if not sender or not receiver or amount is None:
            return False
        try:
            return float(amount) >= 0
        except (TypeError, ValueError):
            return False